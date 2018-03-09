FROM ubuntu:16.04

MAINTAINER Erfan Sayyari <esayyari@ucsd.edu>

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	ca-certificates \
	curl \
        wget \
        git \
        ssh \
	&& rm -rf /var/lib/apt/lists/*


RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
    apt-get update && \
    apt-get -y install r-base r-base-dev





#RUN apt-get -y install libcurl4-openssl-dev
#setup R configs
RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.cnr.berkeley.edu/'; options(repos = r);" > ~/.Rprofile
RUN Rscript -e "install.packages('plyr',dependencies = TRUE)"
RUN Rscript -e "install.packages('reshape', dependencies = TRUE)"
RUN Rscript -e "install.packages('reshape2', dependencies = TRUE)"
RUN Rscript -e "install.packages('scales')"
RUN Rscript -e "install.packages('ggplot2', dependencies = TRUE)"
RUN Rscript -e "install.packages('ape', dependencies = TRUE)"
RUN Rscript -e "install.packages('optparse')"

# installing python and python dependencies
RUN apt-get install -y  python2.7 python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN pip install dendropy==4.3.0

# installing java jre and jdk 
RUN apt-get install -y default-jre default-jdk

#installing newick utilities

RUN mkdir /repository && \
    cd /repository && \
    wget http://cegg.unige.ch/pub/newick-utils-1.6-Linux-x86_64-enabled-extra.tar.gz && \
    tar xzvf newick-utils-1.6-Linux-x86_64-enabled-extra.tar.gz && \
    rm newick-utils-1.6-Linux-x86_64-enabled-extra.tar.gz && \
    cp newick-utils-1.6/src/nw_* /bin

# cloning to ASTRAL and DISCOVISTA

WORKDIR /repository

RUN git clone https://github.com/esayyari/DiscoVista.git;
COPY ASTRAL-DiscoVista.tar.gz /repository 
RUN  tar xzvf ASTRAL-DiscoVista.tar.gz; rm ASTRAL-DiscoVista.tar.gz; cd ./ASTRAL-DiscoVista/; \
	unzip Astral.4.10.12.zip; cp Astral/astral.4.10.12.jar .
#RUN   cd /reposiotry/ASTRAL; git checkout DiscoVista; unzip Astral.zip; cp Astral/astral.*jar .


ENV WS_HOME /repository
ENV PATH /repository/DiscoVista/src/utils:/repository/DiscoVista/src/R:$PATH
RUN mkdir /data


WORKDIR /data
