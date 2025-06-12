# Get command-line arguments
args <- commandArgs(trailingOnly = TRUE)

# Expecting: 1) NHX file path, 2) simplify_label_count
if (length(args) < 2) {
  stop("Usage: Rscript TreeBranchLabeller_plot.R <input_tree.nhx> <simplify_label_count>")
}

input_nhx_file <- args[1]
simplify_label_count <- as.integer(args[2])

# Make sure dependancies are installed
required_packages <- c("ggplot2", "treeio", "ggtree")
missing <- required_packages[!sapply(required_packages, requireNamespace, quietly=TRUE)]
if (length(missing) > 0) {
  stop("Missing required R packages: ", paste(missing, collapse=", "), "\nPlease install before running this script.")
}

# Load the annotated NHX
print("Reading input nhx file...")
tree_step_1 <- treeio::read.nhx(input_nhx_file)

# Get header names by converting to df
nhx_msa_table <- tidyr::as_tibble(tree_step_1)

# Plot tree with branch labels in ggtree
print("Plotting tree...")
tree_step_2 <- ggtree::ggtree(tree_step_1, layout = "rectangular", branch.length = "none") +
  ggtree::geom_label(ggplot2::aes(x = branch, label = branch_label), fill="grey90", fontface = "bold", family = "mono", size = 3, alpha = 0.8, na.rm = TRUE) +
  ggtree::geom_tiplab(ggplot2::aes(label = label), size = 3.5) +
  ggtree::theme_tree()

## Calculate relative position for scale bar

# Extract data
tree_data <- tree_step_2$data
x_min <- min(tree_data$x, na.rm = TRUE)
x_max <- max(tree_data$x, na.rm = TRUE)
y_min <- min(tree_data$y, na.rm = TRUE)
y_max <- max(tree_data$y, na.rm = TRUE)

# Calculate proportional positions
x_pos <- x_min + 0.1 * (x_max - x_min)  # 10% from the left
y_pos <- y_min + 0.9 * (y_max - y_min)  # 90% up

# Add scale bar to tree
print("Adding scale bar to tree...")
tree_step_3 <- tree_step_2 + ggtree::geom_treescale(x = x_pos, y = y_pos)

# Function to modify labels
modify_labels <- function(label, simplify_label = 2) {
  # If the label already contains "+", assume it's already simplified
  if (grepl("\\+\\s*\\d+\\s*more", label)) {
    return(label)
  }
  
  # Replace underscores with commas
  label <- gsub("_", ",", label)
  
  # Split the label into components
  parts <- unlist(strsplit(label, ","))
  
  # Simplify if needed
  if (length(parts) > simplify_label) {
    kept <- parts[1:simplify_label]
    n_more <- length(parts) - simplify_label
    new_label <- paste0(paste(kept, collapse = ","), ",+ ", n_more, " more")
  } else {
    new_label <- paste(parts, collapse = ",")
  }
  
  return(new_label)
}

tree_step_4 <- tree_step_3

# Modify labels in the tree
print("Simplifying tree branch labels...")
tree_step_4$data$branch_label <- sapply(
  tree_step_4$data$branch_label,
  modify_labels,
  simplify_label = simplify_label_count
)

## Save outputs

# Generate output file path based on input NHX file
output_png_file <- file.path(
  dirname(input_nhx_file), 
  paste0("simplified_", basename(sub("\\.nhx$", ".png", input_nhx_file)))
)
output_pdf_file <- file.path(
  dirname(input_nhx_file), 
  paste0("simplified_", basename(sub("\\.nhx$", ".pdf", input_nhx_file)))
)

# Save the plots
print("Saving tree images as .png and .pdf...")
ggplot2::ggsave(output_png_file, tree_step_4, width = 15, height = 9)
ggplot2::ggsave(output_pdf_file, tree_step_4, width = 15, height = 9)
# ggplot2::ggsave(output_svg_file, plot = tree_step_4, device = svglite::svglite, width = 15, height = 9)

# Author - Ben Vezina, https://orcid.org/0000-0003-4224-2537, https://scholar.google.com.au/citations?user=Rf9oh94AAAAJ&hl=en&oi=ao
