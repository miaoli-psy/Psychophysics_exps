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
setwd("D:/SCALab/projects/numerosity_exps/src/results_plots/")

# read data
data_preprocessed <- read_excel("../../data/exp1_rerun_data/cleanedTotalData_fullinfo_v3.xlsx")

data_preprocessed <- data_preprocessed %>% 
  mutate(alignment_con  = case_when(
    crowdingcons == 1 ~ "radial",
    crowdingcons == 0 ~ "tangential"))

# plot: deviation score- numerosity range -------------------------------


# data by subject
data_by_subject <- data_preprocessed %>% 
  group_by(winsize, participant_N, alignment_con) %>% 
  summarise(deviation_score_mean = mean(deviation_score),
            deviation_score_std = sd(deviation_score),
            percent_change_mean = mean(percent_change),
            percent_change_std = sd(percent_change))

# data across subject

data_across_subject <- data_preprocessed %>% 
  group_by(winsize, alignment_con) %>% 
  summarise(
    n = n(),
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
    percent_change_std = sd(percent_change)
    )%>% 
      mutate(deviation_score_SEM = deviation_score_std/sqrt(n),
             percent_change_SEM = percent_change_std/sqrt(n)) %>% 
  mutate(deviation_score_ic = deviation_score_SEM * qt((1 - 0.05)/2 + 0.5, n - 1),
         percent_change_ic = percent_change_SEM * qt((1 - 0.05)/2 + 0.5, n - 1))



# see each column
n_distinct(data_preprocessed$participant_N)


my_plot <-  ggplot() +
  
  geom_bar(data = data_across_subject, aes(x = winsize,
                                           y = deviation_score_mean,
                                           group = alignment_con,
                                           fill = alignment_con),
           position =  position_dodge(0.09), stat = "identity", alpha = 0.5) +
  
  
  # each data point represents the average deviation of 1 participant
  geom_point(data = data_by_subject, aes(x = winsize,
                                         y = deviation_score_mean,
                                         group = alignment_con,
                                         color = alignment_con),
             alpha = 0.25,
             position = position_dodge(0.09)) +
  
  
  geom_errorbar(data = data_across_subject, aes(x = winsize,
                                                y = deviation_score_mean,
                                                ymin = deviation_score_mean - deviation_score_ic,
                                                ymax = deviation_score_mean + deviation_score_ic,
                                                group = alignment_con),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(0.09)) +
  
  scale_fill_manual(labels = c("radial", "tangential"),
                    values = c("#ff4500", "#4169e1"),
                    name = "aligenment condition" )  +
  
  scale_color_manual(labels = c("radial", "tangential"),
                     values = c("#ff4500", "#4169e1"),
                     name = "aligenment condition" )  +
  
  scale_x_continuous(breaks = c(0.3, 0.4, 0.5, 0.6, 0.7),
                     labels = c("21-25", "31-35", "41-45", "49-53", "54-58")) +
  
  scale_y_continuous(breaks = c(-10, -5, 0, 5, 10, 15, 20)) +
  
  
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
        strip.text.x = element_text(size = 12, face = "bold"))


print(my_plot)


ggsave(file = "test.svg", plot = my_plot)

# plot: percent changes - numerosity --------------------------------------

my_plot2 <-  ggplot() +
  
  geom_bar(data = data_across_subject, aes(x = winsize,
                                           y = percent_change_mean,
                                           group = alignment_con,
                                           fill = alignment_con),
           position =  position_dodge(0.09), stat = "identity", alpha = 0.5) +
  
  
  # each data point represents the average deviation of 1 participant
  geom_point(data = data_by_subject, aes(x = winsize,
                                         y = percent_change_mean,
                                         group = alignment_con,
                                         color = alignment_con),
             alpha = 0.25,
             position = position_dodge(0.09)) +
  
  
  geom_errorbar(data = data_across_subject, aes(x = winsize,
                                                y = percent_change_mean,
                                                ymin = percent_change_mean - percent_change_ic,
                                                ymax = percent_change_mean + percent_change_ic,
                                                group = alignment_con),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(0.09)) +
  
  scale_fill_manual(labels = c("radial", "tangential"),
                    values = c("#ff4500", "#4169e1"),
                    name = "aligenment condition" )  +
  
  scale_color_manual(labels = c("radial", "tangential"),
                     values = c("#ff4500", "#4169e1"),
                     name = "aligenment condition" )  +
  
  scale_x_continuous(breaks = c(0.3, 0.4, 0.5, 0.6, 0.7),
                     labels = c("21-25", "31-35", "41-45", "49-53", "54-58")) +
  
  # scale_y_continuous(breaks = c(-10, -5, 0, 5, 10, 15, 20)) +
  
  
  labs(y = "Percent changes", x = "Numerosity") +
  
  
  theme(axis.title.x = element_text(color="black", size=14, face="bold"),
        axis.title.y = element_text(color="black", size=14, face="bold"),
        panel.border = element_blank(),  
        # remove panel grid lines
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        # remove panel background
        panel.background = element_blank(),
        # add axis line
        axis.line = element_line(colour = "black"),
        # x,y axis tick labels
        axis.text.x = element_text(size = 12, face = "bold"),
        axis.text.y = element_text(size = 12, face = "bold"),
        # legend size
        legend.title = element_text(size = 12, face = "bold"),
        legend.text = element_text(size = 10),
        # facet wrap title
        strip.text.x = element_text(size = 12, face = "bold"))


print(my_plot2)


ggsave(file = "test.svg", plot = my_plot2)
