# Testing


```
qiime ancombc ancombc --i-table data/table.qza \
                      --i-taxonomy data/taxonomy.qza \
                      --m-metadata-file data/metadata.txt \
                      --p-formula "labels" \
                      --output-dir results
```
