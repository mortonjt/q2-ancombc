# q2-ANCOMBC
qiime2 plugin for ANCOMBC

# Installation

First install ANCOMBC locally in R via
```
if (!requireNamespace("BiocManager", quietly=TRUE))
    install.packages("BiocManager")
BiocManager::install("ANCOMBC")
install.packages('tidyverse')
```

Then install the qiime2 plugin via
```
pip install git+https://github.com/mortonjt/q2-ancombc.git
qiime dev refresh-cache
```
