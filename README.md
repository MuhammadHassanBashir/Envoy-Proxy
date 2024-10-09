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

## Command to Test CORS

To test your CORS configuration, you can use the following curl commands:
            
Testing CORS with origin http://test-origin-1.com:
            
      curl -i -X OPTIONS https://envoy.disearch.ai \
      -H "Origin: http://test-origin-1.com" \
      -H "Access-Control-Request-Method: POST" \
      -H "Access-Control-Request-Headers: content-type"

Expected CORS Response for Origin http://test-origin-1.com:
      
            HTTP/2 200 
            access-control-allow-origin: http://test-origin-1.com
            access-control-allow-methods: POST
            access-control-allow-headers: content-type
            access-control-max-age: 100
            date: Wed, 09 Oct 2024 18:28:46 GMT
            server: envoy
            content-length: 0
            via: 1.1 google
            alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000

Testing CORS with origin http://test-host-2.com:
            
            curl -i -X OPTIONS https://envoy.disearch.ai \
            -H "Origin: http://test-host-2.com" \
            -H "Access-Control-Request-Method: POST" \
            -H "Access-Control-Request-Headers: content-type"
            
Expected CORS Response for Origin http://test-host-2.com:
            
            HTTP/2 200 
            access-control-allow-origin: http://test-host-2.com
            access-control-allow-methods: POST
            access-control-allow-headers: content-type
            access-control-max-age: 100
            date: Wed, 09 Oct 2024 18:34:32 GMT
            server: envoy
            content-length: 0
            via: 1.1 google
            alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
            
Explanation of CORS Configuration

            In your Envoy CORS configuration, you have specified the following:
            Origins:
            
            http://test-origin-1.com
            http://test-host-2.com
            
These origins are explicitly allowed in the allow_origin_string_match section, meaning the server will accept CORS requests coming from either of these two domains.
            
Allowed Methods:
            
            POST requests are allowed. This is defined in the allow_methods section.
            
Allowed Headers:
            
            The header content-type is permitted, as specified in the allow_headers section.
            
Max Age:
            
            The preflight response can be cached for 100 seconds, defined by max_age: "100". This reduces the number of preflight requests needed for the same method and headers from the same origin.
            
Relevant Envoy Configuration Section
            
            Here is the relevant section of your Envoy configuration where the CORS policy is applied:
            
            virtual_hosts:
              - name: local_service
                domains: ["*"]
                typed_per_filter_config:
                  envoy.filters.http.cors:
                    "@type": type.googleapis.com/envoy.extensions.filters.http.cors.v3.CorsPolicy
                    allow_origin_string_match:
                    - safe_regex:
                        regex: ".*"
                    allow_headers: "content-type,x-grpc-web"
                    allow_methods: "GET, POST, OPTIONS"
                    expose_headers: "custom-header-1,custom-header-2"
                    max_age: "3600"
                    allow_credentials: true
                routes:
                  - match:
                      prefix: "/"
                    route:
                      host_rewrite_literal: envoy.disearch.ai
                      cluster: frontend_service
                    typed_per_filter_config:
                      envoy.filters.http.cors:
                        "@type": type.googleapis.com/envoy.extensions.filters.http.cors.v3.CorsPolicy
                        allow_origin_string_match:
                        - exact: "http://test-origin-1.com"
                        - exact: "http://test-host-2.com"
                        allow_headers: "content-type"
                        allow_methods: "POST"
                        max_age: "100"
            
In this configuration, you have specified both global and route-specific CORS policies. The allow_origin_string_match directive ensures that only the predefined origins are permitted to make cross-origin requests. You also control allowed methods, headers, and the cache duration for preflight requests (via max_age).
            
            
Conclusion
            
            By using the curl commands and configuring your CORS policy as described, Envoy is correctly handling CORS requests from the specified origins (http://test-origin-1.com and http://test-host-2.com). Ensure that any additional requests from other origins or with different methods/headers align with your configuration.
