setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data <- read.csv("./analysis/mentions.csv", stringsAsFactors=TRUE)

data$per_1000 <- (data$mentions/data$length)*1000 

library(ggplot2)
library(dplyr)
library(scales)

mean_phil <- mean(data$length[data$category=="philosophy"], )
mean_maths <- mean(data$length[data$category=="maths"])

phil <- data[data$category=="philosophy", ]
maths <- data[data$category=="maths", ]
phil$typical <- round(mean_phil, 0)
maths$typical <- round(mean_maths, 0)

new_data <- rbind.data.frame(maths, phil)

new_data$per_typical <- (new_data$mentions/new_data$length) * new_data$typical 

# GRAPH 1 - mentions per 1000 characters

p <- ggplot(data, aes(x=method, y=sqrt(per_1000), fill=category)) +
  geom_violin(position=position_dodge(1), trim=FALSE)+
  geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
  stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
  xlab("method of analysis") + 
  ylab("sqrt mentions per 1000 characters") + 
  ylim(c(0,4))+
  scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
  theme_bw()

p 

m <- lm(sqrt(per_1000)~category, data=new_data)
plot(m,which=1)
plot(m,which=2)
res.aov <- aov(sqrt(per_1000)~category, data=new_data)
summary(res.aov)


# GRAPH 2 - typical length of an article
l <- ggplot(new_data, aes(x=category, y=log(length), fill=category)) +
  geom_violin(position=position_dodge(1), trim=TRUE)+
  geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
  stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
  xlab("category of article") + 
  ylab("log average number of characters in article") +
  scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
  theme_bw()

l

ml <- lm(log(length)~category, data=new_data)
plot(ml,which=1)
plot(ml,which=2)
res.aov <- aov(log(length)~category, data=new_data)
summary(res.aov)


# GRAPH 3 : typical number of mentions per article 
q <- ggplot(new_data, aes(x=method, y=per_typical, fill=category)) +
  geom_violin(position=position_dodge(1), trim=TRUE)+
  geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
  stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
  xlab("method of extraction") + 
  ylab("mentions per typical lengthed article") +
  scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
  scale_y_continuous(breaks = scales::pretty_breaks(n = 10))+
  theme_bw(base_size=15)

q

# significance of graph 3 
# assumptions a bit more iffy 
mq <- lm(sqrt(per_typical)~method*category, data=new_data)
plot(mq,which=1)
plot(mq,which=2)
res.aov <- aov(log(per_typical)~method*category, data=new_data)
summary(res.aov)

# GRAPH 4 - MENTIONS PER 1000 BY GENDER
n <- ggplot(new_data, aes(x=category, y=sqrt(per_1000), fill=gender)) +
  geom_violin(position=position_dodge(1), trim=TRUE)+
  geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
  stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
  xlab("category of article") + 
  ylab("sqrt number of mentions per 1000") +
  scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
  theme_bw()

n

n2 <- lm(sqrt(per_1000)~method*category*gender, data=data)

plot(n2,which=1)
plot(n2,which=2)

res.aov <- aov(sqrt(length)~method*category*gender, data=new_data)
summary(res.aov)


# GRAPH 5 - LENGTH OF ARTICLE BY GENDER
m <- ggplot(new_data, aes(x=category, y=log(length), fill=gender)) +
  geom_violin(position=position_dodge(1), trim=FALSE)+
  geom_boxplot(width=.1, position=position_dodge(1), show.legend=FALSE) +
  stat_summary(fun=mean, geom="point", shape=23, size=5, position=position_dodge(1), show.legend=FALSE)+
  xlab("category of article") + 
  ylab("log number of characters in article") +
  scale_fill_manual(values=c('#79CDCD', '#FF7F00'))+
  theme_bw()

m

m2 <- lm(log(length)~method*category*gender, data=data)

plot(m2,which=1)
plot(m2,which=2)

res.aov <- aov(log(length)~method*category*gender, data=new_data)
summary(res.aov)



