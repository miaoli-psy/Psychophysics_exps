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
# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
all_data <- read_csv("../../data/ms1_encircle/preprocessed_encircle.csv")


# visualization -----------------------------------------------------------

# number of groups - numerosity
plot1 <- ggboxplot(all_data,
                  x = "numerosity",
                  y = "groups_n",
                  color = "crowdingcons") +
  facet_wrap( ~ winsize, scale = "free_x")


plot1

# number of inner groups (next to fixation) - numerosity

plot2 <- ggboxplot(all_data,
                    x = "numerosity",
                    y = "inner_groups_n",
                    color = "crowdingcons") +
  facet_wrap( ~ winsize, scale = "free_x")

plot2

# discriptive -------------------------------------------------------------

summary <- all_data %>%
  group_by(winsize, crowdingcons) %>%
  summarize(
    mean = mean(groups_n, na.rm = TRUE),
    std_dev = sd(groups_n, na.rm = TRUE)
  )
summary


# as factor

all_data$crowdingcons <- as.factor(all_data$crowdingcons)
all_data$numerosity <- as.factor(all_data$numerosity)
all_data$winsize <- as.factor(all_data$winsize)
all_data$displayN <- as.factor(all_data$displayN)
all_data$evaluation <- as.factor(all_data$evaluation)

str(all_data)
# zero effect -------------------------------------------------------------

# each winsize
data <- subset(all_data, winsize == 0.6)

BF <-
  ttestBF(formula = average_group ~ crowdingcons,
          data = data,
          rscale = 1) #rscale = 1, 1.5
BF

plot(BF)

# cal SESOI
SESOI <- pwr.t.test(n = 3, power = 1 / 3, type = "two.sample")
SESOI


# TOST
TOST <-
  dataTOSTtwo(
    data = data,
    deps = "average_group",
    group = "crowdingcons",
    var_equal = TRUE,
    low_eqbound = -1.62,
    high_eqbound = 1.62,
    desc = TRUE,
    plots = TRUE
  )
TOST

# test BF anova on average group
bf = anovaBF(groups_n ~ crowdingcons*winsize + evaluation, data = all_data, whichRandom = "evaluation")

bf







