# Build Hybris
After the builder container is ready the Hybris runtime artefacts can be build. Hybris uses ant & gradle to build. The ant part was already executed during the creation of the builder container. Hybris provides a predefined set of Gradle recipes that help to simplify the build of Hybris. There are also some receipes that package the Hybris runtime artefacts in containers. 

### Recipes 
Hybris provides a list of [predefined recipes](https://help.sap.com/viewer/a74589c3a81a4a95bf51d87258c0ab15/1811/en-US/f09d46cf4a2546b586ed7021655e4715.html) that can be executed following the [Hybris build guide](https://help.sap.com/viewer/d0224eca81e249cb821f2cdf45a82ace/1811/en-US/9272c25c53f04eac8ffcdbb0f3affb64.html). 

For this deployment of Hybris on GKE an adapted version of a recipe has been created as a copy of b2c_acc_dockerized. This recipe can be found in the folder build/recipes.
This recipe is adapted to the specifics of the deployment on Kubernetes and GKE. The easiest way to build Hybris is to reuse this recipe and use the scripts located in the build folder to start the Hybris build tools (mainly gradle) and let them do their work fully automated. For this approach the existing cloud build configuration is perfect.

Alternatively, you can leverage the container to build any kind of recipe or execute other build steps. 


### Build Hybris
#### A) Using CloudBuild
There is a cloud build configuration available that builds Hybris using the predefined & customized recipe (b2c_acc_k8s) that is located under build/recipes. The CloudBuild can be started directly from the command line_

```
gcloud builds submit . --config BuildHybris/cloudbuild.yaml --async
```
Alternatively you can also define a trigger in CloudBuild that automatically build it once you update it in cloud source repositories. 


#### B) Manually Build Using Builder Container
In case the predefined recipe is not the suitable approach the builder container can be used to build any kind of Hybris recipe from within the container. Therefore the container is started with a few folders being mapped. The mapping of /var/run/docker allows to use docker within the container, which is required. 

```
docker run -it \
-v /var/run/docker.sock:/var/run/docker.sock \
-v $(pwd)/BuildHybris/config/:/gcphybris/conf/ \
-v $(pwd)/BuildHybris/build/:/gcphybris/build/ \
gcr.io/hybris-on-gcp/hybris-builder 
```

From within the container you can follow the Hybris configuration and installation guides to build the right recipes in the right way. 
Please also have a look at the provided scripts in the build folder and how they start a build via gradle. 
One example: Here is how the base_images recipse can be built:
```
/installer/install.sh -r base_images buildImages
```

After the build was successful and the build created new docker images these must be uploaded to the registry. Therefore they need to be tagged and pushed using docker commands. 
This example shows how this can be done for the hsql image:
```
docker tag b2cacc_deployment_hsql gcr.io/hybris-on-gcp/yacc_hsql
docker push gcr.io/hybris-on-gcp/yacc_hsql
```

### TODO
- Parameterize project_id in cloud build

