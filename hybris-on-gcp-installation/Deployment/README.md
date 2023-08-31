# Deployment of Hybris on GKE

### Kubectl Authorization
Ensure that kubectl is authenticated to access the GKE cluster
```
gcloud container clusters get-credentials hybris-gke-cluster
```

## Preparation
The following steps need to be executed in order to make the yaml files ready for the deploment in your enviroment:
- The IP address of the fileshare (created in Cloud Setup) has to be copied into a1_foundation.yaml (at the place of the persistant volume)

## Deploy
```
kubectl apply -f Deployment/a1_foundation.yaml
```

Then the Platform Initializer
```
kubectl apply -f Deployment/a2_platform_init.yaml
```
In order to see the progress you can stream the logs
```
kubectl logs -f $(kubectl get pod --selector="app=hybris-admin-init"  --output jsonpath='{.items[0].metadata.name}') -c hybris-admin-init
kubectl logs -f $(kubectl get pod --selector="app=hybris-admin-init"  --output jsonpath='{.items[0].metadata.name}') -c cloudsql-proxy
```
The initialization takes roughly about 30 minutes. After the initialization is finished (this can be seen in the logs or the container status) this Job/Deployment can be removed again.
```
kubectl delete -f Deployment/a2_platform_init.yaml
```

Now you are ready to deploy the rest of all the Hybris servers (HAC, Storefront and Backoffice)
```
kubectl apply -f Deployment/a3_hybris_hac.yaml
kubectl apply -f Deployment/a3_hybris_storefront.yaml 
kubectl apply -f Deployment/a3_hybris_backoffice.yaml 
```

If you want to check the logs:
```
kubectl logs -f $(kubectl get pod --selector="app=hybris-hac"  --output jsonpath='{.items[0].metadata.name}') -c hybris-hac
kubectl logs -f $(kubectl get pod --selector="app=hybris-storefront"  --output jsonpath='{.items[0].metadata.name}') -c hybris-storefront
kubectl logs -f $(kubectl get pod --selector="app=hybris-backoffice"  --output jsonpath='{.items[0].metadata.name}') -c hybris-backoffice
```

As soon as the servers are ready (can be found in the logs), which takes about 15 to 20 minutes you can access the various servers. 

## Access
There are three K8s services that you now can access: 
- hybris-hac-service
- hybris-backoffice-service
- hybris-storefront-service

Each service has a dedicated path that you need to add manually
- HAC is available under path /
- Backoffice is available under path /backoffice
- The storefront is available under path /yacceleratorstorefront

For the storefront there is one more step needed to make it easier to access it. Background: Usually the storefront (at least in the accellerator) uses a pattern to identify the right site to access. In the PoC we are using IP adresses and therefore that mechanism doesn't work. A simple work arround is to adapt the URL pattern configuration. Therefore go to HAC --> Console --> ImpEx Import. Copy in the following script and run "Import content":
```
UPDATE CMSSite;uid[unique=true];urlPatterns;
;apparel-uk;(?i)^https?://[^/]+(/[^?]*)?\?(.*\&)?(site=electronics)(|\&.*)$,(?i)^https?://electronics\.[^/]+(|/.*|\?.*)$,(?i)^https?://api\.hybrisdev\.com(:[\d]+)?/rest.*$,(?i)^https?://[^/]*/yacceleratorstorefront((?![\?\&]site=).)*;
```


## Cleaup Everything
```
kubectl delete -f Deployment/a3_hybris_backoffice.yaml 
kubectl delete -f Deployment/a3_hybris_storefront.yaml
kubectl delete -f Deployment/a3_hybris_hac.yaml
kubectl delete -f Deployment/a2_platform_init.yaml
kubectl delete -f Deployment/a1_foundation.yaml 
```

##  Troubleshooting Snippets
```
# Exec in the various containers
kubectl exec $(kubectl get pod --selector="app=hybris-admin-init" --output jsonpath='{.items[0].metadata.name}') -c hybris-admin-init ls /
kubectl exec $(kubectl get pod --selector="app=hybris-hac" --output jsonpath='{.items[0].metadata.name}') -c hybris-hac ls /
kubectl exec $(kubectl get pod --selector="app=hybris-storefront" --output jsonpath='{.items[0].metadata.name}') -c hybris-storefront ls /
kubectl exec $(kubectl get pod --selector="app=hybris-backoffice" --output jsonpath='{.items[0].metadata.name}') -c hybris-backoffice cat /opt/aspects/backoffice/tomcat/conf/Catalina/localhost/backoffice.xml

# Connect to SOLR
kubectl port-forward $(kubectl get pod --selector="app=solr" --output jsonpath='{.items[0].metadata.name}') 8080:8983
```


### TODO
- Find a way to parameterize the filestore IP
- Parameterize CloudSQL instance description of proxy

