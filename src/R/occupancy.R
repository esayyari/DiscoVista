require(ggplot2)
require(reshape)
require(reshape2)
require(plyr)
require(scales)

clades<-read.csv(opt$annotation,sep='\t',header=F)
names(clades) <- c("Names","Clade")
dir.create('figures/')
oc <- read.csv('occupancy.csv',header=F,sep=' ')
names(oc)<-c("Seq","GENE_ID","model_condition", "Taxon","Len")
maxG = length(levels(oc$GENE_ID))

oc$ID <- apply( oc[ , c(1,3) ] , 1 , paste0 , collapse = "-" )
oc <- oc[,c(6,2,4,5)]
ocs <- ddply(oc, .(ID,GENE_ID), transform, rescale= scale(Len,center=F))
ocs$Taxon <- with(ocs, reorder(Taxon, Len, FUN = function(x) {return(length(which(x>0)))}))
ocs$ID <- with(ocs, reorder(ID, Len,FUN = length))

tc=recast(ocs[,c(1,2,3)],ID+Taxon~.); 
names(tc)[3]<-"occupancy"
tc$occupancy_prob <-tc$occupancy/maxG
tc$miss_prob <-1-tc$occupancy_prob

ocs3<-merge(ocs,clades,by.x="Taxon",by.y="Names")
tc_clades3<-dcast(data=ocs3,formula=GENE_ID+ID+Clade~.)
names(tc_clades3)[4]<-"num_clade_present"
tc_clades4<-dcast(tc_clades3[ ,2:4], 
                  ID+Clade~., fun.aggregate = 
                    function(x) (sum(x>0)/length(levels(tc_clades3$GENE_ID))))
names(tc_clades4)[3]<-c("clade_occupancy")




ocs <- ddply(oc, .(ID,GENE_ID), transform, rescale= scale(Len,center=F))
ocs$Taxon <- with(ocs, reorder(Taxon, Len, FUN = function(x) {return(length(which(x>0)))}))
ocs$ID <- with(ocs, reorder(ID, Len,FUN = length))

tc=recast(ocs[,c(1,3,4)],ID+Taxon~.); names(tc)[3]<-"occupancy"
tc2<-tc

if (! is.null(opt$modelCond)) {
  model = opt$modelCond 
  print(model)
  ocs2<-oc[oc$ID %in% c(model),]
  ocs2 <- dcast(ocs2,GENE_ID+Taxon~.,fun.aggregate=sum,value.var="Len")
  names(ocs2) <- c("GENE_ID","Taxon", "Len")


  ocs2 <- ddply(ocs2, .(GENE_ID), transform, rescale= scale(Len,center=F))
  ocs2$Taxon <- with(ocs2, reorder(Taxon, Len, FUN = function(x) {return(length(which(x>0)))}))
  ocs2$GENE_ID <- with(ocs2, reorder(GENE_ID, Len,FUN = length))

  pdf('figures/occupancy_map.pdf',width=24.5,height=11.7,compress=F)
  p1 <- ggplot(ocs2, aes(GENE_ID,Taxon)) + 
    geom_tile(aes(fill = rescale),colour = "white")+
    scale_fill_gradient(low = "white",high = "steelblue")+
    scale_x_discrete(expand = c(0, 0)) +
    scale_y_discrete(expand = c(0, 0) )+
    theme(legend.position = "none",axis.ticks = element_blank(),
        axis.text.x = element_text(size=2,angle = 90, hjust = 0, colour = "grey50"),
        axis.text.y = element_text(size=8,angle = 0, hjust = 0, colour = "grey50"))
  print(p1)
  
  dev.off()
}



pdf('figures/occupancy.pdf',width=23.8, height=11.4,compress=F)
p1 <- qplot(data=tc,
      x=reorder(Taxon,occupancy/maxG,FUN=median),y=occupancy/maxG,geom=c("line"),
      group=ID,color=ID)+theme_bw()+theme(legend.position = "bottom",axis.ticks = element_blank(),
      axis.text.x = element_text(size=16,angle = 90, hjust = 0, colour = "grey50"),
      legend.text=element_text(size=16),axis.text.y=element_text(size=16),text = element_text(size=16))+
  scale_y_continuous(labels = percent)+
  ylab('Occupancy')+xlab('Taxon')+scale_color_brewer(name="",palette = "Paired")
print(p1)
dev.off()

pdf('figures/occupancy_clades.pdf',width=23.8, height=11.4,compress=F)
p1 <- qplot(data=tc_clades4,reorder(Clade,clade_occupancy),clade_occupancy,
      geom="line",color=ID,group=ID)+theme_bw()+theme(legend.position = "bottom",
      axis.text.x = element_text(angle = 90, hjust = 1, vjust=0.5, colour = "grey50"))+
  xlab('Clades')+ylab('Percent')+scale_y_continuous(labels = scales::percent)+
  scale_color_brewer(name="",palette="Paired")
print(p1)

dev.off()









