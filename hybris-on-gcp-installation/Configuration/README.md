# Configuration
The configuration contains some basic steps that are necessary to get Hybris running (like the SSL certifications) as well as the general settings of the solution.

### Kubectl Authorization
Ensure that kubectl is authenticated to access the GKE cluster:
```
gcloud container clusters get-credentials hybris-gke-cluster
```

### Create Hybris Config
The hybris config contains one part for the SQL configuration, which depends on what database you decide for. There are three different SQL configurations available in this project: for CloudSQL, for MySQL on GCE and for HANA on GCE. If you are interested in the latter two options please also [read the instructions for these](sqldbs/README.md). Please remeber to put in the passwords into the configuration files. 

##### With CloudSQL
```
kubectl create configmap hybris-config \
--from-file 10-local.properties=Configuration/config/basic.properties \
--from-file 20-local.properties=Configuration/config/solr.properties \
--from-file 40-local.properties=Configuration/config/cluster.properties \
--from-file 30-local.properties=Configuration/config/sql_a_cloudsql.properties 
```

#####  With MySQL on GCE
```
kubectl create configmap hybris-config \
--from-file 10-local.properties=Configuration/config/basic.properties \
--from-file 20-local.properties=Configuration/config/solr.properties \
--from-file 40-local.properties=Configuration/config/cluster.properties \
--from-file 30-local.properties=Configuration/config/sql_b_mysqlonvm.properties 
```

#####  With HANA
```
kubectl create configmap hybris-config \
--from-file 10-local.properties=Configuration/config/basic.properties \
--from-file 20-local.properties=Configuration/config/solr.properties \
--from-file 40-local.properties=Configuration/config/cluster.properties \
--from-file 30-local.properties=Configuration/config/sql_c_hana.properties 
```

### Provide Secret for CloudSQL
Create a service account (Console -> IAM & Admin -> Service Account) with Cloud SQL client rights (role: roles/cloudsql.client) and download the key as JSON. For the following snippet it is downloaded to .secrets and then renamed to credentials.json:
```
kubectl create secret generic cloudsql-credentials --from-file .secrets/credentials.json
```


### Provide SSL Certs for Hybris
Upload the default certificates that are used for HTTPs access. They will still cause a SSL error in the browser so you need to consider to replace them at a later time. 
```
kubectl create secret generic hybris-ssl-certs --from-file Configuration/config/hybrissecrets/keystore --from-file Configuration/config/hybrissecrets/server.crt --from-file Configuration/config/hybrissecrets/server.key
```

### Create Service Account for KubePing
```
kubectl create serviceaccount hybris-platform-service-account
```


## Cleanup 
```
kubectl delete configmap hybris-config
kubectl delete serviceaccount hybris-platform-service-account
```

## TODO 
- Parameterize / Secure CloudSQL password