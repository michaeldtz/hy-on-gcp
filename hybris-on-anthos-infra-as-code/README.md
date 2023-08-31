
# Hybris on Anthos
This guide describes how to deploy Hybris Commerce on Anthos. It consists of a GKE cluster and an Anthos onPrem cluster. Find out more about Hybris Commerce on GKE at the Google-internal doc (go/hybris-on-gke-poc-guide). Different to the setup described in this guide we will a) distribute the deployment the components of Hybris accross the cloud and onPremise clusters and b) replace the managed services for MySQL and NFS by container deployments of equivalent services. 

### 1) Access to Hybris Artifacts
The build of the hybris artifacts is part of a [predesssor project](https://source.cloud.google.com/hybris-on-gcp/hybris-on-gcp-installation) that covers this step and contains fresh images that can be deployed in the later step. 
To access the container images for Hybris please request access to container registry by contacting [midietz@](mailto:midietz@google.com).

### 2) GKE & Anthos Cluster
This project requires a GKE cluster as well as an Anthos onPremise K8s cluster. Both should be (registered) in the same project as they will have a Istio-based communication in between. 

### 3) Install Istio on Clusters
Execute the following guide to install Istio on both clusters [Link](https://istio.io/docs/setup/install/multicluster/gateways/#deploy-the-istio-control-plane-in-each-cluster) until and including the step Setup DNS. 

### 4) Configuration
As soon as the K8s clusters are available the configuration can be done. These configuration settings are described [here](1_Configuration/README.md). 

### 5) Deployment
Once the configuration is made we can start to deploy all relevant parts. The steps to deploy Hybris are described [here](2_Deployment/README.md) 






