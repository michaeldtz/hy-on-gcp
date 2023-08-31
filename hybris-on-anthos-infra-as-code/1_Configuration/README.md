# Configuration
The configuration contains some basic steps that are necessary to get Hybris running (like the SSL certifications) as well as the general settings of the solution.


### Create MySQL Password as Secret
m

### Create Hybris Config
The hybris config contains one part for the SQL configuration, which depends on what database you decide for. 
In this project we deploy a MySQL db as a container in the onPremise cluster.
Please remeber to put in the passwords into the configuration files. 

```
kubectl create configmap hybris-config \
--from-file 10-local.properties=config/basic.properties \
--from-file 20-local.properties=config/solr.properties \
--from-file 30-local.properties=config/mysql.properties \
--from-file 40-local.properties=config/cluster.properties
```



### Provide SSL Certs for Hybris
Upload the default certificates that are used for HTTPs access. They will still cause a SSL error in the browser so you need to consider to replace them at a later time. 
```
kubectl create secret generic hybris-ssl-certs --from-file config/hybrissecrets/keystore --from-file config/hybrissecrets/server.crt --from-file config/hybrissecrets/server.key
```

### Create Service Account for KubePing
```
kubectl create serviceaccount hybris-platform-service-account
```


## TODO 
- Parameterize / Secure CloudSQL password
- Handle password / secret / https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets
- 