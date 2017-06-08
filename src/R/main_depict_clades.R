require(reshape)
require(plyr)
require(ggplot2)
require(scales)
print(getwd())
if (ST) {
  
  clade.colors <- c("Strong Support"="#1b9e77", 
                    "Weak Support"="#7570b3", 
                    "Compatible (Weak Rejection)"="#d95f02", 
                    "Strong Rejection"="#e7298a", 
                    "Missing"="#66a61e")
  
   clade.colors <- c("Strong Support"="#0073b6ff",
		     "Weak Support"="#00b5ecff",
		     "Compatible (Weak Rejection)"="#f5e526ff",
		     "Strong Rejection"="#f35e00ff",
		     "Missing"="#66a61e")
   if (MS) {
  	rename.c <- list(
    	"Strong Support"="IS_MONO-IS_MONO",
    	"Weak Support"="IS_MONO-CAN_MONO",
    	"Compatible (Weak Rejection)"="CAN_MONO-CAN_MONO", 
    	"Compatible (Weak Rejection)"="NOT_MONO-CAN_MONO", 
    	"Strong Rejection"="NOT_MONO-NOT_MONO",
    	"Weak Support"="IS_MONO_INCOMPLETE-CAN_MONO",
    	"Strong Support"= "IS_MONO_INCOMPLETE-IS_MONO_INCOMPLETE",
    	"Compatible (Weak Rejection)"="NOT_MONO-CAN_MONO_INCOMPLETE", 
    	"Missing"="NO_CLADE-NO_CLADE",
    	"Compatible (Weak Rejection)"="CAN_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE", 
    	"Weak Support"="IS_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE",
    	"Missing"="COMP_MISSING-COMP_MISSING")
   } else {
	rename.c <- list(
    	"Strong Support"="IS_MONO-IS_MONO",
	"Weak Support"="IS_MONO-CAN_MONO",
    	"Compatible (Weak Rejection)"="CAN_MONO-CAN_MONO",
    	"Compatible (Weak Rejection)"="NOT_MONO-CAN_MONO",
    	"Strong Rejection"="NOT_MONO-NOT_MONO",
    	"Missing"="IS_MONO_INCOMPLETE-CAN_MONO",
    	"Missing"= "IS_MONO_INCOMPLETE-IS_MONO_INCOMPLETE",
    	"Missing"="NOT_MONO-CAN_MONO_INCOMPLETE",
    	"Missing"="NO_CLADE-NO_CLADE",
    	"Missing"="CAN_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE",
    	"Missing"="IS_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE",
    	"Missing"="COMP_MISSING-COMP_MISSING")
   }
} else {
  clade.colors <- c("Strongly Supported/Complete"=rgb(50, 160, 45, max = 255), 
                    "Strongly Supported/Incomplete"=rgb(178, 223, 138, max = 255),
                    "Weakly Supported/Complete"=rgb(30, 120, 180, max = 255), 
                    "Weakly Supported/Incomplete"=rgb(160, 190, 225, max = 255),
                    "Weakly Reject"=rgb(255, 240, 170, max = 255),
                    "Strongly Reject"=rgb(230, 25, 26, max = 255), 
                    "Missing"=rgb(192, 192, 192, max = 255))
  rename.c <- list("Strongly Supported/Complete"="IS_MONO-IS_MONO", 
                   "Strongly Supported/Incomplete"= "IS_MONO_INCOMPLETE-IS_MONO_INCOMPLETE",
                   "Weakly Supported/Complete"="IS_MONO-CAN_MONO", 
                   "Weakly Supported/Incomplete"="IS_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE",
                   "Missing"="NO_CLADE-NO_CLADE",
                   "Missing"="COMP_MISSING-COMP_MISSING",
                   "Weakly Reject"="CAN_MONO-CAN_MONO", 
                   "Weakly Reject"="CAN_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE",
                   "Weakly Reject"="NOT_MONO-CAN_MONO", 
                   "Weakly Reject"="NOT_MONO-CAN_MONO_INCOMPLETE",
                   "Strongly Reject"="NOT_MONO-NOT_MONO")
  
  clade.colors <- c(
    "Strongly Supported"=rgb(50, 100, 130, max = 255), 
    #"Strongly Supported"=rgb(178, 223, 138, max = 255),
    "Weakly Supported"=rgb(100, 160, 250, max = 255), 
    #"Weakly Supported"=rgb(160, 190, 225, max = 255),
    "Weakly Reject"=rgb(255, 240, 170, max = 255),
    "Strongly Reject"=rgb(230, 25, 26, max = 255), 
    "Missing"=rgb(192, 192, 192, max = 255))
  
  rename.c <- list(
    "Strongly Supported"="IS_MONO-IS_MONO", 
    "Strongly Supported"= "IS_MONO_INCOMPLETE-IS_MONO_INCOMPLETE",
    "Weakly Supported"="IS_MONO-CAN_MONO", 
    "Weakly Supported"="IS_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE",
    "Missing"="NO_CLADE-NO_CLADE",
    "Missing"="COMP_MISSING-COMP_MISSING",
    "Weakly Reject"="CAN_MONO-CAN_MONO", 
    "Weakly Reject"="CAN_MONO_INCOMPLETE-CAN_MONO_INCOMPLETE",
    "Weakly Reject"="NOT_MONO-CAN_MONO", 
    "Weakly Reject"="NOT_MONO-CAN_MONO_INCOMPLETE",
    "Strongly Reject"="NOT_MONO-NOT_MONO")
}

