#!/usr/bin/env Rscript
options(error=traceback)
options(show.error.locations = TRUE)

library("optparse")
option_list = list(
  make_option(c("-p", "--path"), type="character", default=NULL, 
              help="WS_HOME", metavar="character"),
  make_option(c("-s", "--ST"), type="integer", default=NULL,
              help="Type of data stats, it could be species tree (0), or gene tree (1)"),
  make_option(c("-c","--clade"), type="character", default=NULL,
              help="Clade definition file"),
  make_option(c("-i", "--inputPath"), type="character", default=NULL,
              help="The path to the stat files direcotry"),
  make_option(c("-a", "--annotation"), type="character", default=NULL,
              help="Annotation file"),
  make_option(c("-x", "--modelCond"), type="character", default=NULL,
              help="Model Condition that occupancy map will be plotted."),
  make_option(c("-t", "--cladeOrder"), type="character", default=NULL,
	     help="The file to define new clade names and orders."),
  make_option(c("-y", "--modelCondOrder"), type="character", default=NULL,
	     help="The file to define order of model conditions."),
  make_option(c("-m", "--missing"), type = "integer", default=NULL,
	     help="Indicates if considering partially missing data as complete or not.")
);
opt_parser = OptionParser(option_list=option_list);
optTmp = parse_args(opt_parser)
if (is.null(optTmp$path)){
  print_help(opt_parser)
  stop("At least one argument must be supplied WS_HOME.", call.=FALSE)
} else {
  WS_HOME = optTmp$path
}


reader = paste(WS_HOME,"/DiscoVista/src/R/reader.R", sep="")
source(reader)

currOpt = setOptions(optTmp)
opt = currOpt
setwd(opt$out)

print(getwd())
if(!is.null(opt$cladeOrder)){
  new.clades = read.csv(opt$cladeOrder, sep="\t", header=F)
} else {
  new.clades = NULL
}
if(!is.null(opt$modelCondOrder)){
  new.models = read.csv(opt$modelCondOrder,  sep="\t", header = F)
} else {
  new.models = NULL
}
mode = opt$mode
print(mode)
if (opt$mode == 0 || opt$mode == 1 ) {
  MS = opt$missing
  ST = opt$ST
  cl=read.csv(opt$clade,header=T,sep="\t")
  names(cl)<-c("V1","V2","V3",names(cl)[4:length(cl)])
  depict = paste(WS_HOME,"/DiscoVista/src/R/main_depict_clades.R", sep="")
  source(depict)
  clade.order=c()
  
  for (x in levels(cl$V3)) {
    if (x != "None") {
      clade.order=c(clade.order,paste("[",x,"]"))
      clade.order=c(clade.order,as.vector(paste(cl[cl$V3==x,1],
                                                sapply(cl[cl$V3==x,4],function (x) if (x!="" & !is.na(x)) paste(" (",x,")",sep="") else ""),sep="")))
    }
  }
  data = read.data(file.all="clades.txt.res", file.hs="clades.hs.txt.res", clade.order=clade.order, new.clades = new.clades, new.models = new.models)
  if (mode == 0) {
    metatable(data$y,data$y.colors,data$countes,pages=c(1),raw.all=data$raw.all)
  } else if (mode == 1) {
    sizes = c(12.5,6)
    metabargraph(data$countes.melted,data$y,sizes=sizes)
    metabargraph2(data$countes.melted,data$y,sizes=sizes)
    metahistograms2(data$raw.all)
    pdf("Monophyletic_Bargraph2.pdf",width=sizes[1],height=sizes[2])
    p<-ggplot(data$countes.melted, aes(x = DS, y = value)) + 
       geom_bar(stat="identity") + 
      aes(fill = Classification)+facet_wrap(~CLADE)
    theme(axis.text.x = element_text(angle = 45))+theme_classic()
    print(p)
    dev.off()
  }
} else if (opt$mode == 2) {
  gcplot = paste(opt$WS_HOME,"/DiscoVista/src/R/plot.gc.R", sep="")
  source(gcplot)
} else if (opt$mode == 3) {
  occupancy = paste(opt$WS_HOME,"/DiscoVista/src/R/occupancy.R", sep="")
  source(occupancy)
} else if (opt$mode == 4) {
  branchStat = paste(opt$WS_HOME,"/DiscoVista/src/R/branchStat.R", sep="")
  source(branchStat)
}



