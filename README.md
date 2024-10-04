# Install the envoy proxy using helm in kubernetes cluster.

      helm repo add cloudnativeapp https://cloudnativeapp.github.io/charts/curated/
   
      # command to get envoy helm chart   
      
         helm pull cloudnativeapp/envoy --version 1.5.0 --untar 
      
      # command to install envoy proxy with download helm chart, but before this you need to change the apiversion of PodDisruptionBudget.yaml template from policy/v1beta1 to policy/v1 under envoy templates.
         
         helm install envoy ./envoy/ 
      
      # Now install nginx deployment in a same cluster for testing envoy proxy.. and change the envoy backend for setting the backend as nginx service. because we are trying that our envoy proxy forwards traffic to backend nginx service...

      like    
      
      files:
        envoy.yaml: |-
          ## refs:
          ## - https://www.envoyproxy.io/docs/envoy/latest/start/start#quick-start-to-run-simple-example
          ## - https://raw.githubusercontent.com/envoyproxy/envoy/master/configs/google_com_proxy.v2.yaml
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
                  address: 0.0.0.0           ------------> listening on all ip 
                  port_value: 10000          -------------> with 10000 port
              filter_chains:
              - filters:
                - name: envoy.http_connection_manager
                  config:
                    access_log:
                    - name: envoy.file_access_log
                      config:
                        path: /dev/stdout
                    stat_prefix: ingress_http
                    route_config:                   ------------------> backend configs set here
                      name: local_route
                      virtual_hosts:                 ----------------> giving backend routes
                      - name: local_service
                        domains: ["*"]              -------------------> allowing all domains
                        routes:
                        - match:
                            prefix: "/"            ----------------------> matching prefix
                          route:
                            host_rewrite: www.google.com
                            cluster: service_google      (name of backend service)  -----------> routing traffic to backend service, in our case it would be nginx service
                    http_filters:
                    - name: envoy.router
            clusters:                                     -----------------> setting backend cluster for envoy proxy and giving backend cluster details here...
            - name: service_google                        -------------> giving the same backend service name here     
              connect_timeout: 0.25s
              type: LOGICAL_DNS
              dns_lookup_family: V4_ONLY
              lb_policy: ROUND_ROBIN
              hosts:
                - socket_address:
                    address: nginx-service.default.svc.cluster.local            -----------> gave backend service address here, we can give service FQDN or service name..
                    port_value: 80                                              -------------> backend service port
              tls_context:
                sni: www.google.com                                             --------------> use it tls enable, else disable this.. otherwise it will give you error.. in my case i have not use , so i disable this... after that i got the result...  
              
