
# Hybris on GKE Installation Guide
This guide describes how to build and deploy Hybris Commerce on GKE. It consists of a GKE cluster, a GCFS filestore, a CloudSQL instance and deploys the hybris containers (as well as some other dependencies) on GKE.

### 1) Preparation

#### Download Hybris
Download the hybris installation files and upload them to a GCS bucket. This bucket is used in the build process to download the files from.

#### Environment Variables
Prepare the shell you are working with and define the project, region, zone and GCS bucket as env variables. 
```
export PROJECT_ID=<gcp_project_id>
export REGION=<region>
export ZONE=<zone>
export GCS_BUCKET_HYBRIS=<gcs_bucket_to_hybris_inst_files>
```

Also set the preferences of the gcloud command:
```
gcloud config set core/project $PROJECT_ID
gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE
```

### 2) Build
#### Build the Builder 
The builder is a container that provides the environment to build all hybris artefacts that we need.
This is the first part and the steps to be executed are described [here](BuildBuilder/README.md)

#### Build Hybris Containers
Once the builder is ready we can use it to make the actual hybris artefacts and containers.
The achieve this can be found [here](BuildHybris/README.md)

### 3) Cloud Setup
In the next phase we spin up all the components we need to run Hybris. 
The steps to deploy a GKE cluster, a CloudSQL instance and a CloudFilestore share are desribed [here](CloudSetup/README.md) 

### 4) Configuration
Now it is time to define the configuration and assign it to the GKE cluster in form of secrets, config maps and service accounts.
These configuration settings are described [here](Configuration/README.md) 
Once all the cloud components are up and running we can 

### 5) Deployment
Once all the cloud components are up and running we can start to deploy all relevant parts 
The steps to deploy Hybris are described [here](Deployment/README.md) 








-------------------------
### Work in Progress 

#### Debug
```
kubectl logs -f $(kubectl get pod --selector="app=hybris-storefront"  --output jsonpath='{.items[0].metadata.name}')   -c hybris-storefront
kubectl attach $(kubectl get pod --selector="app=hybris-platform-admin-init" --output jsonpath='{.items[0].metadata.name}')  -i
kubectl exec $(kubectl get pod --selector="app=hsql" --output jsonpath='{.items[0].metadata.name}') -c hsql df -H
kubectl logs -f $(kubectl get pod --selector="app=hybris-platform-admin-init"  --output jsonpath='{.items[0].metadata.name}')   -c platform-admin-init
```

#### TODOs
- Parameterize cloudbuild yamls with project ID and GCS bucket
