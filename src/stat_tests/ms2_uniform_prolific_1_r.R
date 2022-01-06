# libraries
library(readxl)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(emmeans)
library(sjstats)
library(lme4)
library(lmerTest)
library(MuMIn)

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")



all_data_combine_num_each_pp <- read_excel("../../data/prolific_direct_estimate/prolifc_data_combine_num_each_pp.xlsx")


bxp <- ggboxplot(
  all_data_combine_num_each_pp, x = "percent_triplets", y = "mean_deviation_score",
  color = "protectzonetype", 
  palette = "jco",
  facet.by = "winsize",
  short.panel.labs = FALSE
)
bxp

# mix anova winsize(2 between) * clustering(5 within) * type(2 within)
res.aov <- anova_test(
  data = all_data_combine_num_each_pp, dv = mean_deviation_score, wid = participant,
  between = winsize, within = c(percent_triplets, protectzonetype)
)
get_anova_table(res.aov)