#!/usr/bin/env Rscript
# load arguments ---------------------------------------------------------
cat(R.version$version.string, "\n")
args <- commandArgs(TRUE)

inp.abundances.path    <- args[[1]]
inp.metadata.path      <- args[[2]]
formula                <- args[[3]]
p_adj_method           <- args[[4]]
zero_cut               <- as.numeric(args[[5]])
lib_cut                <- as.numeric(args[[6]])
group                  <- args[[7]]
struc_zero             <- as.logical(args[[8]])
neg_lb                 <- as.logical(args[[9]])
tol                    <- as.numeric(args[[10]])
max_iter               <- as.numeric(args[[11]])
conserve               <- as.logical(args[[12]])
alpha                  <- as.numeric(args[[13]])
global                 <- as.logical(args[[14]])
output                 <- args[[15]]
# load libraries ----------------------------------------------------------
suppressWarnings(library(phyloseq))
suppressWarnings(library(tidyverse))
suppressWarnings(library(ANCOMBC))

# load data ---------------------------------------------------------------
otu.file  <- t(read.delim(inp.abundances.path, check.names=FALSE, row.names=1))
metadata.file <- read.delim(inp.metadata.path, check.names=FALSE, row.names=1)
OTU <- otu_table(otu.file, taxa_are_rows = TRUE)
MD <- sample_data(metadata.file)
row.names(MD) <- rownames(metadata.file)
data <- phyloseq(OTU, MD)
# analysis ----------------------------------------------------------------
fit = ancombc(data, formula, p_adj_method)
              # zero_cut, lib_cut, group, struc_zero, neg_lb,
              # tol, max_iter, conserve, alpha, global)

# extracts multivariate regression coeffecients form the structure 
beta <- fit$res$beta				# beta 
se <- fit$res$se 					# standard error
w <- fit$res$W 						# Test statistic
p_val <- fit$res$p_val 				# p-value
q_val <- fit$res$q_val 				# fdr p-value
# diff_abund <- fit$res$diff_abund 	# boolean for differential abundance

# Adds a descriptor to the columns the values associated with the columns
colnames(beta) <- modify(colnames(beta), 
	function(x){return(paste(x, 'beta', sep='_'))})
colnames(se) <- modify(colnames(se), 
	function(x){return(paste(x, 'se', sep='_'))})
colnames(w) <- modify(colnames(w), 
	function(x){return(paste(x, 'W', sep='_'))})
colnames(p_val) <- modify(colnames(p_val), 
	function(x){return(paste(x, 'p-value', sep='_'))})
colnames(q_val) <- modify(colnames(q_val), 
	function(x){return(paste(x, 'q-value', sep='_'))})

# Concatenates everything into a distance matrix
diffs <- as.data.frame(cbind(beta, se, w, p_val, q_val))
# cat(diffs)


# print(paste("global_test", fit$res_global, "\n"))
write.csv(diffs, file=output)
