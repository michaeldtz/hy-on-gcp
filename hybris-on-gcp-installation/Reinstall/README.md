# Hybris Reinstallation on GCP 

Hybris is equipped with a 30 day trial license. As soon as these 30 days are over the system has to be rebuilt from scratch and redeployed. This guide gives the steps to achieve this:

* Run the CloudBuild trigger named "Build Hybris-Builder" here and wait until finished. https://pantheon.corp.google.com/cloud-build/triggers?project=hybris-on-gcp 
* Run the CloudBuild trigger named "Build Hybris Artefacts" here and wait until finsihed. https://pantheon.corp.google.com/cloud-build/triggers?project=hybris-on-gcp
* cd into the folder hybris-on-gcp-installation and execute the following commands to delete the current deplyoments and services:
* Set the right project and get the GKE configuration
```
kubectl delete -f Deployment/a3_hybris_hac.yaml
kubectl delete -f Deployment/a3_hybris_storefront.yaml 
kubectl delete -f Deployment/a3_hybris_backoffice.yaml 
```
* Deploy the Hybris Initiailization and watch the logs to be sure when it is finished (takes about 20 minutes):
```
kubectl apply -f Deployment/a2_platform_init.yaml
kubectl logs -f $(kubectl get pod --selector="app=hybris-admin-init"  --output jsonpath='{.items[0].metadata.name}') -c hybris-admin-init
```
* After Finish you can delete the Hybris Initiailization container and deploy the full set of Hybris services:
```
kubectl delete -f Deployment/a2_platform_init.yaml
kubectl apply -f Deployment/a3_hybris_hac.yaml
kubectl apply -f Deployment/a3_hybris_storefront.yaml 
kubectl apply -f Deployment/a3_hybris_backoffice.yaml 
```
* As soon as HAC is up and running you can log in and run the following import statement:
```
UPDATE CMSSite;uid[unique=true];urlPatterns;
;apparel-uk;(?i)^https?://[^/]+(/[^?]*)?\?(.*\&)?(site=electronics)(|\&.*)$,(?i)^https?://electronics\.[^/]+(|/.*|\?.*)$,(?i)^https?://api\.hybrisdev\.com(:[\d]+)?/rest.*$,(?i)^https?://[^/]*/yacceleratorstorefront((?![\?\&]site=).)*;
```

This is a highly consolidated tutorials. For more details please have a look into the various subfolders in this repo.