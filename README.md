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

# Getting started
To make sure that everything working correctly, run
```
qiime ancombc ancombc \
    --i-table example_data/table.qza \
    --i-taxonomy example_data/taxonomy.qza \
    --m-metadata-file example_data/metadata.txt \
    --p-formula "labels" \
    --output-dir results

```
