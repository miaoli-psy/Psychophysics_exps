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
library(ppcor)


# pre ---------------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
data_corr <- read_excel("../../data/ms1_encircle/ms1_encircle_corr.xlsx")

# visualization -----------------------------------------------------------

my_plot <- ggplot() +
  
  geom_point(
    data = data_corr,
    aes(
      x = groups_mean,
      y = deviation_score_mean,
      color = crowdingcons),
    alpha = 0.8
  ) +
  # geom_smooth(
  #   data = data_corr,
  #   aes(
  #     x = mean,
  #     y = deviation_score_mean,
  #     color = crowdingcons),
  #   
  #   method = lm,
  #   se = FALSE,
  #   fullrange = TRUE,
  #   alpha = 0.5) +
  
  geom_line(
    data = data_corr,
    aes(
      x = groups_mean,
      y = deviation_score_mean,
      color = crowdingcons),
    stat = "smooth",
    method = "lm",
    formula = "y ~ x",
    size = 0.8,
    alpha = 0.8
    ) +
  
  scale_color_manual(values = c("#4f69af", "#ff4500")) +
  
  # scale_x_continuous(breaks = breaks_fun) + 
  
  theme_few() +
  
  facet_wrap( ~ winsize)

print(my_plot)

ggsave(file = "test.svg", plot = my_plot, width = 10, height = 7)

# correlations ------------------------------------------------------------

data_corr_to_test <- dplyr::select(data_corr, deviation_score_mean, numerosity, groups_mean, winsize, crowdingcons)

data_corr_to_test <- subset(data_corr_to_test, winsize == 0.3 & crowdingcons == "radial")
data_corr_to_test <- subset(crowdingcons == "radial")

str(data_corr_to_test)
res <-pcor.test(data_corr_to_test$groups_mean,
     data_corr_to_test$deviation_score_mean, 
     data_corr_to_test$numerosity)
str(res)

