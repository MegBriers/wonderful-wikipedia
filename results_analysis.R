setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data <- read.csv("./analysis/mentions.csv", stringsAsFactors=TRUE)

data$per_1000 <- (data$mentions/data$length)*1000 

library(ggplot2)
library(dplyr)

mean_phil <- mean(data$length[data$category=="philosophy"], )
mean_maths <- mean(data$length[data$category=="maths"])

phil <- data[data$category=="philosophy", ]
maths <- data[data$category=="maths", ]
phil$typical <- round(mean_phil, 0)
maths$typical <- round(mean_maths, 0)

new_data <- rbind.data.frame(maths, phil)

new_data$per_typical <- (new_data$mentions/new_data$length) * new_data$typical 

q <- ggplot(new_data, aes(x=method, y=per_typical, fill=category)) +
  geom_violin(position=position_dodge(1), trim=TRUE)+
  geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
  stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
  xlab("method of analysis") + 
  ylab("mentions per 1000 characters") +
  scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
  theme_bw()

q

r <- ggplot(new_data, aes(x=category, y=length, fill=category)) +
  geom_violin(position=position_dodge(1), trim=TRUE)+
  geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
  stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
  xlab("method of analysis") + 
  ylab("mentions per 1000 characters") +
  scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
  theme_bw()

r

p <- ggplot(data, aes(x=method, y=sqrt(per_1000), fill=category)) +
    geom_violin(position=position_dodge(1), trim=TRUE)+
    geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
    stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
    xlab("method of analysis") + 
    ylab("sqrt mentions per 1000 characters") + 
    ylim(c(0,3.1))+
    scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
    theme_bw()

p 

m1 <- lm(sqrt(per_1000)~method*category, data=data)
plot(m1,which=1)
plot(m1,which=2)

# type 3 - looking for an interaction
Anova(m1,type=3)

# type 2 - no significant interaction
Anova(m1,type=2)


