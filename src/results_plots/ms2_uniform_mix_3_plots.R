# libraries
library(readxl)
library(ggplot2)
library(ggthemes)
library(svglite)

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/results_plots/")

# read data
# full contrast: mix, white, black displays
all_data_full_contrast <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3_full_contrast.xlsx")
all_data_full_contrast_each_pp <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3_full_contrast_each_pp.xlsx")
all_data_combine_num_full_contrast <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3_full_contrast_combine_num.xlsx")
all_data_combine_num_full_contrast_each_pp <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3_full_contrast_combine_num_each_pp.xlsx")

# not full contrast: mix vs. uniform (combine white and black)
all_data <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3.xlsx")
all_data_each_pp <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3_each_pp.xlsx")
all_data_combine_num <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3_combine_num.xlsx")
all_data_combine_num_each_pp <- read_excel("../../data/ms2_uniform_mix_3_data/ms2_uniform_mix_3_combine_num_each_pp.xlsx")


# plot sep numerosity: deviation score as a function of percent single/triplet discs
my_plot <-  ggplot() +
  
  geom_bar(data = all_data_full_contrast, aes(x = percent_triplets,
                                              y = deviation_scoremean,
                                              fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0, 0.5, 1)) +
  
  scale_y_continuous(limits = c(-5, 8)) +
  
  # each data point represents the average deviation of 1 participant
  # geom_point(data = all_data_full_contrast_each_pp, aes(x = percent_triplets,
  #                                                       y = deviation_scoremean,
  #                                                       group = protectzonetype,
  #                                                       colour = protectzonetype),
  #            alpha = 0.2,
  #            position = position_dodge(0.2))+
  
  geom_errorbar(data = all_data_full_contrast, aes(x = percent_triplets,
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
  
  facet_wrap(~ numerosity + contrast_full)
  

print(my_plot)


# seprate numerosity: Relative estimation error as a function of percent triplets
my_plot2 <-  ggplot() +
  
  geom_bar(data = all_data, aes(x = percent_triplets,
                                y = deviation_scoremean,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0, 0.5, 1)) +
  
  scale_y_continuous(limits = c(-5, 8)) +
  
  # each data point represents the average deviation of 1 participant
  # geom_point(data = all_data_each_pp, aes(x = percent_triplets,
  #                                         y = deviation_scoremean,
  #                                         group = protectzonetype,
  #                                         colour = protectzonetype),
  #            alpha = 0.2,
  #            position = position_dodge(0.2)) +
  
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
  
  facet_wrap(~ numerosity + contrast)


print(my_plot2)


# plot combine numerosity, sep winsize
my_plot3 <- ggplot() +
  
  geom_bar(data = all_data_combine_num, aes(x = percent_triplets,
                                            y = deviation_scoremean,
                                            fill = protectzonetype),
           
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0,0.5, 1)) +
  
  scale_y_continuous(limits = c(-4, 5)) +

  geom_errorbar(data = all_data_combine_num, aes(x = percent_triplets,
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
  
  facet_wrap(~ winsize + contrast)

print(my_plot3)



my_plot4 <- ggplot() +
  
  geom_bar(data = all_data_combine_num, aes(x = percent_triplets,
                                            y = percent_changemean,
                                            fill = protectzonetype),
           
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0, 0.5, 1)) +
  
  scale_y_continuous(limits = c(-0.1, 0.1)) +
  
  geom_errorbar(data = all_data_combine_num, aes(x = percent_triplets,
                                                 y = percent_changemean,
                                                 ymin = percent_changemean - SEM_percent_change,
                                                 ymax = percent_changemean + SEM_percent_change,
                                                 group = protectzonetype),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(0.2)) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Relative estimation error", x = "percent single/triplet discs") +
  
  theme_few() +
  
  facet_wrap(~ winsize + contrast)

print(my_plot4)
