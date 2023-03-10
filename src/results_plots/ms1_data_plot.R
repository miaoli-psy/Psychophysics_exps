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
library(svglite)


# prepare -----------------------------------------------------------------

# set working path
setwd("C:/SCALab/projects/numerosity_exps/src/results_plots/")

# read data
data_preprocessed <- read_excel("../../data/exp1_rerun_data/ms1_all_data.xlsx")

data_preprocessed$protectzonetype[data_preprocessed$protectzonetype == 0] <- "tangential"
data_preprocessed$protectzonetype[data_preprocessed$protectzonetype == 1] <- "radial"


# data by subject
data_by_subject <- data_preprocessed %>% 
  group_by(numerosity, 
           protectzonetype, 
           list_index, 
           participant,
           winsize) %>% 
  summarise(
    n = n(),
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score)
  ) %>% 
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt(n)
  )


# data across subject
data_across_subject <- data_preprocessed %>% 
  group_by(numerosity, 
           protectzonetype, 
           list_index,
           winsize) %>% 
  summarise(
    n = n(),
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score)
  ) %>% 
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt(n)
  )

# data across subject2: no averaged for 5 displays
data_across_subject2 <- data_preprocessed %>% 
  group_by(numerosity, 
           protectzonetype, 
           winsize) %>% 
  summarise(
    n = n(),
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score)
  ) %>% 
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt(n)
  )


# plot deviation for each display

my_plot <-  ggplot() +
  
  geom_point(
    data = data_across_subject,
    aes(
      x = numerosity,
      y = deviation_score_mean,
      color = protectzonetype,
      group = protectzonetype
    ),
    position = position_dodge(1),
    stat = "identity",
    alpha = 0.5,
    size = 3
  ) +
  
  geom_errorbar(
    data = data_across_subject,
    aes(
      x = numerosity,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_score_SEM,
      ymax = deviation_score_mean + deviation_score_SEM,
      group = protectzonetype,
      color = protectzonetype
    ),
    size  = 1.2,
    width = .00,
    alpha = 0.5,
    position = position_dodge(1)
  ) +
  
  geom_point(
    data = data_across_subject2,
    aes(
      x = numerosity,
      y = deviation_score_mean,
      color = protectzonetype,
      group = protectzonetype
    ),
    position = position_dodge(1),
    stat = "identity",
    alpha = 0.2,
    size = 3
  ) +
  
  
  scale_fill_manual(values = c("radial" = "#FF0000",
                               "tangential" = "#2600FF")) +
  
  scale_colour_manual(values = c("radial" = "#FF0000",
                                 "tangential" = "#2600FF")) +
  
  geom_hline(yintercept = 0, linetype = "dashed") +
  
  labs(y = "Deviation score", x = "Numerosity") +
  
  theme(axis.title.x = element_text(color="black", size=14, face="bold"),
        axis.title.y = element_text(color="black", size=14, face="bold"),
        panel.border = element_blank(),  
        # remove panel grid lines
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        # remove panel background
        panel.background = element_blank(),
        # add axis line
        axis.line = element_line(colour = "grey"),
        # x,y axis tick labels
        axis.text.x = element_text(size = 12, face = "bold"),
        axis.text.y = element_text(size = 12, face = "bold"),
        # legend size
        legend.title = element_text(size = 12, face = "bold"),
        legend.text = element_text(size = 10),
        # facet wrap title
        strip.text.x = element_text(size = 12, face = "bold")) +
  
  facet_wrap( ~ winsize + list_index , scales = "free_x",
              labeller = labeller(winsize =
                                    c("0.3" = "21-25",
                                      "0.4" = "31-35",
                                      "0.5" = "41-45",
                                      "0.6" = "49-53",
                                      "0.7" = "54-58"),
                                  list_index =
                                    c("0" = "D1",
                                      "1" = "D2",
                                      "2" = "D3",
                                      "3" = "D4",
                                      "4" = "D5")))

print(my_plot)

ggsave(file = "test2.svg", plot = my_plot)




# data across subject
data_across_subject3 <- data_preprocessed %>% 
  group_by(protectzonetype, 
           winsize) %>% 
  summarise(
    n = n(),
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score)
  ) %>% 
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt(n)
  )


# data across subject
data_by_subject3 <- data_preprocessed %>% 
  group_by(participant,
           protectzonetype, 
           winsize) %>% 
  summarise(
    n = n(),
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score)
  ) %>% 
  mutate(
    deviation_score_SEM = deviation_score_std / sqrt(n)
  )

my_plot2 <-  ggplot() +
  
  geom_point(
    data = data_across_subject3,
    aes(
      x = winsize,
      y = deviation_score_mean,
      color = protectzonetype
    ),
    position = position_jitter(0.01),
    stat = "identity",
    alpha = 0.5,
    size = 3
  ) +
  
  geom_errorbar(
    data = data_across_subject3,
    aes(
      x = winsize,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_score_SEM,
      ymax = deviation_score_mean + deviation_score_SEM,
      color = protectzonetype
    ),
    size  = 1.2,
    width = .00,
    alpha = 0.5,
    position = position_dodge(0.01)
  ) +
  
  
  scale_fill_manual(values = c("radial" = "#FF0000",
                               "tangential" = "#2600FF")) +
  
  scale_colour_manual(values = c("radial" = "#FF0000",
                                 "tangential" = "#2600FF")) +
  
  geom_hline(yintercept = 0, linetype = "dashed") +
  
  labs(y = "Deviation score (DV)", x = "Numerosity") +
  
  theme(axis.title.x = element_text(color="black", size=14, face="bold"),
        axis.title.y = element_text(color="black", size=14, face="bold"),
        panel.border = element_blank(),  
        # remove panel grid lines
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        # remove panel background
        panel.background = element_blank(),
        # add axis line
        axis.line = element_line(colour = "grey"),
        # x,y axis tick labels
        axis.text.x = element_text(size = 12, face = "bold"),
        axis.text.y = element_text(size = 12, face = "bold"),
        # legend size
        legend.title = element_text(size = 12, face = "bold"),
        legend.text = element_text(size = 10),
        # facet wrap title
        strip.text.x = element_text(size = 12, face = "bold"))


print(my_plot2)


ggsave(file = "test2.svg", plot = my_plot2, width = 5.07, height = 4.95, units = "in")
