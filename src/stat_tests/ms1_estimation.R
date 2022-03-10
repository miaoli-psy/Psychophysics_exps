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
library(multcomp)
library(nlme)
library(r2glmm)
library(dplyr)
library(TOSTER)
library(BayesFactor)
library(pwr)
library(writexl)
library(ggthemes)
# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
data_preprocessed <- read_excel("../../data/exp1_rerun_data/cleanedTotalData_fullinfo_v3.xlsx")

data_preprocessed_encircle <- read_excel("../../data/ms1_encircle/ms1_encircle_data.xlsx")

# data by display
data_by_display <- data_preprocessed %>%
  group_by(N_disk, crowdingcons, winsize) %>%
  summarise(estimation_mean = mean(response),
            estiamtion_std = sd(response))

data_encircle <- data_preprocessed_encircle %>% 
  group_by(numerosity, crowdingcons) %>% 
  summarise(grouping_num_mean = mean(average_group))

write_xlsx(data_by_display,"1.xlsx")

data_combine <- read_excel("../../data/ms1_encircle/ms1_encircle_corr.xlsx")

# visualization -----------------------------------------------------------

data_radial <- subset(data_combine, winsize == 0.7 & crowdingcons == 1)
data_tangential <- subset(data_combine, winsize == 0.3 & crowdingcons == 0)

my_plot <- ggscatter(data_combine, x = "estimation_mean",
            y = "grouping_num_mean",
            add = "reg.line",
            conf.int = TRUE,
            cor.coef = TRUE,
            cor.method = "pearson",
            xlab = "x",
            ylab = "y")



my_plot <- ggplot() +
  
  geom_point(
    data = data_combine,
    aes(
      x = grouping_num_mean,
      y = estimation_mean,
      color = as.factor(crowdingcons))
  ) +
  geom_smooth(
    data = data_combine,
    aes(
      x = grouping_num_mean,
      y = estimation_mean,
      color = as.factor(crowdingcons)),
    
    method = lm,
    se = FALSE,
    fullrange = TRUE,
    linetype = "dashed") +

  
  scale_color_manual(values = c("#4169e1", "#ff4500")) +
  

  
  theme_few() +
  
  facet_wrap( ~ winsize)

print(my_plot)
             