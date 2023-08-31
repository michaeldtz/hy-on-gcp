# Cloud Setup
This chapter describes the steps to setup the cloud components that are needed to run Hybris on GKE.
That is:
- a Cloud SQL instance
- a GKE cluster
- a Cloud Filestore share

### Run the GKE Cluster
```
gcloud deployment-manager deployments create hybris-gke-cluster --config CloudSetup/DeploymentManager/GKECluster/gkecluster.yaml 
```

### Create FileStore Share
```
gcloud deployment-manager deployments create hybris-media-share --config CloudSetup/DeploymentManager/CloudFileStore/gcfs.yaml 
```
Retrieve the IP adress of the share. It is needed later.

### Create CloudSQL
The easiest option is the fully managed service of CloudSQL. Alternatively, you can use and connect any kind of database that is supported by Hybris. Please find more information on the aspect to use them here: [SQL Databases for Hybris on GCP](../Configuration/sqldbs/README.md).
If you use CloudSQL the following command will easily deploy it via DeploymentManager
```
gcloud deployment-manager deployments create hybris-db-mysql --config CloudSetup/DeploymentManager/CloudSQL/cloudsql.yaml
```

The deployment manager will generate passwords and show them at the end of the build. Securely store the passwords for root and hybrisdb user.


### Cleanup

```
gcloud deployment-manager deployments create hybris-media-share
gcloud deployment-manager deployments create hybris-db-mysql
gcloud deployment-manager deployments create hybris-gke-cluster
```

### TODO
-Automate the Setup Using CloudBuild