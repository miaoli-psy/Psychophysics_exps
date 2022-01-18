# libraries
library(readxl)
library(ggplot2)
library(ggthemes)
library(svglite)

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/results_plots/")

all_data <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2.xlsx")
all_data_each_pp <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2_each_pp.xlsx")
all_data_combine_num <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2_combine_num.xlsx")
all_data_combine_num_each_pp <- read_excel("../../data/ms2_mix_prolific_2_data/ms2_mix_2_combine_num_each_pp.xlsx")

# functions
breaks_fun <- function(x) {
  if (max(x) > 50) {
    c(54, 56, 58, 60, 62, 64)
  } else {
    c(34, 36, 38, 40, 42, 44)
  }
}


# plot sep numerosity
my_plot <-  ggplot() +
  
  geom_bar(data = all_data, aes(x = percent_triplets,
                                y = deviation_scoremean,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0, 0.25,0.5, 0.75, 1)) +
  
  scale_y_continuous(limits = c(-18, 0)) +
  
  # each data point represents the average deviation of 1 participant
  # geom_point(data = all_data_each_pp, aes(x = percent_triplets,
  #                                         y = deviation_scoremean,
  #                                         group = protectzonetype,
  #                                         colour = protectzonetype),
  #            alpha = 0.2,
  #            position = position_dodge(0.2))+
  
  geom_errorbar(data = all_data, aes(x = percent_triplets,
                                     y = deviation_scoremean,
                                     ymin = deviation_scoremean - SEM_deviation_score,
                                     ymax = deviation_scoremean + SEM_deviation_score,
                                     group = protectzonetype),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(0.2)) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "percent single/triplet discs") +
  
  theme_few() +
  
  facet_wrap(~ numerosity, nrow = 2)
  

print(my_plot)

# plot sep clustering
my_plot2 <-  ggplot() +
  
  geom_bar(data = all_data, aes(x = numerosity,
                                y = deviation_scoremean,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 1.5) +
  
  scale_x_continuous(breaks = breaks_fun) +
  
  scale_y_continuous(limits = c(-18, 0)) +
  
  # each data point represents the average deviation of 1 participant
  # geom_point(data = all_data_each_pp, aes(x = percent_triplets,
  #                                         y = deviation_scoremean,
  #                                         group = protectzonetype,
  #                                         colour = protectzonetype),
  #            alpha = 0.2,
  #            position = position_dodge(0.2))+
  
  geom_errorbar(data = all_data, aes(x = numerosity,
                                     y = deviation_scoremean,
                                     ymin = deviation_scoremean - SEM_deviation_score,
                                     ymax = deviation_scoremean + SEM_deviation_score,
                                     group = protectzonetype),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(1.5)) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "numerosity") +
  
  theme_few() +
  
  facet_wrap(~ percent_triplets + winsize, scales = "free")


print(my_plot2)