cols <- c( "ID" , "CLADE", "BOOT")
#Read Raw files
 read.data <- function (file.all=paste(input, "/clades.txt.res", sep=""), file.hs=paste(input, "clades.hs.txt.res", sep=""), clade.order = NULL, new.clades = NULL, new.models = NULL, techs.order = NULL) {
  raw.all = read.csv(file.all,sep="\t", header=T)
  raw.highsupport = read.csv(file.hs,sep="\t", header=T)
  if (! is.null(techs.order)) {
    print("tech renaming...")
    raw.all$ID=factor(raw.all$ID,levels=techs.order)
    raw.highsupport$ID=factor(raw.highsupport$ID,levels=techs.order)
    #print (nrow(raw.all))
    #print (nrow(raw.highsupport))
    print("techs renamed!")
  }
  if (! is.null(clade.order)) {
    print("choosing clades...")
    raw.all = raw.all[which (raw.all$CLADE %in% clade.order),]
    raw.highsupport = raw.highsupport[which (raw.highsupport$CLADE %in% clade.order),]
    print("clades chosen!")
  }
  if (! is.numeric(raw.all$BOOT)){
    raw.all$BOOT <- as.numeric(levels(raw.all$BOOT))[raw.all$BOOT]		
  }
  print("bootstrap is numeric")
  raw.highsupport=raw.highsupport[,c(1,2,3,5)]
  # Merge 75% results and all results
  if (FALSE) {
    merged = merge(raw.all,raw.highsupport,c("ID","DS","CLADE"))
  } else {
    merged = cbind(raw.all[,c("ID","DS","CLADE","MONO","BOOT")],raw.highsupport[,c("MONO")])
  }
  names(merged)[4]<-"MONO"
  names(merged)[6]<-"MONO.75"
  print ("merging finished!")
  #print (nrow(merged))
  # Create counts table
  clade.counts=recast(merged,MONO+MONO.75~CLADE~DS,id.var=c("DS", "CLADE", "MONO", "BOOT", "MONO.75"),fill = NA_real_,fun.aggregate=length)
  #print (clade.counts)
  #d.c=d.c/sum(d.c[,1,1])
  countes.melted <- melt(clade.counts)
  names(countes.melted)[1] <- "Classification"
  levels(countes.melted$Classification) <- rename.c
  lo = levels(countes.melted$Classification)
  countes.melted$Classification <- factor(countes.melted$Classification)
  countes.melted <- melt(recast(countes.melted[complete.cases(countes.melted),], Classification ~ CLADE ~ DS, fill = NA_real_,fun.aggregate=sum))
  countes.melted <- subset(countes.melted, countes.melted$value != 0)
  countes.melted$Classification <- factor(countes.melted$Classification,levels=lo)
  # order clades based on support
  if (is.null(clade.order)) {
    all.monophyletic  <- raw.all[which(raw.all$MONO %in% c("IS_MONO","IS_MONO_INCOMPLETE") ),]
    all.monophyletic$CLADE = reorder(all.monophyletic$CLADE, all.monophyletic$MONO, FUN = function (x) {return (-length(x))})
    clade.order = c(levels(all.monophyletic$CLADE), setdiff(levels(countes.melted$CLADE), levels(all.monophyletic$CLADE)))
  }
  countes.melted$CLADE <- factor(countes.melted$CLADE, levels=clade.order)
  print ("working on counts ...")	
  
  
  # Add 75% and normal classifications, and reorder column
  y=merged
  y$Classification <- factor(paste(as.character(merged$MONO),as.character(merged$MONO.75),sep="-"))
  # ID DS CLADE MONO BOOT MONO.75 Classification
  #y=y[,c(1,2,3,7)]
  levels(y$Classification) <- rename.c
  y$Classification = factor(y$Classification)
  y.colors <- array(clade.colors[levels(y$Classification)])
  y$CLADE <- factor(y$CLADE, levels=rev(clade.order))

  if (! is.null(new.clades)) {
    print("reordering clades")
    old.orders <- as.character(as.vector(t(new.clades)[,1]))
    modified.orders <- as.character(as.vector(t(new.clades)[,2]))

    
    raw.all$CLADE <- factor(raw.all$CLADE, levels = old.orders)
    raw.highsupport$CLADE <- factor(raw.highsupport$CLADE, levels = old.orders)
    y$CLADE <- factor(y$CLADE, levels = old.orders)  
    countes.melted$CLADE <- factor(countes.melted$CLADE, levels = old.orders)  
   for (i in 1:length(levels(raw.all$CLADE))) {
        levels(raw.all$CLADE)[levels(raw.all$CLADE) == old.orders[i]] <- modified.orders[i]
        levels(y$CLADE)[levels(y$CLADE) == old.orders[i]] <- modified.orders[i]

        levels(countes.melted$CLADE)[levels(countes.melted$CLADE) == old.orders[i]] <- modified.orders[i]
        levels(raw.highsupport$CLADE)[levels(countes.melted$CLADE) == old.orders[i]] <- modified.orders[i]
    } 
#    mapvalues(raw.all$CLADE, from = levels(factor(old.orders)), to = levels(factor(modified.orders)))
 #   mapvalues(raw.highsupport$CLADE, from = levels(factor(old.orders)), to = levels(factor(modified.orders)))
  #  mapvalues(y$CLADE, from = levels(factor(old.orders)), to =levels(factor( modified.orders)))
#    mapvalues(countes.melted$CLADE, from = levels(factor(old.orders)), to = levels(factor(modified.orders)))


    raw.all$CLADE <- factor(raw.all$CLADE, levels = rev(modified.orders))
    raw.highsupport$CLADE <- factor(raw.highsupport$CLADE, levels = rev(modified.orders))
    y$CLADE <- factor(y$CLADE, levels = rev(modified.orders))
    countes.melted$CLADE <- factor(countes.melted$CLADE, levels = modified.orders)
   
    
    print("clades reordered!")
  }
  if (! is.null(new.models)) {

    print("renaming and reordering model conditions ...")
    old.orders <- as.vector(t(new.models)[,1])
    modified.orders <- as.vector(t(new.models)[,2])

    raw.all$ID <- factor(raw.all$ID, levels = old.orders)
    raw.highsupport$ID <- factor(raw.highsupport$ID, levels = old.orders)
    y$ID <- factor(y$ID, levels = old.orders)
    

    for (i in 1:length(levels(raw.all$ID))) {
        levels(raw.all$ID)[levels(raw.all$ID) == old.orders[i]] <- modified.orders[i]
        levels(y$ID)[levels(y$ID) == old.orders[i]] <- modified.orders[i]
    }
    raw.all$ID <- factor(raw.all$ID, levels = as.character(modified.orders), exclude = NULL, ordered =TRUE)
    y$ID <- factor(y$ID, levels = as.character(modified.orders), exclude = NULL, ordered =TRUE)
    print("model conditions reordered!")
  }
  return (list (y=y, countes=clade.counts, countes.melted=countes.melted, raw.all = raw.all, y.colors=y.colors))
}

