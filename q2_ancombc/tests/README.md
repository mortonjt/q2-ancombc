# Testing


```
qiime ancombc ancombc --i-table data/table.qza \
                      --i-taxonomy data/taxonomy.qza \
                      --m-metadata-file data/metadata.txt \
                      --p-formula "labels" \
                      --output-dir results
```

To specifically test the Rscript run
```
run_ancombc.R Rdata/input.biom.tsv Rdata/taxonomy.tsv Rdata/input.map.txt labels holm 0.9 1000 nation TRUE TRUE 1e-05 100 TRUE 0.05 TRUE output.summary.txt
```
