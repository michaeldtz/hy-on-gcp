#!/bin/sh

# Reset the config by removing the custom properties file
touch /installer/customconfig/custom.properties
rm /installer/customconfig/custom.properties
touch /installer/customconfig/custom.properties

## copy b2c_acc_k8s recipe
mkdir -p /installer/recipes/b2c_acc_k8s/
cp -R /gcphybris/build/b2c_acc_k8s_1905/recipe/* /installer/recipes/b2c_acc_k8s/

# Download the Solr files
mkdir -p /gcphybris/resources/solr
echo "Starting download of Solr 7.7.1"
curl -s https://archive.apache.org/dist/lucene/solr/7.7.1/solr-7.7.1.tgz > /gcphybris/resources/solr/solr-7.7.1.tgz
echo "Finished download of Solr 7.7.1"
tar zxf /gcphybris/resources/solr/solr-7.7.1.tgz -C  /gcphybris/resources/solr/
mv /gcphybris/resources/solr/solr-7.7.1 /gcphybris/resources/solr/server
cp -R /gcphybris/build/b2c_acc_k8s_1905/solr/* /gcphybris/resources/solr/

# Build the YBase JDK Image
docker build -t ybase_jdk /gcphybris/build/b2c_acc_k8s_1905/base_jdk/.

# Copy the mysql driver to the target folder
cp /gcphybris/dep/mysql-connector-java-5.1.47.jar /hybris/bin/platform/lib/dbdriver/mysql-connector-java-5.1.47.jar


##### Build
# Generate Acclerator
/installer/install.sh -r b2c_acc_k8s buildImages 



 