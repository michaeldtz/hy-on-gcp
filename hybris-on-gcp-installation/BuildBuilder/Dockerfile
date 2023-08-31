FROM marketplace.gcr.io/google/ubuntu1804
LABEL maintainer="midietz@google.com"

# Parameters
ARG USER_HOME_DIR="/root"

### Basics 
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install unzip
RUN apt-get -y install vim

### JDK8
RUN apt-get -y install openjdk-11-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/

### Maven
RUN apt-get -y install maven

ENV M2_HOME /usr/share/maven
ENV M2 /usr/share/maven/bin
ENV PATH ${PATH}:${M2_HOME}/bin

RUN mkdir $USER_HOME_DIR/.m2
ENV MAVEN_CONFIG $USER_HOME_DIR/.m2

### Docker
RUN apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get -y install docker-ce docker-ce-cli containerd.io

### Ant
RUN apt-get -y install ant

### Google Cloud SDK
RUN echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -c -s) main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update && apt-get -y install google-cloud-sdk

ENV ANT_HOME /usr/share/ant
ENV PATH ${PATH}:${ANT_HOME}/bin

### Create download folder
RUN mkdir /gcphybris
RUN mkdir /gcphybris/inst/
RUN mkdir /gcphybris/supp/
RUN mkdir /gcphybris/dep/
RUN mkdir /gcphybris/conf/

### Copy files and extract
COPY inst-files/.       /gcphybris/inst/.
COPY dependencies/.     /gcphybris/dep/.
COPY config/.           /gcphybris/conf/.
#COPY build/.           /gcphybris/build/.

### Check if files are there and / or gstuil them
RUN unzip -q -d /        /gcphybris/inst/CXCMR.ZIP
RUN unzip -q -d /        /gcphybris/inst/CXCOMM.ZIP
RUN unzip -q -d /hybris/ /gcphybris/inst/CONFIG.ZIP

### Build via ANT
RUN cd /hybris/bin/platform && . ./setantenv.sh
RUN cd /hybris/bin/platform && ant clean all

### Insert Central Configs 
RUN cat /gcphybris/conf/*.properties >> /installer/customconfig/custom.properties

WORKDIR /
ENTRYPOINT [ "/bin/bash" ]


