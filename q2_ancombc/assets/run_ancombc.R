#!/usr/bin/env Rscript

# load arguments ---------------------------------------------------------
cat(R.version$version.string, "\n")

args <- commandArgs(TRUE)


inp.abundances.path    <- args[[1]]
inp.taxonomy.path      <- args[[2]]
inp.metadata.path      <- args[[3]]
formula                <- args[[4]]
p_adj_method           <- args[[5]]
zero_cut               <- as.numeric(args[[6]])
lib_cut                <- as.numeric(args[[7]])
group                  <- args[[8]]
struc_zero             <- as.logical(args[[9]])
neg_lb                 <- as.logical(args[[10]])
tol                    <- as.numeric(args[[11]])
max_iter               <- as.numeric(args[[12]])
conserve               <- as.logical(args[[13]])
alpha                  <- as.numeric(args[[14]])
global                 <- as.logical(args[[15]])
output                 <- args[[16]]
# load libraries ----------------------------------------------------------
suppressWarnings(library(phyloseq))
suppressWarnings(library(tidyverse))
suppressWarnings(library(ANCOMBC))

# load data ---------------------------------------------------------------
otu.file  <- t(read.delim(inp.abundances.path, check.names=FALSE, row.names=1))
metadata.file <- read.delim(inp.metadata.path, check.names=FALSE, row.names=1)
taxonomy.file <- read.delim(inp.taxonomy.path, check.names=FALSE, row.names=1)
OTU <- otu_table(otu.file, taxa_are_rows = TRUE)
TAX <- tax_table(taxonomy.file)
MD <- sample_data(metadata.file)
row.names(TAX) <- rownames(taxonomy.file) # wtf phyloseq...
data <- phyloseq(OTU, TAX, MD)
print(data)
# analysis ----------------------------------------------------------------
fit = ancombc(data, formula, p_adj_method,
              zero_cut, lib_cut, group, struc_zero, neg_lb,
              tol, max_iter, conserve, alpha, global)

sfit <- as.data.frame(fit)
print(paste("global_test", fit$res_global, "\n"))
write.csv(sfit$res, file=output)
