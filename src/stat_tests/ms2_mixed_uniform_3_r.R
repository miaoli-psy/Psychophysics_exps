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
data_preprocessed <- read_excel("../../data/ms2_uniform_mix_3_data/preprocessed_uniform_mix_3.xlsx")

# check average age

check_age <- data_preprocessed %>% 
  group_by(participant) %>% 
  summarise_at(vars(age),list(age = mean))

check_age <- check_age %>% 
  summarise_at(vars(age), list(age = mean))


# data by subject
data_by_subject <- data_preprocessed %>%
  group_by(numerosity, participant, protectzonetype, perceptpairs, winsize, contrast_full) %>%
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize = 4 or 8

data_by_subject <- data_by_subject %>% 
  mutate(
    deviation_score_SEM = 
      case_when(
        contrast_full == "mix" ~ deviation_score_std / sqrt (8),
        contrast_full == "black" ~ deviation_score_std / sqrt (4),
        contrast_full == "white" ~ deviation_score_std / sqrt (4)
      ),
    percent_change_SEM = 
      case_when(
        contrast_full == "mix" ~ percent_change_std / sqrt (8),
        contrast_full == "black" ~ percent_change_std / sqrt (4),
        contrast_full == "white" ~ percent_change_std / sqrt (4)
      )
    
    
  )

# data across subject
data <- data_preprocessed %>% 
  group_by(numerosity, protectzonetype, perceptpairs, winsize, contrast_full) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize 8 or 4 displays * 19 participants
data <- data %>%
  mutate(
    deviation_score_SEM =
      case_when(
        contrast_full == "mix" ~ deviation_score_std / sqrt (8 * 19),
        contrast_full == "black" ~ deviation_score_std / sqrt (4 * 19),
        contrast_full == "white" ~ deviation_score_std / sqrt (4 * 19)
      ), 
    percent_change_SEM =
      case_when(
        contrast_full == "mix" ~ percent_change_std / sqrt (8 * 19),
        contrast_full == "black" ~ percent_change_std / sqrt (4 * 19),
        contrast_full == "white" ~ percent_change_std / sqrt (4 * 19)
      )
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
  facet_wrap( ~ winsize * contrast_full, nrow = 2, scale = "free_x")

print(bxp)

# clustering level
bxp2 <- ggboxplot(data = data_by_subject,
                  x = "perceptpairs",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize * contrast_full, nrow = 2, scale = "free_x")

print(bxp2)

# numerosity

bxp3 <- ggboxplot(data = data_by_subject,
                  x = "numerosity",
                  y = dv,
                  color = "protectzonetype") +
  facet_wrap( ~ winsize * contrast_full, nrow = 2, scale = "free_x")

print(bxp3)




# data: combine uniform displays ------------------------------------------

# data by subject
data_by_subject2 <- data_preprocessed %>%
  group_by(numerosity, participant, protectzonetype, winsize, contrast) %>%
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize =  8

data_by_subject2 <- data_by_subject2 %>% 
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt (8),
    percent_change_SEM = percent_change_std / sqrt (8)
    )

# data across subject
data2 <- data_preprocessed %>% 
  group_by(numerosity, protectzonetype, winsize, contrast) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize 8  * 19 participants
data2 <- data2 %>%
  mutate(
    deviation_score_SEM =
      case_when(
        contrast == "mix" ~ deviation_score_std / sqrt (8 * 19),
        contrast == "uniform" ~ deviation_score_std / sqrt (8 * 19)
      ), 
    percent_change_SEM =
      case_when(
        contrast == "mix" ~ percent_change_std / sqrt (8 * 19),
        contrast == "uniform" ~ percent_change_std / sqrt (8 * 19)
      )
  )

# result plots ------------------------------------------------------------

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
  
  ylim(-3.5, 7) +
  
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
  
  facet_wrap( ~ winsize * contrast, nrow = 2, scale = "free_x")


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
  group_by(protectzonetype, winsize, contrast) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))


# samplesize 8  * 19 participants
data3 <- data3 %>%
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt (8 * 19 * 6),
    percent_change_SEM = percent_change_std / sqrt (8 * 19 * 6)
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
    width = 0.1
  ) +
  
  scale_x_continuous(breaks = c(0.4, 0.6)) +
  
  ylim(-3.5, 7) +
  
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
    position = position_dodge(0.1)
  ) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "nuemrosity") +
  
  theme_few() +
  
  facet_wrap( ~  contrast, scale = "free_x")


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
my_data <- data_by_subject2

summary(my_data)

str(my_data)

my_data$protectzonetype <- as.factor(my_data$protectzonetype)
my_data$numerosity <- as.factor(my_data$numerosity)
my_data$participant <- as.factor(my_data$participant)
my_data$contrast <- as.factor(my_data$contrast)


# check the effect of alignment condition (protectzonetype)
alignment_con.model_random_slope <-
  lmer(
    deviation_score_mean ~ protectzonetype + numerosity + contrast +
      (1 + protectzonetype|participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.model_random_slope


coef(alignment_con.model_random_slope)

alignment_con.null_random_slope <-
  lmer(
    deviation_score_mean ~ numerosity + contrast +
      (1 + protectzonetype | participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.null_random_slope


anova(alignment_con.model_random_slope, 
      alignment_con.null_random_slope)

# the effect of contrast

alignment_con.null_random_slope2 <-
  lmer(
    deviation_score_mean ~ numerosity + protectzonetype +
      (1 + protectzonetype | participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.null_random_slope2

anova(alignment_con.model_random_slope, 
      alignment_con.null_random_slope2)

# the effect of contrast * protectionzone


alignment_con.model_random_slope3 <-
  lmer(
    deviation_score_mean ~ protectzonetype + numerosity + contrast + protectzonetype * contrast +
      (1 + protectzonetype|participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.model_random_slope3


coef(alignment_con.model_random_slope3)

alignment_con.null_random_slope3 <-
  lmer(
    deviation_score_mean ~ numerosity + contrast + protectzonetype +
      (1 + protectzonetype | participant),
    data = my_data,
    REML = FALSE
  )
alignment_con.null_random_slope3


anova(alignment_con.model_random_slope3, 
      alignment_con.null_random_slope3)


r.squaredGLMM(alignment_con.model_random_slope)

r2beta(alignment_con.model_random_slope, method = 'kr', partial = TRUE)

tab_model(alignment_con.model_random_slope, p.val = "kr", show.df = TRUE, show.std = TRUE, show.se = TRUE, show.stat = TRUE)
# posc-hoc on models not on data set (maybe: https://cran.r-project.org/web/packages/emmeans/vignettes/interactions.html)
emmeans_res <- emmeans(
  alignment_con.model_random_slope,
  list(pairwise ~ protectzonetype * numerosity * contrast),
  adjust = "tukey"
)
print(emmeans_res)

