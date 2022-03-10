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
data_preprocessed <- read_excel("../../data/ms2_triplets_4_data/preprocessed_triplets_4.xlsx")

# data by subject
data_by_subject <- data_preprocessed %>%
  group_by(numerosity, participant, protectzonetype, winsize) %>%
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize = 15

data_by_subject <- data_by_subject %>% 
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt (15),
    percent_change_SEM = percent_change_std / sqrt (15)
    )
    

# data across subject
data <- data_preprocessed %>% 
  group_by(numerosity, protectzonetype, winsize) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize 15 displays * 19 participants
data <- data %>%
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt (15 * 16),
    percent_change_SEM = percent_change_std / sqrt (15 * 16)
  )



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

# numerosity

bxp3 <- ggboxplot(data = data_by_subject,
                  x = "numerosity",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize, ncol = 2, scale = "free_x")

print(bxp3)



# result plots ------------------------------------------------------------

x_breaks <- function(x){
  if (x < 75) {
    c(51, 54, 57, 60, 63, 66, 69, 72)
  } else{
    c(78, 81, 84, 87, 90, 93, 96, 99)
  }
}

my_plot2 <-  ggplot() +
  
  geom_bar(
    data = data,
    aes(x = numerosity,
        y = deviation_score_mean,
        fill = protectzonetype),
    position = "dodge",
    stat = "identity",
    alpha = 0.5,
    width = 2
  ) +
  
  scale_x_continuous(breaks = x_breaks) +
  
  # ylim(-3.5, 7) +
  
  geom_errorbar(
    data = data,
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
    position = position_dodge(2)
  ) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "nuemrosity") +
  
  theme_few() +
  
  facet_wrap( ~ winsize , ncol = 2, scale = "free_x")


print(my_plot2)

ggsave(
  file = "test.svg",
  plot = my_plot2,
  width = 12,
  height = 5,
  dpi = 300
)


# result plot 2: combine numerosity ---------------------------------------


# data across subject
data3 <- data_preprocessed %>% 
  group_by(protectzonetype, winsize) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize 8  * 19 participants
data3 <- data3 %>%
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt (15 * 16 * 8),
    percent_change_SEM = percent_change_std / sqrt (15 * 16 * 8)
    )

my_plot3 <-  ggplot() +
  
  geom_bar(
    data = data3,
    aes(x = winsize,
        y = deviation_score_mean,
        fill = protectzonetype),
    position = "dodge",
    stat = "identity",
    alpha = 0.5,
    width = 0.25
  ) +
  
  # scale_x_continuous(breaks = c(0.4, 0.6)) +
  
  # ylim(-3.5, 7) +
  
  geom_errorbar(
    data = data3,
    aes(
      x = winsize,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_score_SEM,
      ymax = deviation_score_mean + deviation_score_SEM,
      group = protectzonetype
    ),
    color = "black",
    size  = 1.2,
    width = .00,
    position = position_dodge(0.25)
  ) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "nuemrosity range") +
  
  theme_few()
  
print(my_plot3)

ggsave(
  file = "test.svg",
  plot = my_plot3,
  width = 12,
  height = 5,
  dpi = 300
)



# LMM  ------------------------------------

# TODO
my_data <- data_by_subject

summary(my_data)

str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$numerosity <- as.factor(my_data$numerosity)
my_data$participant <- as.factor(my_data$participant)
my_data$winsize <- as.factor(my_data$winsize)



# check the effect of alignment condition (protectzonetype)
alignment_con.model_random_slope <-
  lmer(
    deviation_score_mean ~ protectzonetype + numerosity + 
      (1 + protectzonetype|participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.model_random_slope


coef(alignment_con.model_random_slope)

alignment_con.null_random_slope <-
  lmer(
    deviation_score_mean ~ numerosity +
      (1 + protectzonetype | participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.null_random_slope


anova(alignment_con.model_random_slope, 
      alignment_con.null_random_slope)


r.squaredGLMM(alignment_con.model_random_slope)

r2beta(alignment_con.model_random_slope, method = 'kr', partial = TRUE)

tab_model(alignment_con.model_random_slope, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)
# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans_res <- emmeans(
  alignment_con.model_random_slope,
  list(pairwise ~ protectzonetype * numerosity),
  adjust = "tukey"
)
print(emmeans_res)

