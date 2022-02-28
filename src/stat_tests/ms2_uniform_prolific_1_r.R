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
data_preprocessed <- read_excel("../../data/ms2_uniform_prolific_1_data/preprocessed_prolific.xlsx")

# data by subject
data_by_subject <- data_preprocessed %>%
  group_by(numerosity, participant, protectzonetype, perceptpairs, winsize) %>%
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))

# samplesize = 5 (each condition 5 displays)
data_by_subject <- data_by_subject %>%
  mutate(devoatopm_socre_SEM = deviation_score_std / sqrt(5),
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
# dv <- "deviation_score_mean"
dv <- "percent_change_mean"

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



# LMM ---------------------------------------------------------------------

# ID as factor
str(my_data)

my_data$perceptpairs <- as.factor(my_data$perceptpairs)
my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$numerosity <- as.factor(my_data$numerosity)
my_data$participant <- as.factor(my_data$participant)


alignment_con.model1 <-
  lmer(
    deviation_score_mean ~ protectzonetype +
      perceptpairs +
      (1 | participant) +
      (1 | numerosity),
    data = my_data,
    REML = FALSE
  )
alignment_con.model1


alignment_con.null1 <-
  lmer(
    deviation_score_mean ~ perceptpairs +
      (1 | participant) +
      (1 | numerosity),
    data = my_data,
    REML = FALSE
  )
alignment_con.null1


anova(alignment_con.model1, alignment_con.null1)

# check interaction: no interaction
alignment_con.interaction <-
  lmer(
    deviation_score_mean ~ protectzonetype * perceptpairs +
      (1 | participant) +
      (1 | numerosity),
    data = my_data,
    REML = FALSE
  )

anova(alignment_con.interaction, alignment_con.model1)

# random slope vs. random intercepts

coef(alignment_con.model1)

alignment_con.model_random_slope <-
  lmer(
    deviation_score_mean ~ protectzonetype + perceptpairs + numerosity +
      (1 + protectzonetype|participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.model_random_slope


coef(alignment_con.model_random_slope)

alignment_con.null_random_slope <-
  lmer(
    deviation_score_mean ~ perceptpairs + numerosity +
      (1 + protectzonetype |
         participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.null_random_slope


anova(alignment_con.model_random_slope, 
      alignment_con.null_random_slope)



# try: numerosity not as random effect

alignment_con.model2 <-
  lmer(
    deviation_score_mean ~ protectzonetype +
      perceptpairs +
      numerosity +
      (1 + protectzonetype | participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.model2


coef(alignment_con.model)

alignment_con.null2 <-
  lmer(
    deviation_score_mean ~ perceptpairs +
      numerosity +
      (1 + protectzonetype | participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.null2

anova(alignment_con.model2, alignment_con.null2)




# fix effect r2

r.squaredGLMM(alignment_con.model_random_slope)
# https://www.rdocumentation.org/packages/r2glmm/versions/0.1.2/topics/r2beta
# https://stats.stackexchange.com/questions/453758/differences-in-proportion-of-variance-explained-by-mumin-and-r2glmm-packages-usi
# r2beta may have error

# model R2
r2beta(alignment_con.model_random_slope, method = 'kr', partial = TRUE)

# an APA style table: https://cran.r-project.org/web/packages/sjPlot/vignettes/tab_mixed.html
tab_model(alignment_con.model_random_slope, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)

# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans_res <- emmeans(
  alignment_con.model_random_slope,
  list(pairwise ~ protectzonetype * numerosity * perceptpairs),
  adjust = "tukey"
)


# troditional ANOVA


# read data

# ANOVA
data_anova <-
  read_excel(
    "../../data/ms2_uniform_prolific_1_data/prolifc_data_combine_cluster_each_pp.xlsx"
  )
data_anova <- subset(data_anova, winsize == 0.6)

res.anova <-
  aov(
    mean_deviation_score ~ numerosity + protectzonetype + numerosity:protectzonetype,
    data = data_anova
  )
Anova(res.anova, type = "III")


res.mol1 <-
  lmer(mean_deviation_score ~ percent_triplets +
         protectzonetype + (1 | participant),
       data = data_anova)
res.null <-
  lmer(mean_deviation_score ~ percent_triplets +
         (1 | participant),
       data = data_anova)
anova(res.null, res.mol1)

r.squaredGLMM(res.mol1)
r2beta(res.mol1, method = 'kr', partial = TRUE)
