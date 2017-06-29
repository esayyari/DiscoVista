#!/usr/bin/env Rscript

require(ape)


args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("Please send the tree file", call.=FALSE)
}

tree<-read.tree(args[1])

d<-dirname(args[1])
pdf(paste(d,"/tree.pdf",sep=""))
plot(tree, type = "phylogram",use.edge.length=F,edge.width = 5,edge.color="orange",root.edge = T); 
edgelabels(tree$edge.length, bg = "black",col="white", font=2)
dev.off()