metabargraph2 <- function (d.c.m, y,sizes=c(15,19)){
  
  pdf("Monophyletic_Bargraphs_Porportion.pdf",width=sizes[1],height=sizes[2])
  xfont = 10
  titlefont = 12
  x = d.c.m[d.c.m$Classification != "Missing",]
  d.c.m.colors <- array(clade.colors[levels(droplevels(x$Classification))])
  p1 <- ggplot(x, aes(x=CLADE, y = value, fill=Classification) , main="Support for each clade") + xlab("") + ylab("Proportion of relevant gene trees") + 
    geom_bar(position="fill",stat="identity",colour="black") + facet_wrap(~DS,scales="free_y",ncol=1) + theme_bw()+ 
    theme(axis.text.x = element_text(size=xfont,angle = 90,hjust=1),axis.text.y = element_text(size=xfont, hjust=1), legend.position="bottom", legend.direction="horizontal", legend.text = element_text(size=xfont),axis.title=element_text(size=titlefont)) + 
    scale_fill_manual(name=element_blank(), values=d.c.m.colors)  + scale_x_discrete(drop=FALSE)
  
  print(p1)
  dev.off()
}

metabargraph <- function (d.c.m, y,sizes=c(15,19)){
  
  pdf("Monophyletic_Bargraphs.pdf",width=sizes[1],height=sizes[2])
  d.c.m.colors <- array(clade.colors[levels(droplevels(d.c.m$Classification))])
  p1 <- ggplot(d.c.m, aes(x=CLADE, fill=Classification) , main="Support for each clade") + xlab("") + ylab("Number of Gene Trees") + 
    geom_bar(aes(y = value),stat="identity",colour="black") + facet_wrap(~DS,scales="free_y",ncol=1) + theme_bw()+ 
    theme(axis.text.x = element_text(size=10,angle = 90,hjust=1),legend.position="bottom", legend.direction="horizontal") + 
    scale_fill_manual(name=element_blank(), values=d.c.m.colors)  + scale_x_discrete(drop=FALSE)
  
  print(p1)
  dev.off()
  
  for ( ds in levels(droplevels(y$DS))) {
    write.csv(file=paste(ds,"counts","csv",sep="."),cast(d.c.m[which(d.c.m$DS == ds),c(1,2,4)],CLADE~Classification))
    print(ds)
    for ( clade in levels(y$CLADE)) {
      q <- y[which(y$CLADE == clade & y$DS ==ds),] 
      write.csv(file=paste("finegrained/clades",ds,gsub("/",",",clade),"csv",sep="."),q, row.names=F)
    }
  } 
  
}

