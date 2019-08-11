# Scater file but for taking a whole folder of data files 

# Import required packages 
if (!require(scater)) BiocManager::install("scater")
library(scater)
library(tools)
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
if (!require(scater)) install.packages('Seurat')
library(Seurat)
if (!require(phantasus)) BiocManager::install("phantasus")
library(phantasus)
if (!require(scran)) BiocManager::install("scran")
library(scran)

# take in information regarding the directory path and output text file
args = commandArgs(trailingOnly=TRUE)

###################
###################
####################
###################
# # Test Arguments
args[1] <- "stemformatics"
args[2] <- "output.csv"

#Check if there are enough command line arguments
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "out_multiple.txt"
} else if (length(args) > 2) {
  stop("You only need 2 arguments. Input file and output file")
}

# Create a list of documents in the directory 
input_directory <- args[1]
files_in_folder <- list.files(input_directory)


# Create the output data structure
output_labels <- c("total_features_by_counts", "total_counts", 
                   "pct_counts_in_top_50_features", "pct_counts_in_top_100_features", 
                   "pct_counts_in_top_200_features", "pct_counts_in_top_500_features")

output_data.frame <- data.frame(matrix(ncol = length(output_labels), nrow = 0))
colnames(output_data.frame) <- output_labels

# View(output_data.frame)

# Define function for generating quality score of files
quality_variables <- function(sc_filename) {
  
  # #REMEMBER TO UNDO
  # #######
  # #############
  # ###################
  # ##################
  # sc_filename <- "Stemformatics_dataset6580.gct"
  
  sc_filename_path <- paste(input_directory,"/", sc_filename, sep = "")
  # Change reading method based on file type 
  file.extention <- file_ext(sc_filename_path)
  if (file.extention == "csv") {
    stemformatics_data <- read.csv(sc_filename_path)
    # View(stemformatics_data)
  } else if(file.extention == "tsv") {
    stemformatics_data <- read.table(sc_filename_path)
  } else if(file.extention == "gct") {
    print(".gct file")
    intermediary <- read.gct(sc_filename_path)
    stemformatics_data <- intermediary@assayData$exprs
  } else {
    stop("The correct file type was not found")
  }
  
  # Change matrix into a single cell experiment
  test_sce <- SingleCellExperiment(assays = list(counts = t(stemformatics_data)))
  test_sce <- calculateQCMetrics(test_sce)
  
  
  # View(colData(test_sce))
  quality_matrix <- colData(test_sce)
  # View(quality_matrix@listData)
  quality_data.frame <- as.data.frame(colData(test_sce))
  # quality_data.frame[1,]
  quality_data.frame[is.na(quality_data.frame)] <- 0
  # View(quality_data.frame)
  
  interesting_columns <- c(2, 4, 6, 7, 8, 9)
  interesting_quality <- quality_data.frame[,interesting_columns]

  mean_quality.table <- as.table(colMeans(interesting_quality))
  mean_quality.vector <- as.data.frame(colMeans(interesting_quality))
  # View(mean_quality.vector)
  # View(mean_quality.dataframe)
  
  
  #Implement Seurat
  # test_sce$total_counts
  stemformatics_seurat <- CreateSeuratObject(counts = stemformatics_data, project = "stem")
  stemformatics_seurat[["percent.mt"]] <- PercentageFeatureSet(stemformatics_seurat, pattern = "^MT-")
  #Create seurat indicators 
  mt_genes <- mean(stemformatics_seurat$percent.mt)
  sd_genes <- sd(stemformatics_seurat$nFeature_RNA)
  # Add indicators to larger data table
  mean_quality.vector <- rbind(mean_quality.vector, mt_genes)
  mean_quality.vector <- rbind(mean_quality.vector, sd_genes)
  rownames(mean_quality.vector)[7:8] <- c("mt_genes", "sd_genes")
  
  return(mean_quality.vector)
}


# run the function for every file in the directory

for (data_file in files_in_folder) {
  print(data_file)
  output_row <- quality_variables(data_file)
  # Use the output of the function to create extra rows in a table
  output_data.frame <- rbind(t(output_row), output_data.frame, row.names = FALSE)
}

# Return the output dataframe
write.csv(output_data.frame, args[2], row.names = FALSE)

