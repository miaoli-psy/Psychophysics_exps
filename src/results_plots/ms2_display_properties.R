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
library(svglite)

# set working path
setwd("D:/SCALab/projects/numerosity_exps/displays/ms2_displays/")

# read data
displays <- read_excel("displays.xlsx")

# data by display
data_across5_display <- displays %>%
  group_by(protectzonetype,
           perceptpairs,
           numerosity,
           winsize) %>%
  summarise(
    convexhull_mean = mean(convexhull),
    convexhull_std = sd(convexhull),
    occupancyarea_mean = mean(occupancyarea),
    occupancyarea_std = sd(occupancyarea),
    averageE_mean = mean(averageeccentricity),
    averageE_std = sd(averageeccentricity),
    averagespacing_mean = mean(averagespacing),
    averagespacing_std = sd(averagespacing),
    density_itemsperdeg2_mean = mean(density),
    density_itemsperdeg2_std = sd(density),
    n = n()
  )


x_breaks <- function(x){
  if (x < 50) {
    c(34, 36, 38, 40, 42, 44)
  } else{
    c(54, 56, 58, 60, 62, 64)
  }
}

# convexhull
my_plot <-  ggplot() +
  
  geom_point(data = data_across5_display, aes(x = numerosity,
                                              y = occupancyarea_mean,
                                              color= protectzonetype,
                                              group = protectzonetype),
             position = "dodge", stat = "identity", alpha = 0.5, width = 0.5) +
  
  
  geom_hline(yintercept = 0, linetype = "dashed") +
  
  labs(y = "occupancyarea (convexhull 2D volume deg2)", x = "numerosity") +
  
  scale_color_manual(labels = c("tangential", "radial"),
                     values = c("#4169e1", "#ff4500"),
                     name = "alignment condition" ) +

  scale_x_continuous(breaks = x_breaks) +
  
  
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
  
  facet_wrap( ~ perceptpairs * winsize, 
              scale = "free_x",
              labeller = labeller(winsize =
                                    c("0.4" = "winsize0.4",
                                      "0.6" = "winsize0.6"),
                                  perceptpairs = 
                                    c("0" = "0 pair",
                                      "0.25" = "25% pairs",
                                      "0.5" = "50% pairs",
                                      "0.75" = "75% pairs",
                                      "1" = "100% pairs")))

print(my_plot)


# occupancy area (convexhull 2D volume)
my_plot2 <-  ggplot() +
  
  geom_point(data = data_across5_display, aes(x = numerosity,
                                              y = convexhull_mean,
                                              color= protectzonetype,
                                              group = protectzonetype),
             position = "dodge", stat = "identity", alpha = 0.5, width = 0.5) +
  
  
  geom_hline(yintercept = 0, linetype = "dashed") +
  
  labs(y = "convexhull (deg)", x = "numerosity") +
  
  scale_color_manual(labels = c("tangential", "radial"),
                     values = c("#4169e1", "#ff4500"),
                     name = "alignment condition" ) +
  
  scale_x_continuous(breaks = x_breaks) +
  
  
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
  
  facet_wrap( ~ perceptpairs * winsize, 
              scale = "free_x",
              labeller = labeller(winsize =
                                    c("0.4" = "winsize0.4",
                                      "0.6" = "winsize0.6"),
                                  perceptpairs = 
                                    c("0" = "0 pair",
                                      "0.25" = "25% pairs",
                                      "0.5" = "50% pairs",
                                      "0.75" = "75% pairs",
                                      "1" = "100% pairs")))

print(my_plot2)


# density item/deg2
my_plot3 <-  ggplot() +
  
  geom_point(data = data_across5_display, aes(x = numerosity,
                                              y = density_itemsperdeg2_mean,
                                              color= protectzonetype,
                                              group = protectzonetype),
             position = "dodge", stat = "identity", alpha = 0.5, width = 0.5) +
  
  
  geom_hline(yintercept = 0, linetype = "dashed") +
  
  labs(y = "density (item/deg2)", x = "numerosity") +
  
  scale_color_manual(labels = c("tangential", "radial"),
                     values = c("#4169e1", "#ff4500"),
                     name = "alignment condition" ) +
  
  scale_x_continuous(breaks = x_breaks) +
  
  
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
  
  facet_wrap( ~ perceptpairs * winsize, 
              scale = "free_x",
              labeller = labeller(winsize =
                                    c("0.4" = "winsize0.4",
                                      "0.6" = "winsize0.6"),
                                  perceptpairs = 
                                    c("0" = "0 pair",
                                      "0.25" = "25% pairs",
                                      "0.5" = "50% pairs",
                                      "0.75" = "75% pairs",
                                      "1" = "100% pairs")))

print(my_plot3)


