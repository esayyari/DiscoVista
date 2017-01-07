require(reshape)
require(ggplot2)
require(reshape2)
require(plyr)
require(scales)


dir.create('figures/')

d<-read.csv('branchStats.csv',sep=" ",header=T)

cdat <- ddply(d, c("DS","model_condition"), summarise, mean_bl=mean(avgtaxonToTaxonBrLen),max_bl=mean(maxtaxonToTaxonBrLen),support=mean(avgBrSupp))


d1<-read.csv('branchSupport.csv',sep=' ',header=F)
cdat2 <- ddply(d1, c("V1","V2"), summarise, rating.mean=mean(V3))


pdf('figures/histogram_MLBS_distribution.pdf',width=30,height=15,compress=F)
p1 <- ggplot(d1, aes(V3,fill = V2))+
  geom_histogram(alpha=1,color = "black",size=0.05,binwidth=10,position="dodge",aes(y=..count../sum(..count..)))+facet_wrap(~V1)+
  theme_bw()+theme(legend.position="bottom",text = element_text(size=24),
                   axis.text.x = element_text(size=24,angle = 0),
                   axis.text.y = element_text(size=24,angle = 0),
                   legend.text=element_text(size=24))+ylab('percent')+
  scale_y_continuous(labels = percent)+
  scale_fill_brewer(name="",palette="Paired")+xlab('MLBS')+
  geom_vline(data=cdat2, aes(xintercept=rating.mean, colour=interaction(V2)),size=1,linetype="dashed")+
  scale_color_brewer(name="",palette = "Paired")
print(p1)
dev.off()



pdf('figures/average_taxa_distance_vs_MLBS.pdf',width=7,height=4.5,compress=F)
p1 <- qplot(data=cdat,mean_bl,support,color=model_condition)+facet_wrap(~DS)+geom_point(size=4)+
  theme_bw()+xlab('average taxa distance')+
  theme(legend.position="bottom",text = element_text(size=12),
        axis.text.x = element_text(size=12,angle = 0),
        axis.text.y = element_text(size=12,angle = 0),
        legend.text=element_text(size=12))+
  ylab('average bootstrap support (percent)')+
  scale_color_brewer(name='',palette='Paired')
print(p1)
dev.off()


pdf('figures/maximum_taxa_distance_vs_MLBS.pdf',width=7,height=4.5,compress=F)
p1 <- qplot(data=cdat,max_bl,support,color=model_condition)+facet_wrap(~DS)+geom_point(size=4)+
  theme_bw()+  theme(legend.position="bottom",text = element_text(size=12),
                     axis.text.x = element_text(size=12,angle = 0),
                     axis.text.y = element_text(size=12,angle = 0),
                     legend.text=element_text(size=12))+
  xlab('average maximum taxa distance')+ylab('average bootstrap support (percent)')+
  scale_color_brewer(name='',palette='Paired')+theme(legend.position="bottom")
print(p1)
dev.off()


