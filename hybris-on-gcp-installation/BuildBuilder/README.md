# Build the Builder
To simplify and automate the installation process the build activities will be executed within a dedicated container. Therefore the first step is to create the image of the builder container that contains all the installation files and necessary dependencies. This can be created using Google CloudBuild or locally using docker. 

### A) Using CloudBuild
There is a cloud build configuration available that builds the BuilderContainer using Google CloudBuild. This can either be used in combination with source repositories to create an automated CloudBuild or alternatively it can be submitted directly via the respective gcloud command:
```
gcloud builds submit . --config BuildBuilder/cloudbuild.yaml --async
```

Alternatively you can also define a trigger in CloudBuild that automatically build it once you update it in cloud source repositories. 

### B) Using Docker
In order to build the docker container locally the hybris installation files need to be placed in the inst-files folder and described [here](BuildBuilder/inst-files/README.md). Afterwards the docker build can be executed and the image can be pushed to Cloud Container Registry.

```
docker build -t gcr.io/$(PROJECT_ID)/hybris-builder .
docker push  gcr.io/$(PROJECT_ID)/hybris-builder
```

### TODOs
- parameterize project id in cloudbuild.yaml
- gcloud builds submit currently fails / trigger works