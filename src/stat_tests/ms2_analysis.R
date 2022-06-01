# libraires ---------------------------------------------------------------
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

# Exp1 ===========================================================

# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
data_preprocessed <- read_excel("../../data/ms2_uniform_prolific_1_data/preprocessed_prolific.xlsx")

# check age, sex
data_by_subject <- data_preprocessed %>%
  group_by(participant, age, sex, winsize) %>%
  tally() 
  

df_win06 <-subset(data_by_subject, winsize == 0.6)
mean(df_win06$age)

# LMM ---------------------------------------------------------------------

# data by subject
data_by_subject2 <- data_preprocessed %>%
  group_by(numerosity,
           participant,
           protectzonetype,
           winsize) %>%
  summarise(
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )


# as factors
str(data_by_subject2)
data_by_subject2$protectzonetype <- as.factor(data_by_subject2$protectzonetype)
data_by_subject2$numerosity <- as.factor(data_by_subject2$numerosity)
data_by_subject2$participant <- as.factor(data_by_subject2$participant)


# separate groups - 2 experiments
data_by_subject_ws04_2 <- subset(data_by_subject2, winsize == 0.4)
data_by_subject_ws06_2 <- subset(data_by_subject2, winsize == 0.6)


# TODO
# Exp1a (small numerosity range)
# my_data2 <- data_by_subject_ws04_2

# Exp1b (large numerosity range)
my_data2 <- data_by_subject_ws06_2


# interaction effect

# full model with interaction
alignment_con.model_random_slope <-
  lmer(
    deviation_score_mean ~ protectzonetype * numerosity +
      (1 + protectzonetype | participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.model_random_slope


# reduced model without interaction
alignment_con.reduced_random_slope <-
  lmer(
    deviation_score_mean ~ numerosity + protectzonetype +
      (1 + protectzonetype | participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.reduced_random_slope


# likelihood ratio test
anova(alignment_con.model_random_slope, 
      alignment_con.reduced_random_slope)


# visualize the interaction (if exists)
emmip(alignment_con.model_random_slope, protectzonetype ~ numerosity)


# main effect of alignment condition and numerosity
alignment_con.null_random_slope3 <-
  lmer(
    deviation_score_mean ~ protectzonetype +
      (1 + protectzonetype | participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.null_random_slope3


anova(alignment_con.reduced_random_slope, 
      alignment_con.null_random_slope3)


# estimates
emms <- emmeans(
  alignment_con.reduced_random_slope,
  list(pairwise ~ numerosity*protectzonetype),
  adjust = "tukey"
)

summary(emms, infer = TRUE)



r.squaredGLMM(alignment_con.model_random_slope3)

r2beta(alignment_con.model_random_slope3, method = 'kr', partial = TRUE)

tab_model(alignment_con.model_random_slope3, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)

# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans(
  alignment_con.model_random_slope3,
  list(pairwise ~ protectzonetype * numerosity),
  adjust = "tukey"
)

summary(glht(alignment_con.model_random_slope3, linfct=mcp(numerosity ="Tukey")))

lsmeans(alignment_con.model_random_slope3, pairwise~protectzonetype*numerosity, adjust="tukey")


# Exp 2 ====================================================================

# read data
data_preprocessed <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2_preprocessed.xlsx")


# check age, sex
data_by_subject <- data_preprocessed %>%
  group_by(participant, age, sex, winsize) %>%
  tally() 


df_win06 <-subset(data_by_subject, winsize == 0.6)
mean(df_win06$age)


# data by subject
data_by_subject2 <- data_preprocessed %>%
  group_by(numerosity,
           participant,
           protectzonetype,
           winsize) %>%
  summarise(
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )

# separate groups
data_by_subject_ws04_2 <- subset(data_by_subject2, winsize == 0.4)
data_by_subject_ws06_2 <- subset(data_by_subject2, winsize == 0.6)

# TODO
my_data2 <- data_by_subject_ws06_2

summary(my_data2)


my_data2$protectzonetype <- as.factor(my_data2$protectzonetype)
my_data2$numerosity <- as.factor(my_data2$numerosity)
my_data2$participant <- as.factor(my_data2$participant)
my_data2$winsize <- as.factor(my_data2$winsize)


# interaction effect

# full model with interaction
alignment_con.model_random_slope <-
  lmer(
    deviation_score_mean ~ protectzonetype * numerosity +
      (1 + protectzonetype | participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.model_random_slope


# reduced model without interaction
alignment_con.reduced_random_slope <-
  lmer(
    deviation_score_mean ~ numerosity + protectzonetype +
      (1 + protectzonetype | participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.reduced_random_slope


# likelihood ratio test
anova(alignment_con.model_random_slope, 
      alignment_con.reduced_random_slope)


# visualize the interaction (if exists)
emmip(alignment_con.model_random_slope, protectzonetype ~ numerosity)


# main effect of alignment condition and numerosity
alignment_con.null_random_slope3 <-
  lmer(
    deviation_score_mean ~ protectzonetype +
      (1 + protectzonetype | participant),
    data = my_data2,
    REML = FALSE
  )
alignment_con.null_random_slope3


anova(alignment_con.reduced_random_slope, 
      alignment_con.null_random_slope3)


# estimates
emms <- emmeans(
  alignment_con.reduced_random_slope,
  list(pairwise ~ numerosity * protectzonetype),
  adjust = "tukey"
)

summary(emms, infer = TRUE)



r.squaredGLMM(alignment_con.model_random_slope3)

r2beta(alignment_con.model_random_slope3, method = 'kr', partial = TRUE)

tab_model(alignment_con.model_random_slope3, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)

summary(glht(alignment_con.model_random_slope3, linfct=mcp(protectzonetype ="Tukey")))
