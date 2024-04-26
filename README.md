**This plugin has been replaced with functionality in the [`q2-composition`](https://github.com/qiime2/q2-composition) plugin.
You should now access ANCOM-BC in QIIME 2 through the q2-composition plugin that is included in the QIIME 2 `amplicon` distribution.
You do not need to install this plugin to use ANCOM-BC through QIIME 2.**

As of February 2024, you can find instructions for using ANCOM-BC in QIIME 2 in the [*Moving Pictures* tutorial](https://docs.qiime2.org/2024.2/tutorials/moving-pictures/#differential-abundance-testing-with-ancom-bc).


The original README text for this repository follows.
---

# q2-ANCOMBC

# Installation

Make sure you have qiime2 installed according to the [installation instruction](). Once you have the conda enviroment activated, open R by running

```bash
R
```

This will open the R prompt window in the terminal. R libraries installed in the terminal within your conda enviroment are the only ones qiime2 will see; if you wish to install ancombc in R studio or something similar, you will need to redo the installation there.

In the R terminal, install ANCOMBC locally:

```R
if (!requireNamespace("BiocManager", quietly=TRUE))
    install.packages("BiocManager")
BiocManager::install("ANCOMBC")
install.packages('tidyverse')
```

Then install the qiime2 plugin via

```bash
pip install git+https://github.com/mortonjt/q2-ancombc.git
qiime dev refresh-cache
```

If you run the command,

```bash
qiime
```

you should see `ancombc` listed in the avaliable plugins.

# Getting started

You can try running ANCOM-BC using the tutorial data in this repository. Start by making a tutorial directory and downloading the tutorial dataset:

```bash
mkdir ancom-bc-tutorial
cd ancom-bc-tutorial

# Downloads the files
wget https://github.com/mortonjt/q2-ancombc/raw/main/example_data/table.qza
wget https://github.com/mortonjt/q2-ancombc/raw/main/example_data/taxonomy.qza
wget https://raw.githubusercontent.com/mortonjt/q2-ancombc/main/example_data/metadata.txt
```

We can run ANCOM-BC using an R-style formula. In this case, we'll use the "labels" column:

```bash
qiime ancombc ancombc \
    --i-table table.qza \
    --m-metadata-file metadata.txt \
    --p-formula "labels" \
    --o-differentials differentials.qza

```

This will output a single results file, `differentials.qza`, which contains the parameters and p-value. You can visualize this and the taxonomy results using qiime:

```bash
qiime metadata tabulate \
 --m-input-file differentials.qza \
 --m-input-file taxonomy.qza \
 --o-visualization differentials.qzv
```

In the output table, you will find 5 columns from ANCOM-BC: 

* `beta`: The coeffecient for the taxonomic feature. 
* `se`: The standard error for the coeffecient
* `W`: The test statistic, calculated as $\beta/se$
* `p_val`: The p-value; p-value comes from a two-sided z-test using the W test statistics
* `q_val`: The adjusted p-value after multiple hypothsis correction.

If you included the taxonomy artifact, you will find an additional 2:

* `Taxon`: The taxonomic identifier for the features. 
* `Confidence`: How confident the classifier was with the taxonomic assignment. Most 

# Citation

Lin, H. and Peddada, S.D. (2020) "Analysis of compositions of microbiomes with bias correction." *Nature Communications* **11**: 3514. doi: 10.1038/s41467-020-17041-7

# Credits

These docs draw heavily off the documentation from the R repository by Frederick Huang Lin. 
