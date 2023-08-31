#!/bin/sh
chmod +x /gcphybris/build/*.sh

# Reset the config by removing the custom properties file
touch /installer/customconfig/custom.properties
rm /installer/customconfig/custom.properties
touch /installer/customconfig/custom.properties

## copy b2c_acc_k8s recipe
mkdir /installer/recipes/b2c_acc_k8s/
cp -R /installer/recipes/b2c_acc_dockerized/* /installer/recipes/b2c_acc_k8s/
cp -R /gcphybris/build/b2c_acc_k8s_1811/recipe/* /installer/recipes/b2c_acc_k8s/

# Copy the JDK to the right place
cp /gcphybris/dep/sapjvm-*.rpm /installer/recipes/base_images/resources/base_jdk/java/.

# Copy the mysql driver to the target folder
cp /gcphybris/dep/mysql-connector-java-5.1.47.jar /hybris/bin/platform/lib/dbdriver/mysql-connector-java-5.1.47.jar

# Generate the Base
/installer/install.sh -r base_images buildImages

# Generate the Additionals (Solr and Zookeeper)
/installer/install.sh -r base_images buildAdditionalImages

# Generate Acclerator
/installer/install.sh -r b2c_acc_k8s buildImages

# Retag the images to comply with the cloudbuild yaml
docker tag b2cacc_deployment_platform b2c_acc_k8s_platform
docker tag b2cacc_deployment_hsql b2c_acc_k8s_hsql
docker tag ybase_solr b2c_acc_k8s_solr

# Tag all the Images
#docker tag b2cacc_deployment_platform gcr.io/hybris-on-gcp/hybris_platform_b2c_acc
#docker tag b2cacc_deployment_platform gcr.io/hybris-on-gcp/hybris_platform_b2c_acc:1811
#docker tag b2cacc_deployment_hsql gcr.io/hybris-on-gcp/hybris_hsql
#docker tag b2c_acc_k8s_solr gcr.io/hybris-on-gcp/hybris_solr

