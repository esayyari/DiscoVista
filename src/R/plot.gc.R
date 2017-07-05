require(ggplot2)
require(reshape2)
require(reshape)
require(plyr)
f = read.csv("gc-stat.csv",sep=" ")
fall=f[,c(1,2,3,10,11,12,13)]
fall$GC<-fall[,5]+fall[,6]
fdall = melt(fall,id=c("GENE","SEQUENCE","TAXON"))
levels(fdall$variable)<-c("A","C","G","T","GC")

dir.create('figures', showWarnings = F)

fcg<-f[,c(1,2,3)]
fcg$ALL<-f[,11]+f[,12]
fcg$C1<-f[,21]+f[,22]
fcg$C2<-f[,31]+f[,32]
fcg$C3<-f[,41]+f[,42]
fcg=melt(fcg,id=c("GENE","SEQUENCE","TAXON"))

tc=dcast(data=fcg[],formula=SEQUENCE+variable~.,fun.aggregate=mean)

names(tc)<-c("SEQUENCE","variable","value")

pdf("figures/pTpP_GC_point.pdf",width=12,height=5)
p <- qplot(reorder(SEQUENCE,value),value,data=tc,geom="point", color=variable,
           group=variable,xlab="")+
  theme(axis.text.x = element_text(angle = 90, hjust=1))+scale_color_brewer(name="",palette = "RdBu")
print(p)
dev.off()

pdf("figures/pTpP_GC_boxplot.pdf",width=12,height=5)

p<-ggplot(aes(as.factor(reorder(SEQUENCE,value)),value),data=fcg)+
  geom_boxplot(outlier.size=0.3,outlier.alpha = 0.1)+xlab("")+ylab("GC content")+ 
  theme(axis.text.x = element_text(angle = 90,hjust=1),
        panel.background = element_rect(fill ='#fbe4d8ff'),
        strip.background = element_rect(fill="#f0ac86f8"))+
  facet_grid(variable~., scales = "free")

print(p)
dev.off()
