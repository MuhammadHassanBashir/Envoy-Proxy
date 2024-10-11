# ENVOY PROXY

FOR CREATING ENVOY PROXY WITH ASKANGIE BACKEND. THE FOLLOWING SERVICE ALSO NEED TO BE CONFIGURE.

- RESERVE THE IP FOR APPLICATION LOAD BALANCER USING GCLOUD COMMAND

   **cloud compute addresses create envoy-proxy --global  

   Verify the creation and obtain details of the reserved static IP.

   **gcloud compute addresses describe nginxexample --global

- CONFIGURE THE WORKLOAD IDENTITY IN ENVOY NAMESPACE FOR ASKENGI DEPLOYMENT

- SET NODE TO TAINT AND ADD TOLERATION AND NODE AFFINITY IN DEPLOYMENTS FILE. FOR DEPLOYING SERVICES ON SPECFIC NODES

     kubectl taint nodes <node-name> key=value:taint-effect

     kubectl taint nodes <node-name> =value:taint-effect


  