metahistograms<- function (d.boot) {
  print(levels(d.boot$DS))
  pdf("Monophyletic_Bootstrap_Support.pdf",width=18,height=18)
  o <- theme(strip.text.x = element_text(size = 9))
  Main="Distribution of Support for each Clade When Monophyletic and Complete"
  for (l in levels(d.boot$DS)){		
    d.boot.mono  <- d.boot[which(d.boot$MONO == "IS_MONO" & d.boot$DS == l & !is.na(d.boot$BOOT)),]
    d.boot.mono$CLADE = reorder(d.boot.mono$CLADE, d.boot.mono$MONO, FUN = function (x) {return (-length(x))})
    p1 <- qplot(BOOT,data=d.boot.mono,binwidth=5, main = paste(Main," (", l, ")"), xlab="Bootstrap Support")+facet_wrap(~CLADE,scales="free_y") + o
    print(p1)
  }
  
  Main="Distribution of Support for each Clade When Monophyletic but Potentially Incomplete"
  for (l in levels(d.boot$DS)){
    d.boot.mono  <- d.boot[which(d.boot$MONO %in% c("IS_MONO","IS_MONO_INCOMPLETE") & d.boot$DS == l  & !is.na(d.boot$BOOT)),]
    d.boot.mono$CLADE = reorder(d.boot.mono$CLADE, d.boot.mono$MONO, FUN = function (x) {return (-length(x))})
    p1 <- qplot(BOOT,data=d.boot.mono,binwidth=5, main = paste(Main," (", l, ")"), xlab="Bootstrap Support")+facet_wrap(~CLADE,scales="free_y") + o
    print(p1)
  }
  dev.off()	
}

