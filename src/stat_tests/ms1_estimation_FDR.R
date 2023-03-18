# libraries
library(readxl)
library(tidyverse)
library(dplyr)
library(purrr)

# prepare -----------------------------------------------------------------

# set working path
setwd("c:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
data_preprocessed <- read_excel("../../data/exp1_rerun_data/cleanedTotalData_fullinfo_v3.xlsx")

# Replace 1 with "radial" and 0 with "tangential"
data_preprocessed$crowdingcons <- ifelse(data_preprocessed$crowdingcons == 1, "radial", "tangential")


grouped_data <- data_preprocessed %>%
  group_by(participant_N, crowdingcons, winsize) %>%
  summarize(mean_deviation = mean(deviation_score, na.rm = TRUE)) 

group_by_winsize <- grouped_data %>%
  group_by(winsize)

results <- group_by_winsize %>%
  summarize(
    t_test = t.test(mean_deviation ~ crowdingcons, paired = TRUE)$statistic,
    p_value = t.test(mean_deviation ~ crowdingcons, paired = TRUE)$p.value
  )

# FDR
adjusted_p <- p.adjust(results$p_value, method = "fdr")
results$p_adjusted <- adjusted_p

  
  
