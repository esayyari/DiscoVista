#!/usr/bin/env Rscript

WS_HOME="/Users/erfan/Main/repository/"


reader = paste(WS_HOME,"/DiscoVista/src/R/reader.R", sep="")
source(reader)

setwd("/Users/erfan/Main/oasis/Insects/genes/")

print(getwd())

new.clades = read.csv("../newOrders.txt1",  sep="\t", header = F)


  MS = F
  ST = F
  cl=read.csv("../clade-defs.txt",header=T,sep="\t")
  names(cl)<-c("V1","V2","V3",names(cl)[4:length(cl)])
  depict = paste(WS_HOME,"/DiscoVista/src/R/main_depict_clades.R", sep="")
  source(depict)
  clade.order=c()
  
  
  data = read.data(file.all="clades.txt.res", file.hs="clades.hs.txt.res", clade.order=clade.order, new.clades = new.clades)
  mode = 1
  # if (mode == 0) {
  #   figuresizes = c(10.5,12)
  #   metatable(data$y,data$y.colors,data$countes,pages=c(1),raw.all=data$raw.all,figuresizes=figuresizes)
  # } else if (mode == 1) {
    data$countes.melted$M<-data$countes.melted$DS
    data$y$M<-data$y$DS
    
    data$y$M<-gsub(pattern = "FAA_", replacement="", x=data$y$M)
    data$y$Th<-data$y$M
    data$y$Th<-gsub(pattern = ".*_raxml",replacement ="RAxML",x=data$y$Th)
    data$y$Th[grep(pattern = "^RAxML",x=data$y$Th,invert=T)]<-"FastTree"
    data$y$M<-gsub(pattern = "_raxml",replacement="",x=data$y$M)
    
    data$countes.melted$M<-gsub(pattern = "FAA_", replacement="", x=data$countes.melted$M)
    data$countes.melted$Th<-data$countes.melted$M
    data$countes.melted$Th<-gsub(pattern = ".*_raxml",replacement ="RAxML",x=data$countes.melted$Th)
    data$countes.melted$Th[grep(pattern = "^RAxML",x=data$countes.melted$Th,invert=T)]<-"FastTree"
    data$countes.melted$M<-gsub(pattern = "_raxml",replacement="",x=data$countes.melted$M)
    
    data$countes.melted$M<-as.factor(data$countes.melted$M)
    data$countes.melted$Th<-as.factor(data$countes.melted$Th)
    data$y$M<-as.factor(data$y$M)
    data$y$Th<-as.factor(data$y$Th)
    
    sizes = c(12,6)
    
    pdf("figures/Monophyletic_Bargraphs_Porportion.pdf",width=sizes[1],height=sizes[2])
    xfont = 10
    titlefont = 12
    d.c.m<-data$countes.melted
    x = d.c.m[d.c.m$Classification != "Missing",]
    
    d.c.m.colors <- array(clade.colors[levels(droplevels(x$Classification))])
    levels(x$M) <- list("No-Filtering"="no_filtering","33% Filtering"="33","50% Filtering"="50","66% Filtering"="66")
    # x$M <- factor(x$M,levels=c("no_filtering","33","50","66"))
    x$Th<- factor(x$Th,levels=c("RAxML","FastTree"))
    p1 <- ggplot(x[x$M %in% c("No-Filtering","50% Filtering"),], aes(x=CLADE, y = value, fill=Classification) , main="Support for each clade") + xlab("") + ylab("Proportion of relevant gene trees") + 
      geom_bar(position="fill",stat="identity",colour="black") +
      facet_grid(M~Th,scales="free_y") + theme_bw()+ 
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



