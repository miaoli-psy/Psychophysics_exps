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
library(ggplot2)
library(ggthemes)
library(svglite)
library(sjPlot)

# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
data_preprocessed <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2_preprocessed.xlsx")

# data by subject
data_by_subject <- data_preprocessed %>%
  group_by(numerosity, participant, protectzonetype, perceptpairs, winsize) %>%
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize = 5 (each condition 5 displays)
data_by_subject <- data_by_subject %>%
  mutate(deviation_socre_SEM = deviation_score_std / sqrt(5),
         percent_change_SEM = percent_change_std / sqrt(5))

# data across subject
data <- data_preprocessed %>% 
  group_by(numerosity, protectzonetype, perceptpairs, winsize) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))

# samplesize = 34 * 5 for winsize0.4; 32 * 5 for winsize 0.6
data <- data %>%
  mutate(
    deviation_score_SEM =
      case_when(
        winsize == 0.4 ~ deviation_score_std / sqrt(34 * 5),
        winsize == 0.6 ~ deviation_score_std / sqrt(32 * 5)
      ), 
    percent_change_SEM =
      case_when(
        winsize == 0.4 ~ percent_change_std / sqrt(34 * 5),
        winsize == 0.6 ~ percent_change_std / sqrt(32 * 5)
      )
  )


# separate groups
data_by_subject_ws04 <- subset(data_by_subject, winsize == 0.4)
data_by_subject_ws06 <- subset(data_by_subject, winsize == 0.6)

# TODO
my_data <- data_by_subject_ws04

summary(my_data)


# Visualization------------------------------------------------------

# TODO
dv <- "deviation_score_mean"
# dv <- "percent_change_mean"

# subject
bxp <- ggboxplot(data = data_by_subject,
                 x = "participant",
                 y = dv,
                 color = "protectzonetype") +
  facet_wrap( ~ winsize, nrow = 2, scale = "free_x")

print(bxp)

# clustering level
bxp2 <- ggboxplot(data = data_by_subject,
                  x = "perceptpairs",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, ncol = 2, scale = "free_x")

print(bxp2)

# numerosity

bxp3 <- ggboxplot(data = data_by_subject,
                  x = "numerosity",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, ncol = 2, scale = "free_x")

print(bxp3)


# result plots ------------------------------------------------------------
my_plot <-  ggplot() +
  
  geom_bar(data = data, aes(x = perceptpairs,
                                y = deviation_score_mean,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0, 0.25,0.5, 0.75, 1)) +
  
  # scale_y_continuous(limits = c(-5, 5)) +
  
  # each data point represents the average deviation of 1 participant
  # geom_point(data = data_by_subject, aes(x = perceptpairs,
  #                                         y = deviation_score_mean,
  #                                         group = protectzonetype,
  #                                         colour = protectzonetype),
  #            alpha = 0.2,
  #            position = position_dodge(0.2))+
  
  geom_errorbar(data = data, aes(x = perceptpairs,
                                     y = deviation_score_mean,
                                     ymin = deviation_score_mean - deviation_score_SEM,
                                     ymax = deviation_score_mean + deviation_score_SEM,
                                     group = protectzonetype),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(0.2)) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "percentage of disc pairs") +
  
  theme_few() +
  
  facet_wrap(~ numerosity, nrow = 2)


print(my_plot)

ggsave(
  file = "test.svg",
  plot = my_plot,
  width = 12,
  height = 5,
  dpi = 300
)


# data no clustering ------------------------------------------------------


# data by subject
data_by_subject2 <- data_preprocessed %>%
  group_by(numerosity, participant, protectzonetype, winsize) %>%
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize = 25 (each condition 5 displays * 5 clustering = 25)
data_by_subject2 <- data_by_subject2 %>%
  mutate(deviation_socre_SEM = deviation_score_std / sqrt(25),
         percent_change_SEM = percent_change_std / sqrt(25))


# data across subject
data2 <- data_preprocessed %>% 
  group_by(numerosity, protectzonetype, winsize) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize = 29 * 25 for winsize0.4; 27 * 25 for winsize 0.6

data2 <- data2 %>%
  mutate(
    deviation_score_SEM =
      case_when(
        winsize == 0.4 ~ deviation_score_std / sqrt(29 * 25),
        winsize == 0.6 ~ deviation_score_std / sqrt(27 * 25)
      ), 
    percent_change_SEM =
      case_when(
        winsize == 0.4 ~ percent_change_std / sqrt(29 * 25),
        winsize == 0.6 ~ percent_change_std / sqrt(27 * 25)
      )
  )


# separate groups
data_by_subject_ws04_2 <- subset(data_by_subject2, winsize == 0.4)
data_by_subject_ws06_2 <- subset(data_by_subject2, winsize == 0.6)

# TODO
my_data2 <- data_by_subject_ws04_2

summary(my_data2)


# result plots 2 ------------------------------------------------------------

x_breaks <- function(x){
  if (x < 50) {
    c(34, 36, 38, 40, 42, 44)
  } else{
    c(54, 56, 58, 60, 62, 64)
  }
}


my_plot2 <-  ggplot() +
  
  geom_bar(
    data = data2,
    aes(x = numerosity,
        y = deviation_score_mean,
        fill = protectzonetype),
    position = "dodge",
    stat = "identity",
    alpha = 0.5,
    width = 1.5
  ) +
  
  scale_x_continuous(breaks = x_breaks) +
  
  geom_errorbar(
    data = data2,
    aes(
      x = numerosity,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_score_SEM,
      ymax = deviation_score_mean + deviation_score_SEM,
      group = protectzonetype
    ),
    color = "black",
    size  = 1.2,
    width = .00,
    position = position_dodge(1.5)
  ) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "nuemrosity") +
  
  theme_few() +
  
  facet_wrap( ~ winsize, ncol = 2, scale = "free_x")


print(my_plot2)

ggsave(
  file = "test.svg",
  plot = my_plot2,
  width = 12,
  height = 5,
  dpi = 300
)

str(my_data2)

my_data2$protectzonetype <- as.factor(my_data2$protectzonetype)
my_data2$numerosity <- as.factor(my_data2$numerosity)
my_data2$participant <- as.factor(my_data2$participant)


# LMM without clustering as fix factor ------------------------------------

# numerosity as fix effect

alignment_con.model_random_slope3 <-
  lmer(
    deviation_score_mean ~ protectzonetype + numerosity +
      (1 + protectzonetype|participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.model_random_slope3


coef(alignment_con.model_random_slope3)

alignment_con.null_random_slope3 <-
  lmer(
    deviation_score_mean ~ numerosity +
      (1 + protectzonetype | participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.null_random_slope3


anova(alignment_con.model_random_slope3, 
      alignment_con.null_random_slope3)


r.squaredGLMM(alignment_con.model_random_slope3)

r2beta(alignment_con.model_random_slope3, method = 'kr', partial = TRUE)

tab_model(alignment_con.model_random_slope3, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)
# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans_res <- emmeans(
  alignment_con.model_random_slope3,
  list(pairwise ~ protectzonetype * numerosity),
  adjust = "tukey"
)
print(emmeans_res)

