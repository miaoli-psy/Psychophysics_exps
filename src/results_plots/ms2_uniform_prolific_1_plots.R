# libraries
library(readxl)
library(ggplot2)
library(ggthemes)
library(svglite)

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/results_plots/")

# read data
all_data <- read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_r.xlsx")
all_data_each_pp <- read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_each_pp.xlsx")
all_data_combine_num <- read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_r_combine_num.xlsx")
all_data_combine_num_each_pp <- read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_combine_num_each_pp.xlsx")
all_data_combine_cluster <- read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_r_combine_cluster.xlsx")
all_data_combine_cluster_each_pp <- read_excel("../../data/ms2_uniform_prolific_1_data/prolifc_data_combine_cluster_each_pp.xlsx")


# plot sep numerosity
my_plot <-  ggplot() +
  
  geom_bar(data = all_data, aes(x = percent_triplets,
                                y = mean_deviation_score,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0, 0.25,0.5, 0.75, 1)) +
  
  scale_y_continuous(limits = c(-25, 25)) +
  
  # each data point represents the average deviation of 1 participant
  geom_point(data = all_data_each_pp, aes(x = percent_triplets,
                                          y = mean_deviation_score,
                                          group = protectzonetype,
                                          colour = protectzonetype),
             alpha = 0.2,
             position = position_dodge(0.2))+
  
  geom_errorbar(data = all_data, aes(x = percent_triplets,
                                     y = mean_deviation_score,
                                     ymin = mean_deviation_score - SEM,
                                     ymax = mean_deviation_score + SEM,
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

# plot combine numerosity, sep winsize
my_plot2 <- ggplot() +
  
  geom_bar(data = all_data_combine_num, aes(x = percent_triplets,
                                            y = mean_deviation_score,
                                            fill = protectzonetype),
           
           position = "dodge", stat = "identity", alpha = 0.5, width = 0.2) +
  
  scale_x_continuous(breaks = c(0, 0.25,0.5, 0.75, 1)) +
  
  scale_y_continuous(limits = c(-10, 0)) +

  geom_errorbar(data = all_data_combine_num, aes(x = percent_triplets,
                                                         y = mean_deviation_score,
                                                         ymin = mean_deviation_score - SEM,
                                                         ymax = mean_deviation_score + SEM,
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
  
  facet_wrap(~ winsize)

print(my_plot2)


# plot combine cluster
my_plot3 <-  ggplot() +
  
  geom_bar(data = all_data_combine_cluster, aes(x = numerosity,
                                y = mean_deviation_score,
                                fill = protectzonetype),
           position = "dodge", stat = "identity", alpha = 0.5, width = 1.5) +
  
  scale_x_continuous(breaks = c(34, 36, 38, 40, 42, 44, 54, 56, 58, 60, 62, 64)) +

  scale_y_continuous(limits = c(-25, 25)) +
  
  # each data point represents the average deviation of 1 participant
  geom_point(data = all_data_combine_cluster_each_pp, aes(x = numerosity,
                                          y = mean_deviation_score,
                                          group = protectzonetype,
                                          colour = protectzonetype),
             alpha = 0.2,
             position = position_dodge(1.5))+
  
  geom_errorbar(data = all_data_combine_cluster, aes(x = numerosity,
                                     y = mean_deviation_score,
                                     ymin = mean_deviation_score - SEM,
                                     ymax = mean_deviation_score + SEM,
                                     group = protectzonetype),
                color = "black",
                size  = 1.2,
                width = .00,
                position = position_dodge(1.5)) +
  
  scale_fill_manual(values = c("radial" = "#ff4500",
                               "tangential" = "#4169e1")) +
  
  scale_colour_manual(values = c("radial" = "#ff4500",
                                 "tangential" = "#4169e1")) +
  
  labs(y = "Deviation score", x = "percent single/triplet discs") +
  
  theme_few()

print(my_plot3)


ggsave(file = "test.svg", plot = my_plot, dpi = 600, height = 8, width = 20)



