#!/usr/bin/env Rscript

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
              help="Model Condition that occupancy map will be plotted.")
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


mode = opt$mode
print(mode)
if (opt$mode == 0 || opt$mode == 1 ) {
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
  data = read.data(file.all="clades.txt.res", file.hs="clades.hs.txt.res", clade.order=clade.order)
  print(cl)
  if (mode == 0) {
    print("here")
    metatable(data$y,data$y.colors,data$countes,pages=c(1),raw.all=data$raw.all)
  } else if (mode == 1) {
    metabargraph(data$countes.melted,data$y,sizes=c(12.5,15))
    metabargraph2(data$countes.melted,data$y,sizes=c(12.5,15))
    metahistograms2(data$raw.all)
    sizes = c(12.5,15)
    pdf("Monophyletic_Bargraph2.pdf",width=sizes[1],height=sizes[2])
    p<-ggplot(data$countes.melted, aes(x = DS, y = value)) + 
       geom_bar(stat="identity") + 
      aes(fill = Classification)+facet_wrap(~CLADE)
    theme(axis.text.x = element_text(angle = 45))
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



