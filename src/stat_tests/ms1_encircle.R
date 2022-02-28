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
all_data <- read_excel("../../data/ms1_encircle/ms1_encircle_data.xlsx")
all_data_by_num <- read_excel("../../data/ms1_encircle/ms1_encircle_by_num.xlsx")

# change col name
colnames(all_data_by_num)[which(names(all_data_by_num) == "mean")] <- "average_group"
# visualization -----------------------------------------------------------

# number of groups - numerosity
plot1 <- ggboxplot(all_data,
                  x = "numerosity",
                  y = "average_group",
                  color = "crowdingcons") +
  facet_wrap( ~ winsize, scale = "free_x")

plot1

# number of inner groups (next to fixation) - numerosity

plot2 <- ggboxplot(all_data,
                    x = "numerosity",
                    y = "average_inner_group",
                    color = "crowdingcons") +
  facet_wrap( ~ winsize, scale = "free_x")

plot2

# discriptive -------------------------------------------------------------

summary <- all_data %>%
  group_by(winsize, crowdingcons) %>%
  summarize(
    mean = mean(average_group, na.rm = TRUE),
    std_dev = sd(average_group, na.rm = TRUE)
  )
summary


# as factor

all_data$crowdingcons <- as.factor(all_data$crowdingcons)
all_data$numerosity <- as.factor(all_data$numerosity)
all_data$winsize <- as.factor(all_data$winsize)
all_data$displayN <- as.factor(all_data$displayN)


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
bf = anovaBF(average_group ~ crowdingcons*winsize, 
             data = all_data,
             whichRandom = "displayN")

bf


# test BF anova on average inner group

bf = anovaBF(average_inner_group ~ crowdingcons*winsize, data = all_data, whichRandom = "displayN")

bf

