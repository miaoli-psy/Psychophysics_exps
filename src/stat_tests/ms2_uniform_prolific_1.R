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
library(mixedpower)
# prepare -----------------------------------------------------------------

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/stat_tests/")

# read data
data_preprocessed <- read_excel("../../data/ms2_uniform_prolific_1_data/preprocessed_prolific.xlsx")

# separate groups
data_ws04 <- subset(data_preprocessed, winsize == 0.4)
data_ws06 <- subset(data_preprocessed, winsize == 0.6)

# TODO
my_data <- data_ws04


# Visualization------------------------------------------------------

# TODO
dv <- "deviation_score"

# subject
bxp <- ggboxplot(data = my_data,
                 x = "participant",
                 y = dv,
                 color = "protectzonetype") +
  facet_wrap( ~ winsize, nrow = 2, scale = "free_x")

print(bxp)

# clustering level
bxp2 <- ggboxplot(data = my_data,
                  x = "perceptpairs",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, ncol = 2, scale = "free_x")

print(bxp2)

# numerosity

bxp3 <- ggboxplot(data = my_data,
                  x = "numerosity",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, ncol = 2, scale = "free_x")

print(bxp3)


hist(my_data$deviation_score)


# LMM ----------------------------------------------------------------

my_data$deviation_score2 <- scale(my_data$deviation_score, center = TRUE, scale = TRUE)
hist(my_data$deviation_score2)

# ID as factor
str(my_data)

# my_data$perceptpairs <- as.factor(my_data$perceptpairs)
my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$numerosity <- as.factor(my_data$numerosity)


# not converged
full_model <- lmer(deviation_score2 ~ protectzonetype * numerosity + 
                     (1 + numerosity + protectzonetype|participant), data = my_data, REML = FALSE)

summary(full_model)
rePCA(full_model)
summary(rePCA(full_model))


# converged
model.lm <- lmer(deviation_score2 ~ protectzonetype * numerosity + 
                   (1 + protectzonetype|participant), data = my_data, REML = FALSE)

summary(model.lm)
anova(model.lm)

model.lm2 <- lmer(deviation_score2 ~ protectzonetype * numerosity + 
                   (1 |participant), data = my_data, REML = FALSE)

summary(model.lm2)


# so model.lm is a better converged model

anova(model.lm, model.lm2)

# interaction

model.reduced <- lmer(deviation_score2 ~ protectzonetype + numerosity + 
                        (1 + protectzonetype|participant), data = my_data, REML = FALSE)
summary(model.reduced)
anova(model.reduced)
anova(model.lm, model.reduced)

emmip(model.lm, protectzonetype ~ numerosity)


# alignment condition/numerosity
model.null <- lmer(deviation_score2 ~ protectzonetype + (1 + protectzonetype|participant),
                  data = my_data, REML = FALSE)


anova(model.reduced, model.null)

# simple (main) effect (only for data_ws04)

simple_main <- joint_tests(model.lm, by = "numerosity")


# contrast: post-hoc comparison
emms <- emmeans(
  model.lm,
  list(pairwise ~ protectzonetype|numerosity),
  adjust = "tukey"
)

summary(emms, infer = TRUE)


emms2 <- emmeans(
  model.lm,
  list(pairwise ~ numerosity|protectzonetype),
  adjust = "tukey"
)

summary(emms2, infer = TRUE)

# fix effect r2

r.squaredGLMM(model.lm)
# https://www.rdocumentation.org/packages/r2glmm/versions/0.1.2/topics/r2beta
# https://stats.stackexchange.com/questions/453758/differences-in-proportion-of-variance-explained-by-mumin-and-r2glmm-packages-usi
# r2beta may have error

# model R2
r2beta(model.lm, method = 'kr', partial = TRUE)

# an APA style table: https://cran.r-project.org/web/packages/sjPlot/vignettes/tab_mixed.html
tab_model(model.lm, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)

# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans_res <- emmeans(
  alignment_con.model_random_slope,
  list(pairwise ~ protectzonetype * numerosity),
  adjust = "tukey"
)

print(emmeans_res)


summary(glht(alignment_con.model_random_slope3, linfct=mcp(numerosity ="Tukey")))

