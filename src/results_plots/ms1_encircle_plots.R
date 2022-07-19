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
data_preprocessed <- read_csv("../../data/ms1_encircle/preprocessed_encircle.csv")

# plot: perceived groups - numerosity range -------------------------------


# data by subject
data_by_subject <- data_preprocessed %>% 
  group_by(winsize, evaluation, crowdingcons) %>% 
  summarise(perceived_group_n_mean = mean(groups_n),
            perceived_group_n_std = sd(groups_n))

# data across subject
data_across_subject <- data_preprocessed %>% 
  group_by(winsize, crowdingcons) %>% 
  summarise(
    n = n(),
    perceived_group_n_mean = mean(groups_n),
    perceived_group_n_std = sd(groups_n)
  )%>% 
  mutate(perceived_group_n_SEM = perceived_group_n_std/sqrt(n)
         ) %>% 
  mutate(perceived_group_n_std_ic = perceived_group_n_SEM * qt((1 - 0.05)/2 + 0.5, n - 1))


my_plot <-  ggplot() +
  
  geom_bar(data = data_across_subject, aes(x = winsize,
                                           y = perceived_group_n_mean,
                                           group = crowdingcons,
                                           fill = crowdingcons),
           position =  position_dodge(0.09), stat = "identity", alpha = 0.5) +
  
  
  # each data point represents the average deviation of 1 participant
  geom_point(data = data_by_subject, aes(x = winsize,
                                         y = perceived_group_n_mean,
                                         group = crowdingcons,
                                         color = crowdingcons),
             alpha = 0.25,
             position = position_dodge(0.09)) +

  
  geom_errorbar(data = data_across_subject, aes(x = winsize,
                                                y = perceived_group_n_mean,
                                                ymin = perceived_group_n_mean - perceived_group_n_SEM,
                                                ymax = perceived_group_n_mean + perceived_group_n_SEM,
                                                group = crowdingcons),
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
  
  scale_y_continuous(breaks = c(0, 5, 10, 15, 20, 25)) +

  
  labs(y = "Perceived number of groups", x = "Numerosity") +
  
  
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


# plot grouping per evaluation
my_plot2 <-  ggplot() +
  
  geom_bar(data = data_by_subject, aes(x = winsize,
                                           y = perceived_group_n_mean,
                                           group = crowdingcons,
                                           fill = crowdingcons),
           position =  position_dodge(0.09), stat = "identity", alpha = 0.5) +
  
  
  
  scale_fill_manual(labels = c("radial", "tangential"),
                    values = c("#ff4500", "#4169e1"),
                    name = "aligenment condition" )  +
  
  scale_color_manual(labels = c("radial", "tangential"),
                     values = c("#ff4500", "#4169e1"),
                     name = "aligenment condition" )  +
  
  scale_x_continuous(breaks = c(0.3, 0.4, 0.5, 0.6, 0.7),
                     labels = c("21-25", "31-35", "41-45", "49-53", "54-58")) +
  
  scale_y_continuous(breaks = c(0, 5, 10, 15, 20, 25)) +
  
  
  labs(y = "Perceived number of groups", x = "Numerosity") +
  
  
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
  
  facet_wrap( ~ evaluation)


print(my_plot2)
