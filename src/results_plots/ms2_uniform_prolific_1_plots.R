# libraries
library(readxl)
library(ggplot2)
library(ggthemes)
library(svglite)

# set working path
setwd("c:/SCALab/projects/numerosity_exps/src/results_plots/")

# read data
data_preprocessed <- read_excel("../../data/ms2_uniform_prolific_1_data/preprocessed_prolific.xlsx")

# plots numerosity in x-axis -----------------------------------------

# pre-process

# data by subject
data_by_subject <- data_preprocessed %>%
  group_by(numerosity,
           participant,
           protectzonetype,
           winsize) %>%
  summarise(
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )


# data across subject (samplesize = 34 * 5 for winsize0.4; 32 * 5 for winsize 0.6)
data_across_subject <- data_preprocessed %>%
  group_by(numerosity, protectzonetype, winsize) %>%
  summarise(
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )

# plot deviation - numerosity, separate exp1a (small winsize) and exp1b (large winsize)

breaks_fun <- function(x) {
  if(max(x) < 50) {
    seq(34, 44, 2)
  } else {
    seq(54, 64, 2)
  }
}


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
    alpha = 0.6,
    size = 3
  ) +
  
  scale_x_continuous(breaks = breaks_fun) +
  
  scale_y_continuous(limits = c(-13, 0)) +
  
  geom_errorbar(
    data = data_across_subject,
    aes(
      x = numerosity,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_socre_SEM,
      ymax = deviation_score_mean + deviation_socre_SEM,
      group = protectzonetype,
      color = protectzonetype
    ),
    size  = 1.2,
    width = .00,
    alpha = 0.6,
    position = position_dodge(1)
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
  
  facet_wrap( ~ winsize, nrow = 1, scales = "free_x")


print(my_plot)


ggsave(file = "test.svg", plot = my_plot, width = 6.72, height = 3.19, units = "in")

# plots combine all numerosities -----------------------------------------

# data by subject
data_by_subject2 <- data_preprocessed %>%
  group_by(participant,
           protectzonetype,
           winsize) %>%
  summarise(
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )


# data across subject (samplesize = 34 * 5 for winsize0.4; 32 * 5 for winsize 0.6)
data_across_subject2 <- data_preprocessed %>%
  group_by(protectzonetype, winsize) %>%
  summarise(
    deviation_score_mean = mean(deviation_score),
    deviation_score_std = sd(deviation_score),
    percent_change_mean = mean(percent_change),
    percent_change_std = sd(percent_change),
    n = n()
  ) %>%
  mutate(
    deviation_socre_SEM = deviation_score_std / sqrt(n),
    percent_change_SEM = percent_change_std / sqrt(n),
    deviation_socre_CI = deviation_socre_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                    1),
    percent_change_CI = percent_change_SEM * qt((1 - 0.05) / 2 + .5, n -
                                                  1)
  )


my_plot2 <-  ggplot() +
  
  geom_bar(
    data = data_across_subject2,
    aes(
      x = protectzonetype,
      y = deviation_score_mean,
      fill = protectzonetype
    ),
    position = position_dodge(1),
    stat = "identity",
    width = 0.3,
    alpha = 0.5,
    size = 3
  ) +
  
  
  # scale_y_continuous(limits = c(-13, 0)) +
  
  geom_errorbar(
    data = data_across_subject2,
    aes(
      x = protectzonetype,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_socre_SEM,
      ymax = deviation_score_mean + deviation_socre_SEM,
      color = protectzonetype
    ),
    size  = 1.2,
    width = .00,
    alpha = 0.8,
    position = position_dodge(1)
  ) +
  
  geom_point(
    data = data_by_subject2,
    aes(
      x = protectzonetype,
      y = deviation_score_mean,
      color = protectzonetype
    ),
    position = position_jitter(0.1),
    stat = "identity",
    alpha = 0.1,
    size = 3
  ) +
  
  
  scale_fill_manual(values = c("radial" = "#FF0000",
                               "tangential" = "#2600FF")) +
  
  scale_colour_manual(values = c("radial" = "#FF0000",
                                 "tangential" = "#2600FF")) +

  geom_hline(yintercept = 0, linetype = "dashed") +
  
  labs(y = "Deviation score (DV)", x = "Alignment condition") +
  
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
        strip.text.x = element_text(size = 12, face = "bold"),
        # remove legend
        legend.position = "none") +
  
  facet_wrap( ~ winsize, nrow = 1, scales = "free_x",
              labeller = labeller(winsize =
                                    c("0.4" = "Exp 1a (34-44)",
                                      "0.6" = "Exp 1b (54-64)")))


print(my_plot2)

ggsave(file = "test.svg", plot = my_plot2, width = 4, height = 3.19, units = "in")


my_plot3 <-  ggplot() +
  
  geom_point(
    data = data_across_subject2,
    aes(
      x = protectzonetype,
      y = deviation_score_mean,
      color = protectzonetype
    ),
    position = position_dodge(1),
    stat = "identity",
    alpha = 0.5,
    size = 3
  ) +
  
  
  scale_y_continuous(limits = c(-6, 0)) +
  
  geom_errorbar(
    data = data_across_subject2,
    aes(
      x = protectzonetype,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_socre_SEM,
      ymax = deviation_score_mean + deviation_socre_SEM,
      color = protectzonetype
    ),
    size  = 1.2,
    width = .00,
    alpha = 0.8,
    position = position_dodge(1)
  ) +

  
  
  scale_fill_manual(values = c("radial" = "#FF0000",
                               "tangential" = "#2600FF")) +
  
  scale_colour_manual(values = c("radial" = "#FF0000",
                                 "tangential" = "#2600FF")) +
  
  geom_hline(yintercept = 0, linetype = "dashed") +
  
  labs(y = "Deviation score", x = "Alignment condition") +
  
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
        strip.text.x = element_text(size = 12, face = "bold"),
        # remove legend
        legend.position = "none") +
  
  facet_wrap( ~ winsize, nrow = 1, scales = "free_x",
              labeller = labeller(winsize =
                                    c("0.4" = "Exp 1a (34-44)",
                                      "0.6" = "Exp 1b (54-64)")))


print(my_plot3)

ggsave(file = "test.svg", plot = my_plot3, width = 5.23, height = 4.6, units = "in")
# ggsave(file = "test.svg", plot = my_plot3)
