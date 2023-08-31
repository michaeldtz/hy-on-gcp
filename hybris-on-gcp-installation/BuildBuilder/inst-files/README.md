# Hint
For local builds with docker copy the hybris installation files here
There should be the following files
- CXCMR.ZIP
- CXDATAHUB.ZIP
- CXCOMM.ZIP
- CONFIG.ZIP


The config file contains all the content of the /hybris/config folder. This folder is created with a very first ant build. 
If you dont have the content then you have to run an initial ant build 
```
cd /hybris/bin/platform && . ./setantenv.sh
cd /hybris/bin/platform && ant clean all
```