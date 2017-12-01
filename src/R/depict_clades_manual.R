#!/usr/bin/env Rscript

WS_HOME="/Users/erfan/Main/repository/"


reader = paste(WS_HOME,"/DiscoVista/src/R/reader.R", sep="")
source(reader)

setwd("/Users/erfan/Main/oasis/1KP-new/speciestrees/output-small4")

print(getwd())

new.orders = read.csv("../../parameters/newsporder.txt",  sep="\t", header = F)


MS = T
ST = T
cl=read.csv("../../parameters//clade-defs.txt",header=T,sep="\t")
names(cl)<-c("V1","V2","V3",names(cl)[4:length(cl)])
depict = paste(WS_HOME,"/DiscoVista/src/R/main_depict_clades-temp.R", sep="")
source(depict)
clade.order=c()l
cladeorder<-read.csv("../../parameters/cladeorder.txt",header=F,sep="\t")

data = read.data(file.all="clades.txt.res", file.hs="clades.hs.txt.res", clade.order=NULL, new.clades = cladeorder, new.models=new.orders)
data$y[!is.na(data$y$BOOT) &data$y$BOOT>100, ]$BOOT<-data$y[!is.na(data$y$BOOT) &data$y$BOOT>100, ]$BOOT/100
data$raw.all[!is.na(data$raw.all$BOOT) &data$raw.all$BOOT>100, ]$BOOT<-data$raw.all[!is.na(data$raw.all$BOOT) &data$raw.all$BOOT>100, ]$BOOT/100
tn = levels((data$y$ID))
mode = 0
# if (mode == 0) {
#data$raw.all$ID<-factor(data$raw.all$ID,levels=tn[c(7,5,8,6, 12,9,   3,4,14,11, 1,2,13,10)])

#data$y$ID <-factor(data$y$ID,levels=tn[c(1,9,10,11,7,5,8,6,17,14,3,4,19,16,12,2,18,15,13)])
#data$raw.all$ID<-factor(data$raw.all$ID,levels=tn[c(1,9,10,11,7,5,8,6,17,14,9,10,11,3,4,19,16,12,2,18,15,13)])
figuresizes = c(10,12)
metatable(data$y,data$y.colors,data$countes,pages=c(1),raw.all=data$raw.all,figuresizes=figuresizes)
# } else if (mode == 1) {

data$countes.melted$M<-data$countes.melted$DS
data$y$M<-data$y$DS

# data$y$M<-gsub(pattern = "FNA2AA_", replacement="", x=data$y$M)
# data$y$Th<-data$y$M
# data$y$Th<-gsub(pattern = ".*_raxml",replacement ="RAxML",x=data$y$Th)
# data$y$Th[grep(pattern = "^RAxML",x=data$y$Th,invert=T)]<-"FastTree"
# data$y$M<-gsub(pattern = "_raxml",replacement="",x=data$y$M)
# 
# data$countes.melted$M<-gsub(pattern = "FNA2AA_", replacement="", x=data$countes.melted$M)
# data$countes.melted$Th<-data$countes.melted$M
# data$countes.melted$Th<-gsub(pattern = ".*_raxml",replacement ="RAxML",x=data$countes.melted$Th)
# data$countes.melted$Th[grep(pattern = "^RAxML",x=data$countes.melted$Th,invert=T)]<-"FastTree"
# data$countes.melted$M<-gsub(pattern = "_raxml",replacement="",x=data$countes.melted$M)
# 
data$countes.melted$M<-as.factor(data$countes.melted$M)
data$countes.melted$Th<-as.factor(data$countes.melted$Th)
data$y$M<-as.factor(data$y$M)
data$y$Th<-as.factor(data$y$Th)

sizes = c(6,12)

pdf("Monophyletic_Bargraphs_Porportion.pdf",width=sizes[1],height=sizes[2])
xfont = 10
titlefont = 12
d.c.m<-data$countes.melted
x = d.c.m[d.c.m$Classification != "Missing",]

d.c.m.colors <- array(clade.colors[levels(droplevels(x$Classification))])
levels(x$M) <- list("No-Filtering"="no_filtering","33% Filtering"="33","50% Filtering"="50","66% Filtering"="66")
# x$M <- factor(x$M,levels=c("no_filtering","33","50","66"))
x$Th<- factor(x$Th,levels=c("RAxML","FastTree"))
p1 <- ggplot(x, aes(x=CLADE, y = value, fill=Classification) , main="Support for each clade") + xlab("") + ylab("Proportion of relevant gene trees") + 
  geom_bar(position="fill",stat="identity",colour="black") +
  facet_grid(DS~.,scales="free_y") + 
  theme_bw()+ 
  geom_hline(aes(yintercept=.25),size=0.8,color="red")+
  geom_hline(aes(yintercept=.5),size=0.8,color="red")+
  theme(axis.text.x = element_text(size=xfont,angle = 90,hjust=1,color="black")
        ,axis.text.y = element_text(size=10, hjust=1,color="black"), 
        legend.position="bottom", legend.direction="horizontal",
        legend.text = element_text(size=14),
        axis.title=element_text(size=14)) + 
  scale_fill_manual(name=element_blank(), values=d.c.m.colors)  + 
  scale_x_discrete(drop=FALSE)

print(p1)
dev.off()



