# TreeBranchLabeller
Annotates tree branches for visualisation of multiple sequence alignments etc.



# Installation

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

# Quick start
```bash

```



4. Inside R terminal, install R libraries
```R
install.packages(c("ggplot2", "BiocManager"))
BiocManager::install("treeio")
BiocManager::install("ggtree")
```


# Requirements and dependancies

- python==3.11
- biopython==1.85
- ete3==3.1.3
- R version 4.5.0
- R libraries
  - ggplot2
  - treeio
  - ggtree