metahistograms2<- function (d.boot) {
  print(levels(d.boot$DS))
  pdf("Monophyletic_Bootstrap_Support_2.pdf",width=18,height=18)
  o <- theme_bw()+theme(strip.text.x = element_text(size = 9),legend.position="bottom")
  
  Main="Distribution of Support for each Clade When Monophyletic but Potentially Incomplete"
  d.boot.mono  <- d.boot[which(d.boot$MONO %in% c("IS_MONO","IS_MONO_INCOMPLETE")  & !is.na(d.boot$BOOT)),]
  #d.boot.mono$CLADE = reorder(d.boot.mono$CLADE, d.boot.mono$MONO, FUN = function (x) {return (-length(x))})
  p1 <- qplot(DS,BOOT,data=d.boot.mono,geom="jitter", alpha=0.5, colour=DS,  main = Main, xlab="Bootstrap Support")+facet_wrap(~CLADE,scales="free_y") + o
  print(p1)
  dev.off()	
}
metatable <- function (y,y.colors,c.counts,pages=1:3, figuresizes=c(5,15),raw.all){
  print(levels(y$DS))
  # Draw the block driagram
  for ( ds in levels(y$DS)) {
    
    pdf(paste(ds,"block","pdf",sep="."),width=figuresizes[1],height=figuresizes[2])
    #png(paste(ds,"block","png",sep="."),width=2000,height=2000)#,width=figuresizes[1],height=figuresizes[2])
    
    op <- theme(axis.text.x = element_text(size=10,angle = 90,hjust=1),
                legend.position="bottom",axis.text.y = element_text(hjust=1))
    if (1 %in% pages) {			
      p1 <- qplot(ID,CLADE,data=y,fill=Classification,geom="tile",xlab="",ylab="")+ 
        scale_x_discrete(drop=FALSE) + scale_y_discrete(drop=FALSE) +
        scale_fill_manual(name="Classification", values=y.colors) + theme_bw() + op
      print(p1)
      
    }
    
    if (2 %in% pages){
      # find clades with no suport
      l=melt(c.counts["IS_MONO-IS_MONO",,ds]+c.counts["IS_MONO-CAN_MONO",,ds])
      nosup = row.names(l)[which(l$value==0)] 		
      y.d <- y[which(y$DS == ds),c(1,3,4)] 
      y.d.r = y.d[which (!y.d$CLADE %in% nosup),]
      y.d.r$CLADE = factor(y.d.r$CLADE)
      p2 <- qplot(ID,CLADE,data=y.d.r,fill=Classification,geom="tile",xlab="",ylab="")+ 
        scale_fill_manual(name="Classification", values=y.colors) + theme_bw() + op
      
      
      print(p2)
    }
    
    if (3 %in% pages) {
      l=melt(c.counts["IS_MONO-IS_MONO",,ds])
      losup = row.names(l)[which(l$value==0)] 		
      y.d.rr = y.d[which (!y.d$CLADE %in% losup),]
      y.d.rr$CLADE = factor(y.d.rr$CLADE)
      
      p3 <- qplot(ID,CLADE,data=y.d.rr,fill=Classification,geom="tile",xlab="",ylab="")+ 
        scale_fill_manual(name="Classification", values=y.colors)+ theme_bw() + op 
      
      
      print(p3)
    }
    dev.off()
    if (MS) {
	db = raw.all[raw.all$MONO %in% c("IS_MONO","IS_MONO_INCOMPLETE"),]
    } else {
	db=raw.all[raw.all$MONO=="IS_MONO",]
    }
    dbc=y[which(y$Classification=="Compatible (Weak Rejection)"),c(1:3)]
    dbn=y[which(y$Classification=="Strong Rejection"),c(1:3)]
    dbc$BOOT <- rep(-50, nrow(dbc))
    dbn$BOOT <- rep(-100, nrow(dbn))
    db2=rbind(dbn[,cols],dbc[,cols],db[,cols]);
    print("here2")
    print(db2$BOOT)
    #db2$CLADE <- factor(db2$CLADE, levels=rev(clade.order))
    nrow(db2)
    pdf(paste(ds,"block-shades","pdf",sep="."),width=figuresizes[1],height=figuresizes[2]) 
    if(nrow(dbn) == 0 && nrow(dbc)!= 0) {
	c<-scale_fill_gradientn(na.value="white",colours=c("#257070","#459090","#599590","#69a1a0","#DDEEFF","#ec7f98"),values=rescale((c(100,99,90,50,0,-50))))
    } else if(nrow(dbn) == 0 && nrow(dbc) == 0) {
	c<-scale_fill_gradientn(na.value="white",colours=c("#257070","#459090","#599590","#69a1a0","#DDEEFF"),values=rescale((c(100,99,90,50,0))))
    } else if(nrow(dbn) != 0 && nrow(dbc) !=0 ) {
    	c<-scale_fill_gradientn(na.value="white",colours=c("#257070","#459090","#599590","#69a1a0","#DDEEFF","#ec7f98","#c84060"),values=rescale((c(100,99,90,50,0,-50,-100))))
    } else {
    
       c<-scale_fill_gradientn(na.value="white",colours=c("#257070","#459090","#599590","#69a1a0","#DDEEFF","#c84060"),values=rescale((c(100,99,90,50,0,-100))))
    }
    p1 <- qplot(ID,CLADE,data=db2,fill=BOOT,geom="tile",xlab="",ylab="")+
      scale_x_discrete(drop=FALSE) + scale_y_discrete(drop=FALSE)+c+
      #scale_fill_gradientn(na.value="white",colours=c("#257070","#459090","#599590","#69a1a0","#DDEEFF","#ec7f98","#c84060")),values=rescale(rev(c(100,99,90,50,0,-50,-100))))+ 
      #scale_fill_gradientn(limits = c(-100,100), colours=c("#c84060","#ec7f98","#DDEEFF","#69a1a0","#257070"),na.value="white")+
      theme_classic() + theme(axis.text.x = element_text(size=10,angle = 90,hjust=1),
                         axis.text.y = element_text(hjust=1))+theme(legend.position="bottom")
    print(p1)
    dev.off()
    write.csv(file=paste(ds,"metatable.results","csv",sep="."),cast(y,ID~CLADE))		
  }
}


metabargraph1 <- function (d.c.m, y,sizes=c(15,19)){
  
  pdf("Monophyletic_Bargraphs.pdf",width=sizes[1],height=sizes[2])
  d.c.m.colors <- array(clade.colors[levels(droplevels(d.c.m$Classification))])
  p1 <- ggplot(d.c.m, aes(x=DS, fill=Classification) , main="Support for each clade") + xlab("") + ylab("Clade") + 
    geom_tile(aes(y = as.factor(CLADE)),stat="identity",colour="black") + facet_wrap(~CLADE,scales="free_y",ncol=1) + theme_bw()+ 
    theme(strip.background = element_blank(),strip.text.y = element_blank(),axis.ticks.x=element_blank(),axis.ticks.y=element_blank(),
          strip.text.x = element_blank(),axis.text.x = element_text(size=10,angle = 90,hjust=1),legend.position="left", legend.direction="vertical") + 
    scale_fill_manual(name=element_blank(), values=d.c.m.colors,na.value="transparent")  + scale_x_discrete(drop=FALSE)
  
  print(p1)
  dev.off()
  
}
