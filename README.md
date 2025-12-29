# TreeBranchLabeller
Annotates tree branches for visualisation of multiple sequence alignments etc. Outputs branch-labelled .nxh files, since newick trees cannot label branches. 
In the following image, I have highlighted the key residue changes between blaIMP variants, resulting in branch divergences.

![simplified_labeled_tree](https://github.com/user-attachments/assets/3bc2dac8-d1bf-49ef-aea8-b6a31ed14505)

## Quick start
```bash
# Activate environment
conda activate TreeBranchLabeller_v1.0.0

# Output branch labelled tree with up to n=4 features per branch
python TreeBranchLabeller.py \
  --tree test_data/input/input_tree.nwk \
  --msa test_data/input/input_alignment.fasta \
  --output branch_labeled_tree.nhx \
  --simplify_label_count 4
```

## Input and outputs
- Input files:
  - Any tree (.newick)
  - Alignment file (.fasta)
- Outputs:
  - A .nhx output tree with labelled branches. Can be visualised in any way you see fit
  - A simplified .nhx output tree with n labelled branches. Can be visualised in any way you see fit
  - Visualised .png tree constructed in R
  - Visualised .pdf tree constructed in R

## Options

-`h`, `--help`                     Shows help message

-`t`, `--tree`                     Input Newick tree file

-`m`, `--msa`                      Input multiple sequence alignment file (FASTA format)

-`o`, `--output`                   Output base filename

-`s`, `--simplify_label_count`     Number of amino acid changes to show before summarizing with '+nmore' (used in simplified tree)

`--version`                        Show version number

## Installation

1. Clone repo
```bash
git clone https://github.com/bananabenana/TreeBranchLabeller.git
cd TreeBranchLabeller
```
2. Install python deps
```bash
conda env create -y -f TreeBranchLabeller_conda_env.yml
```
3. Install R
```bash
# R installation
sudo apt update
sudo apt install --no-install-recommends software-properties-common dirmngr
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt install --no-install-recommends r-base
R
```
4. Inside R terminal, install R libraries
```R
install.packages(c("ggplot2", "BiocManager"))
BiocManager::install("treeio")
BiocManager::install("ggtree")
quit()
```
5. Test
```bash
conda activate TreeBranchLabeller_v1.0.0
python TreeBranchLabeller.py -h
```

## Requirements and dependancies

- python==3.11
- biopython==1.85
- ete3==3.1.3
- R version 4.5.0
- R libraries
  - ggplot2
  - treeio
  - ggtree

## Citation
Please cite: Vezina, B., Morampalli, B.R., Nguyen, HA. et al. The rise and global spread of IMP carbapenemases (1996-2023): a genomic epidemiology study. Nat Commun (2025). https://doi.org/10.1038/s41467-025-66874-7


## Author
- Ben Vezina
  - ORCID: https://orcid.org/0000-0003-4224-2537
  - Google Scholar: https://scholar.google.com.au/citations?user=Rf9oh94AAAAJ&hl=en&oi=ao

