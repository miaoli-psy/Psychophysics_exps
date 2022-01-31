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
# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
all_data <- read_excel("../../data/ms1_encircle/ms1_encircle_data.xlsx")
all_data_by_num <- read_excel("../../data/ms1_encircle/ms1_encircle_by_num.xlsx")

# change col name
colnames(all_data_by_num)[which(names(all_data_by_num) == "mean")] <- "average_group"
# visualization -----------------------------------------------------------

plot <- ggboxplot(all_data,
                  x = "numerosity",
                  y = "average_group",
                  color = "crowdingcons") +
  facet_wrap( ~ winsize, scale = "free_x")

print(plot)

# as factor

all_data$crowdingcons <- as.factor(all_data$crowdingcons)
all_data$numerosity <- as.factor(all_data$numerosity)
all_data$winsize <- as.factor(all_data$winsize)

# anova the effect of winsize/numerosity and alignment condition on averge_group

eff <- lmer(average_group ~ winsize * crowdingcons + (1|list_index), data = all_data)
anova(eff)

qqnorm(resid(eff))




