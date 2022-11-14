# libraries
library(readxl)
library(ggplot2)
library(ggthemes)
library(svglite)

# set working path
setwd("D:/SCALab/projects/numerosity_exps/src/results_plots/")

# read data
data_preprocessed <- read_excel("../../data/ms2_uniform_mix_3_data/preprocessed_uniform_mix_3.xlsx")

# data by subject
data_by_subject <- data_preprocessed %>%
  group_by(numerosity,
           participant,
           protectzonetype,
           winsize,
           contrast) %>%
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


data_across_subject <- data_preprocessed %>%
  group_by(numerosity,
           protectzonetype,
           winsize,
           contrast) %>%
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
  
  scale_y_continuous(limits = c(-4, 6.5)) +
  
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
        strip.text.x = element_text(size = 12, face = "bold")) +
  
  facet_wrap( ~ winsize * contrast, nrow = 2, scales = "free_x")


print(my_plot)


ggsave(file = "test2.svg", plot = my_plot, width = 6.72, height = 6.4, units = "in")


data_preprocessed <- data_preprocessed %>% 
  mutate(group = case_when(
    protectzonetype == "radial" & contrast == "mix" ~ "radial mix",
    protectzonetype == "tangential" & contrast == "mix" ~ "tangential mix",
    protectzonetype == "radial" & contrast == "uniform" ~ "radial uniform",
    protectzonetype == "tangential" & contrast == "uniform" ~ "tangential uniform")
)


# data by subject
data_by_subject <- data_preprocessed %>%
  group_by(numerosity,
           participant,
           winsize,
           group) %>%
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


data_across_subject <- data_preprocessed %>%
  group_by(numerosity,
           winsize,
           group) %>%
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
  
  geom_point(
    data = data_across_subject,
    aes(
      x = numerosity,
      y = deviation_score_mean,
      color = group,
      group = group
    ),
    position = position_dodge(1),
    stat = "identity",
    alpha = 0.6,
    size = 3
  ) +
  
  scale_x_continuous(breaks = breaks_fun) +
  
  scale_y_continuous(limits = c(-4, 6.5)) +
  
  geom_errorbar(
    data = data_across_subject,
    aes(
      x = numerosity,
      y = deviation_score_mean,
      ymin = deviation_score_mean - deviation_socre_SEM,
      ymax = deviation_score_mean + deviation_socre_SEM,
      group = group,
      color = group
    ),
    size  = 1.2,
    width = .00,
    alpha = 0.6,
    position = position_dodge(1)
  ) +
  
  scale_fill_manual(values = c("radial mix" = "#FF0000",
                               "tangential mix" = "#2600FF",
                               "radial uniform" = "#ff8080",
                               "tangential uniform" = "#9380ff")) +
  
  scale_colour_manual(values = c("radial mix" = "#FF0000",
                                 "tangential mix" = "#2600FF",
                                 "radial uniform" = "#ff8080",
                                 "tangential uniform" = "#9380ff")) +
  
  
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
        strip.text.x = element_text(size = 12, face = "bold")) +
  
  facet_wrap( ~ winsize, ncol = 2, scales = "free_x")


print(my_plot2)

ggsave(file = "test2.svg", plot = my_plot2, width = 6.72, height = 3.2, units = "in")
