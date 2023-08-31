# SQL Databases for Hybris on GCP

Instead of using CloudSQL and the respective DeploymentManager scripts it is also possible to use any other supported DB for Hybris.
Additionally, this repository provides the configuration for two other options
- MySQL running on GCE
- HANA Express running on GCE

Here you can find some hints on setting up these databases

### MySQL on GCE
You need to create a dedicated user and a database that Hybris can use. The easiest way to get connected to the MySQL instance is to log in to the host via ssh and run the mysql command. From there you can run the following commands to create user and database:

```
CREATE DATABASE hybris;
CREATE USER 'hybrisdb'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'hybrisdb'@'%';
```
Consider to replace the % sign by a more restrictive setting, e.g. the IP-range of the GKE cluster.
In order to observe that the Hybris intialization is happening you can run the following statement:
```
SELECT table_name,table_rows FROM information_schema.tables WHERE table_schema = "hybris";
```


### HANA Express on GCE
In this case 
HANA Express
Instance Number: 90
hdbsql -n 127.0.0.1:39015 -u SYSTEM
CREATE USER hybrisdb PASSWORD ap5UoxKL NO FORCE_FIRST_PASSWORD_CHANGE
GRANT ALL PRIVILEGES ON SCHEMA hybris TO hybrisdb;

SELECT TABLE_NAME, RECORD_COUNT FROM M_CS_TABLES WHERE UPPER(SCHEMA_NAME) = 'HYBRIS'

