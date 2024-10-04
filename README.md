# Setting Up Envoy Proxy in a Kubernetes Cluster

## Install Envoy Proxy Using Helm

      First, add the Helm repository for the Cloud Native App:
      
      helm repo add cloudnativeapp https://cloudnativeapp.github.io/charts/curated/
      
      Next, pull the Envoy Helm chart:
      
      helm pull cloudnativeapp/envoy --version 1.5.0 --untar
     
## Install Envoy Proxy
      
      Before installing Envoy, modify the PodDisruptionBudget.yaml template within the Envoy chart. Change the apiVersion from policy/v1beta1 to policy/v1.
      
      Now, install the Envoy Proxy using the following command:

      helm install envoy ./envoy/

## Deploy an NGINX Service for Testing

      Deploy an NGINX service in the same cluster to test the Envoy Proxy. Modify the Envoy configuration to set the backend to the NGINX service, allowing Envoy to forward traffic to it.
      
      Here’s a sample envoy.yaml configuration:

      files:
        envoy.yaml: |-
          admin:
            access_log_path: /dev/stdout
            address:
              socket_address:
                address: 0.0.0.0
                port_value: 9901
      
          static_resources:
            listeners:
            - name: listener_0
              address:
                socket_address:
                  address: 0.0.0.0  # Listening on all IP addresses
                  port_value: 10000  # Port for the listener
              filter_chains:
              - filters:
                - name: envoy.http_connection_manager
                  config:
                    access_log:
                    - name: envoy.file_access_log
                      config:
                        path: /dev/stdout
                    stat_prefix: ingress_http
                    route_config:
                      name: local_route
                      virtual_hosts:
                      - name: local_service
                        domains: ["*"]  # Allowing all domains
                        routes:
                        - match:
                            prefix: "/"  # Matching all prefixes
                          route:
                            host_rewrite: www.google.com
                            cluster: service_google  # Name of the backend service (NGINX)
                    http_filters:
                    - name: envoy.router
            clusters:
            - name: service_google  # Backend service cluster name
              connect_timeout: 0.25s
              type: LOGICAL_DNS
              dns_lookup_family: V4_ONLY
              lb_policy: ROUND_ROBIN
              hosts:
                - socket_address:
                    address: nginx-service.default.svc.cluster.local  # Backend service address
                    port_value: 80  # Backend service port
              #tls_context:
              #  sni: www.google.com  # Use this if enabling TLS; otherwise, disable it

## Verification
     
       To verify that Envoy is correctly set up, check which port it is listening on. By default, Envoy listens on port 10000. You can confirm this in the envoy.yaml file under the files section.
      
      You can also describe the Envoy deployment and service to verify the targetPort, containerPort, and servicePort. Ensure that at least the targetPort and containerPort are the same.
      
      Once confirmed, port-forward the Envoy service to a local port and verify that it forwards traffic to the backend service. You can do this by browsing to:

      http://localhost:<localport>
      
      By following these steps, you should have a functioning Envoy Proxy set up to route traffic to your NGINX service.
