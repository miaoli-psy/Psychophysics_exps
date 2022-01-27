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
all_data_each_pp <- read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_each_pp.xlsx")

# separate groups
all_data_small_num <- subset(all_data_each_pp, winsize == 0.4)
all_data_large_num <- subset(all_data_each_pp, winsize == 0.6)

# TODO
data <- all_data_small_num


# random factors ----------------------------------------------------------

# subject
bxp <- ggboxplot(data = all_data_each_pp, 
                 x = "participant", 
                 y = "mean_deviation_score", 
                 color = "protectzonetype") +
  facet_wrap(~ winsize, nrow = 2)

print(bxp)

# clustering level
bxp2 <- ggboxplot(data = all_data_each_pp, 
                  x = "percent_triplets", 
                  y = "mean_deviation_score", 
                  color = "protectzonetype") +
  facet_wrap(~ winsize, ncol = 2)

print(bxp2)

# numerosity

bxp3 <- ggboxplot(data = all_data_each_pp, 
                  x = "numerosity", 
                  y = "mean_deviation_score", 
                  color = "protectzonetype") +
  facet_wrap(~ winsize, nrow = 2, scales = "free")

print(bxp3)


# LMM ---------------------------------------------------------------------

# ID as factor
str(data)

data$percent_triplets <-as.factor(data$percent_triplets)
data$protectzonetype <-as.factor(data$protectzonetype)

alignment_con.model1 <- lmer(mean_deviation_score ~ protectzonetype + 
                               percent_triplets + 
                               (1|participant) + 
                               (1|numerosity), 
                             data = data, REML = FALSE)
alignment_con.model1


alignment_con.null1 <- lmer(mean_deviation_score ~ percent_triplets + 
                              (1|participant) + 
                              (1|numerosity), 
                            data = data, REML = FALSE)
alignment_con.null1


anova(alignment_con.model1, alignment_con.null1)

# check interaction: no interaction
alignment_con.interaction <- lmer(mean_deviation_score ~ protectzonetype * percent_triplets + 
                                    (1|participant) + 
                                    (1|numerosity), 
                                  data = data, REML = FALSE)

anova(alignment_con.interaction, alignment_con.model1)

# random slope vs. random intercepts

coef(alignment_con.model)

alignment_con.model_random_slope <- lmer(mean_deviation_score ~ protectzonetype + percent_triplets + 
                                           (1 + protectzonetype|participant) + 
                                           (1 + protectzonetype|numerosity), 
                                         data = data, REML = FALSE)
alignment_con.model_random_slope


coef(alignment_con.model)

alignment_con.null_random_slope <- lmer(mean_deviation_score ~ percent_triplets + 
                                          (1 + protectzonetype|participant) + 
                                          (1 + protectzonetype|numerosity), 
                                        data = data, REML = FALSE)
alignment_con.null_random_slope


anova(alignment_con.model_random_slope, alignment_con.null_random_slope)



# numerosity not as random effect

alignment_con.model2 <- lmer(mean_deviation_score ~ protectzonetype + 
                               percent_triplets + 
                               numerosity + 
                               (1+ protectzonetype|participant),
                             data = data, REML = FALSE)
alignment_con.model2


coef(alignment_con.model)

alignment_con.null2 <- lmer(mean_deviation_score ~ percent_triplets + 
                              numerosity +
                              (1+ protectzonetype|participant),
                            data = data, REML = FALSE)
alignment_con.null2 

anova(alignment_con.model2, alignment_con.null2)


# fix effect r2

r.squaredGLMM(alignment_con.model2)
# https://www.rdocumentation.org/packages/r2glmm/versions/0.1.2/topics/r2beta
# https://stats.stackexchange.com/questions/453758/differences-in-proportion-of-variance-explained-by-mumin-and-r2glmm-packages-usi
# r2beta may have error
r2beta(alignment_con.model, method = 'kr', partial = TRUE)

# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans(alignment_con.model, list(pairwise ~ protectzonetype * percent_triplets), adjust = "tukey")



# Troditional ANOVA -------------------------------------------------------

# mix anova winsize(2 between) * clustering(5 within) * type(2 within)
res.aov <- anova_test(
  data = all_data_combine_num_each_pp, dv = mean_deviation_score, wid = participant,
  between = winsize, within = c(percent_triplets, protectzonetype)
)
get_anova_table(res.aov)


# check if all fixed factors have been correctly identified as factor
str(data)
data$percent_triplets <-as.factor(data$percent_triplets)
data$protectzonetype <-as.factor(data$protectzonetype)

bxp2 <- ggboxplot(
  data, x = "percent_triplets", y = "mean_deviation_score", 
  color = "protectzonetype",
  palette = "joc",
  facet.by = "winsize",
  short.panel.labs = FALSE)

print(bxp2)


res.aov2 <- anova_test(
  data = data, dv = mean_deviation_score, wid = participant,
  within = c(percent_triplets, protectzonetype)
)
get_anova_table(res.aov2)

model1 <- lm(mean_deviation_score ~ percent_triplets + protectzonetype, data = data)
Anova(model1, type = "III")


# check model assumptions: failed, cannot do ANOVA

plot(model1, 2)
aov_residuals <- residuals(object = model1)
shapiro.test(aov_residuals)

# Start LMM

summary(data)

effect <- lmer(mean_deviation_score ~ as.factor(percent_triplets) * as.factor(protectzonetype) + (1|participant), data = data)
anova(effect)
eta_sq(effect, partial = TRUE)
r.squaredGLMM(effect) #adjust r2 for the model as an alternative

# post hocs for main effect
lsmeans(effect, pairwise~protectzonetype|percent_triplets, adjust="tukey")






