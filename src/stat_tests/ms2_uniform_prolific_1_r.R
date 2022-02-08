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
# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
all_data_each_pp <-
  read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_each_pp.xlsx")

# separate groups
all_data_small_num <- subset(all_data_each_pp, winsize == 0.4)
all_data_large_num <- subset(all_data_each_pp, winsize == 0.6)

# TODO
data <- all_data_large_num

summary(data)


# Visualization------------------------------------------------------

# subject
bxp <- ggboxplot(data = all_data_each_pp,
                 x = "participant",
                 y = "mean_deviation_score",
                 color = "protectzonetype") +
  facet_wrap( ~ winsize, nrow = 2)

print(bxp)

# clustering level
bxp2 <- ggboxplot(data = all_data_each_pp,
                  x = "percent_triplets",
                  y = "mean_deviation_score",
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, ncol = 2)

print(bxp2)

# numerosity

bxp3 <- ggboxplot(data = all_data_each_pp,
                  x = "numerosity",
                  y = "mean_deviation_score",
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, nrow = 2, scales = "free")

print(bxp3)


# LMM ---------------------------------------------------------------------

# ID as factor
str(data)

data$percent_triplets <- as.factor(data$percent_triplets)
data$protectzonetype <- as.factor(data$protectzonetype)
data$numerosity <- as.factor(data$numerosity)


alignment_con.model1 <-
  lmer(
    mean_deviation_score ~ protectzonetype +
      percent_triplets +
      (1 | participant) +
      (1 | numerosity),
    data = data,
    REML = FALSE
  )
alignment_con.model1


alignment_con.null1 <-
  lmer(
    mean_deviation_score ~ percent_triplets +
      (1 | participant) +
      (1 | numerosity),
    data = data,
    REML = FALSE
  )
alignment_con.null1


anova(alignment_con.model1, alignment_con.null1)

# check interaction: no interaction
alignment_con.interaction <-
  lmer(
    mean_deviation_score ~ protectzonetype * percent_triplets +
      (1 | participant) +
      (1 | numerosity),
    data = data,
    REML = FALSE
  )

anova(alignment_con.interaction, alignment_con.model1)

# random slope vs. random intercepts

coef(alignment_con.model)

alignment_con.model_random_slope <-
  lmer(
    mean_deviation_score ~ protectzonetype + percent_triplets +
      (1 + protectzonetype |
         participant) +
      (1 + protectzonetype |
         numerosity),
    data = data,
    REML = FALSE
  )
alignment_con.model_random_slope


coef(alignment_con.model)

alignment_con.null_random_slope <-
  lmer(
    mean_deviation_score ~ percent_triplets +
      (1 + protectzonetype |
         participant) +
      (1 + protectzonetype |
         numerosity),
    data = data,
    REML = FALSE
  )
alignment_con.null_random_slope


anova(alignment_con.model_random_slope,
      alignment_con.null_random_slope)



# numerosity not as random effect

alignment_con.model2 <-
  lmer(
    mean_deviation_score ~ protectzonetype +
      percent_triplets +
      numerosity +
      (1 + protectzonetype | participant),
    data = data,
    REML = FALSE
  )
alignment_con.model2


coef(alignment_con.model)

alignment_con.null2 <-
  lmer(
    mean_deviation_score ~ percent_triplets +
      numerosity +
      (1 + protectzonetype | participant),
    data = data,
    REML = FALSE
  )
alignment_con.null2

anova(alignment_con.model2, alignment_con.null2)



alignment_con.model4 <-
  lmer(
    mean_deviation_score ~ protectzonetype +
      numerosity +
      percent_triplets +
      (1 + protectzonetype | participant),
    data = data,
    REML = FALSE
  )
alignment_con.model4


alignment_con.null4 <-
  lmer(
    mean_deviation_score ~ percent_triplets +
      numerosity +
      (1 + protectzonetype | participant),
    data = data,
    REML = FALSE
  )
alignment_con.null4

anova(alignment_con.model4, alignment_con.null4)


# fix effect r2

r.squaredGLMM(alignment_con.model4)
# https://www.rdocumentation.org/packages/r2glmm/versions/0.1.2/topics/r2beta
# https://stats.stackexchange.com/questions/453758/differences-in-proportion-of-variance-explained-by-mumin-and-r2glmm-packages-usi
# r2beta may have error

# model R2
r2beta(alignment_con.model4, method = 'kr', partial = TRUE)

# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans(
  alignment_con.model_random_slope,
  list(pairwise ~ protectzonetype * percent_triplets),
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
