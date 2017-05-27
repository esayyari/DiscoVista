setOptions <- function(opt) {
  if (is.null(opt$path)){
    print_help(opt_parser)
    stop("At least one argument must be supplied WS_HOME.", call.=FALSE)
  } else {
    WS_HOME1 = opt$path
  }

  if (is.null(opt$ST)){
    print_help(opt_parser)
    stop("Please specify wheather the stat file is for species trees (0) or gene trees (1).", call.=FALSE)
  } else {
    mode1 = as.integer(opt$ST)
    if ( as.integer(opt$ST) == 0 ) {
      ST1 = TRUE
    } else {
      ST1 = FALSE
    }
  }
  if ((mode1 == 0 || mode1 == 1) && is.null(opt$clade)){
    print_help(opt_parser)
    stop("Please specify the path to the clade definitions.", call.=FALSE)
  } else {
    clade1 = opt$clade
  }
  if ((mode1 == 0 || mode1 == 1 || mode1 == 4) && is.null(opt$annotation)){
    print_help(opt_parser)
    stop("Please specify the path to the annotation file.", call.=FALSE)
  } else {
    annotation1 = opt$annotation
  }

  if (is.null(opt$inputPath)){
    print_help(opt_parser)
    stop("Please specify the path to the input stat files")
  } else {
    input = opt$inputPath
    input1 = input
  }
  if (is.null(opt$missing)) {
  	MS = FALSE
  } else {
  	if(opt$missing == 1) {
  		MS = TRUE
  	} else {
		MS = FALSE
  	}
 }
  opt$missing = MS
  out1 = opt$inputPath
  opt$out = out1
  opt$mode = mode1
  opt$ST = ST1
  opt$WS_HOME = WS_HOME
  return(opt)
}
