# ENVOY PROXY

FOR CREATING ENVOY PROXY WITH ASKANGIE BACKEND. THE FOLLOWING SERVICE ALSO NEED TO BE CONFIGURE.

- RESERVE THE IP FOR APPLICATION LOAD BALANCER USING GCLOUD COMMAND

   **cloud compute addresses create envoy-proxy --global  

   Verify the creation and obtain details of the reserved static IP.

   **gcloud compute addresses describe nginxexample --global

- CONFIGURE THE WORKLOAD IDENTITY IN ENVOY NAMESPACE FOR ASKENGI DEPLOYMENT

- SET NODE TO TAINT AND ADD TOLERATION AND NODE AFFINITY IN DEPLOYMENTS FILE. FOR DEPLOYING SERVICES ON SPECFIC NODES

     kubectl taint nodes <node-name> key=value:taint-effect

     kubectl taint nodes ask-angie-nodepool app=ask-angie-external 

    set the same key and values in tolerence when you are setting tolerence in deployment.

    tolerations:
      - key: "app"
        operator: "Equal"
        value: "ask-angie-external"
        effect: "NoSchedule"

    use below command to labelling the node and set same label to node affinity when you are setting the node affinity in deployment

    kubectl label nodes ask-angie-nodepool app=ask-angie-external

    affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: "app"
                operator: "In"
                values:
                - "ask-angie-external"

    NOTE: taint work with tolerence and node label work with node affinity. And you can use both for your case.. Mean set taint and label on node and tolerence and node affinity on deployment mean pods 
 



  
