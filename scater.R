#if (!requireNamespace("BiocManager", quietly = TRUE))
#    install.packages("BiocManager")

#BiocManager::install("scater")
# Take in command line arguments 
args = commandArgs(trailingOnly=TRUE)

#Check if there are enough command line arguments
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "out.txt"
} else if (length(args) > 2) {
  stop("You only need 2 arguments. Input file and output file")
}

stemformatics_data <- read.table(args[1])

library(scater)
# stemformatics_data <- read.table("imac_atlas_expression_v7.1.tsv")

test_sce <- SingleCellExperiment(assays = list(counts = t(stemformatics_data)))
test_sce <- calculateQCMetrics(test_sce)
colnames(colData(test_sce))
colData(test_sce)
# View(colData(test_sce))

colData(test_sce)


quality_matrix <- colData(test_sce)
quality_data.frame <- as.data.frame(colData(test_sce))
quality_data.frame[1,]
# View(quality_data.frame)


interesting_columns <- c(2, 4, 5, 6, 7, 8)
interesting_quality <- quality_data.frame[,interesting_columns]
# View(quality_mens)

mean_quality.table <- as.table(colMeans(quality_mens))
mean_quality.vector <- as.vector(mean_quality)
# View(mean_quality.vector)
# View(mean_quality.dataframe)
args[2] <- "output.txt"
write.table(mean_quality.table, file=args[2], row.names=FALSE)