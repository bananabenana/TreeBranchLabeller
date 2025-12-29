import argparse
from Bio import AlignIO
from Bio.Seq import Seq
from ete3 import Tree
import os
import subprocess

r_script_path = os.path.join(os.path.dirname(__file__), "TreeBranchLabeller_plot.R")


def parse_newick(newick_file):
    return Tree(newick_file)

def parse_fasta(fasta_file):
    return AlignIO.read(fasta_file, "fasta")

def get_aa_differences(seq1, seq2):
    differences = []
    for i, (aa1, aa2) in enumerate(zip(seq1, seq2)):
        if aa1 != aa2:
            differences.append((i + 1, aa1, aa2))
    return differences

def reconstruct_ancestral_sequences(tree, alignment):
    for clade in tree.traverse("postorder"):
        if clade.is_leaf():
            clade.sequence = next((rec.seq for rec in alignment if rec.id == clade.name), None)
        else:
            clade.sequence = Seq("".join(
                max(set(aa), key=lambda x: (aa.count(x), x))
                for aa in zip(*[child.sequence for child in clade.children])
            ))

def simplify_label(label, count):
    parts = label.split('_')
    if len(parts) > count:
        shown = '_'.join(parts[:count])
        remaining = len(parts) - count
        return f"{shown}_+{remaining}more"
    return label

def label_tree_with_aa_changes(tree, alignment, simplify=False, simplify_label_count=2):
    print("Reconstructing ancestral sequences...")
    reconstruct_ancestral_sequences(tree, alignment)
    print("Labeling tree branches with amino acid changes...")
    for clade in tree.traverse("preorder"):
        if not clade.is_leaf() and len(clade.children) == 2:
            child1, child2 = clade.children
            changes = get_aa_differences(child1.sequence, child2.sequence)
            labels = []
            for pos, aa1, aa2 in changes:
                labels.append(f"{pos}{aa1}")
                labels.append(f"{pos}{aa2}")
            if labels:
                label1 = "_".join(labels[::2])
                label2 = "_".join(labels[1::2])
                if simplify:
                    label1 = simplify_label(label1, simplify_label_count)
                    label2 = simplify_label(label2, simplify_label_count)
                child1.add_feature("branch_label", label1)
                child2.add_feature("branch_label", label2)
                print(f"Labeling branches: {child1.name} with {label1}, {child2.name} with {label2}")
            else:
                print(f"No changes found for children {child1.name} and {child2.name}")
    return tree

def main(tree_file, msa_file, output_file, simplify_label_count):
    print("Parsing Newick tree...")
    tree = parse_newick(tree_file)
    print("Parsing multiple sequence alignment...")
    alignment = parse_fasta(msa_file)

    # Original labeled tree
    labeled_tree = label_tree_with_aa_changes(tree.copy(), alignment)
    labeled_tree.write(outfile=output_file, format=1, features=["branch_label"])
    print(f"Original labeled tree written to {output_file}")

    # Simplified labeled tree
    simplified_output = os.path.join(os.path.dirname(output_file), f"simplified_{os.path.basename(output_file)}")
    simplified_tree = label_tree_with_aa_changes(
        tree.copy(),
        alignment,
        simplify=True,
        simplify_label_count=simplify_label_count
    )
    simplified_tree.write(outfile=simplified_output, format=1, features=["branch_label"])
    print(f"Simplified labeled tree written to {simplified_output}")
    print("Thanks for using TreeBranchLabeller. Please cite Vezina, B., Morampalli, B.R., Nguyen, HA. et al. The rise and global spread of IMP carbapenemases (1996-2023): a genomic epidemiology study. Nat Commun (2025). https://doi.org/10.1038/s41467-025-66874-7")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Label phylogenetic tree with amino acid changes")
    parser.add_argument("-t", "--tree", required=True, help="Input Newick tree file")
    parser.add_argument("-m", "--msa", required=True, help="Input multiple sequence alignment file (FASTA format)")
    parser.add_argument("-o", "--output", default="labeled_tree.newick", help="Output Newick tree file")
    parser.add_argument("-s", "--simplify_label_count", type=int, default=2,
                        help="Number of amino acid changes to show before summarizing with '+nmore' (used in simplified tree)")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    main(args.tree, args.msa, args.output, args.simplify_label_count)

    # Call R script AFTER main() to generate plots
    subprocess.run([
        "Rscript",
        r_script_path,
        args.output,
        str(args.simplify_label_count)
    ])


# Author - Ben Vezina, https://orcid.org/0000-0003-4224-2537, https://scholar.google.com.au/citations?user=Rf9oh94AAAAJ&hl=en&oi=ao
