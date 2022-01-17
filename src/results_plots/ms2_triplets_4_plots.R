# libraries
library(readxl)
library(ggplot2)
library(ggthemes)
library(svglite)

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/results_plots/")

# read data
all_data <- read_excel("../../data/ms2_triplets_4_data/ms2_triplets_4_data.xlsx")
all_data_each_pp <- read_excel("../../data/ms2_triplets_4_data/ms2_triplets_4_data_each_pp.xlsx")

# plot deviation score
my_plot <-  ggplot() +
  
  geom_bar(data = all_data, aes(x = numerosity,
                                y = deviation_scoremean,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 2) +
  
  scale_x_continuous(breaks = c(51, 54, 57, 60, 63, 66, 69, 72, 78, 81, 84, 87, 90, 93, 96, 99 )) +
  
  scale_y_continuous(limits = c(-10, 10)) +
  
  # each data point represents the average deviation of 1 participant
   # geom_point(data = all_data_each_pp, aes(x = numerosity,
   #                                         y = deviation_scoremean,
   #                                        group = protectzonetype,
   #                                         colour = protectzonetype),
   #            alpha = 0.2,
   #            position = position_dodge(2))+

   geom_errorbar(data = all_data, aes(x = numerosity,
                                      y = deviation_scoremean,
                                      ymin = deviation_scoremean - SEM_deviation_score,
                                      ymax = deviation_scoremean + SEM_deviation_score,
                                      group = protectzonetype),
                 color = "black",
                 size  = 1.2,
                 width = .00,
                 position = position_dodge(2)) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "numerosity") +
  
  theme_few()

print(my_plot)


my_plot2 <-  ggplot() +
  
  geom_bar(data = all_data, aes(x = numerosity,
                                y = percent_changemean,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 2) +
  
  scale_x_continuous(breaks = c(51, 54, 57, 60, 63, 66, 69, 72, 78, 81, 84, 87, 90, 93, 96,99 )) +
  
  scale_y_continuous(limits = c(-0.25, 0.25)) +
  
  # each data point represents the average deviation of 1 participant
  geom_point(data = all_data_each_pp, aes(x = numerosity,
                                          y = percent_changemean,
                                          group = protectzonetype,
                                          colour = protectzonetype),
             alpha = 0.2,
             position = position_dodge(2))+
  
  geom_errorbar(data = all_data, aes(x = numerosity,
                                     y = percent_changemean,
                                     ymin = percent_changemean - SEM_percent_change,
                                     ymax = percent_changemean + SEM_percent_change,
                                     group = protectzonetype),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(2)) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Relative estimation error", x = "numerosity") +
  
  theme_few()

print(my_plot2)