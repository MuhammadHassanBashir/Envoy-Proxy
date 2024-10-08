

# Envoy-Proxy

## Terminology

A few definitions before we dive into the main architecture documentation. Some of the definitions are slightly contentious within the industry, however they are how Envoy uses them throughout the documentation and codebase, so c’est la vie.

    **Host**: An entity capable of network communication (application on a mobile phone, server, etc.). In this documentation a host is a logical network application. A physical piece of hardware could possibly have multiple hosts running on it as long as each of them can be independently addressed.
    
    **Downstream**: A downstream host connects to Envoy, sends requests, and receives responses.
    
    **Upstream**: An upstream host receives connections and requests from Envoy and returns responses.
    
    **Listener**: A listener is a named network location (e.g., port, unix domain socket, etc.) that can be connected to by downstream clients. Envoy exposes one or more listeners that downstream hosts connect to.
    
    **Cluster**: A cluster is a group of logically similar upstream hosts that Envoy connects to. Envoy discovers the members of a cluster via service discovery. It optionally determines the health of cluster members via active health checking. The cluster member that Envoy routes a request to is determined by the load balancing policy.
    
    **Mesh**: A group of hosts that coordinate to provide a consistent network topology. In this documentation, an “Envoy mesh” is a group of Envoy proxies that form a message passing substrate for a distributed system comprised of many different services and application platforms.
    
    **Runtime configuration**: Out of band realtime configuration system deployed alongside Envoy. Configuration settings can be altered that will affect operation without needing to restart Envoy or change the primary configuration.
   **Network Filter**:
   **Threading Model**:
   **Connection Pool**:   

## Flow

  Downstream ----> envoy(listener) ---> cluster(upstream hosts)

## NOTES

- Downstream: Requests come from Downstream
- Upstream: Responses come from Upstream
- Service mesh/side car
- Cluster: Group of hosts/endpoints are called a cluster, Cluster has a load balancing policy.
- Listeners: listen on a port for downstream clients, It is similar to fronted in HAPROXY, **Network Filters** are applied to Listeners, like TCP/HTTP filters, Transport Sockets TLS.

- Network Filters: 
   - How Envoy maps Listerners and clusters.
   - TCP Proxy Network Filter
     - envoy.filters.network.tcp_proxy
   - HTTP Proxy Network Filter
     - envoy.filters.network.http_connection_manager
   - MongoDB/MySQL Network Filter

- Connection Pools
  - Each Host in a cluster gets 1 or more conneciton pools
  - Each protocol get a pool HTTP 1.1, HTTP/2
  - More pools allocated per priority or socket options
  - Connection Pools are per worker thread

- Threading Model
  - Single process multi-threadded model
  - Each thread is bound to a single connection
  - No coordination b/w threads

Example:
   -   Test 4 services
   -   Install envoy
   -   layer 7 proxying
      -   proxy to 4 Backends
      -   Conditional app1 app2
      -   Prevent admin access
   -   layer 4 proxying
   -    Enables HTTPS
   -    Enables HTTP/2
   -    Disable TLS 1.0/1.1
   -    SSL Labs Test   

## Install envoy on ubuntu focal:

      wget -O- https://apt.envoyproxy.io/signing.key | sudo gpg --dearmor -o /etc/apt/keyrings/envoy-keyring.gpg
      echo "deb [signed-by=/etc/apt/keyrings/envoy-keyring.gpg] https://apt.envoyproxy.io focal main" | sudo tee /etc/apt/sources.list.d/envoy.list
      sudo apt-get update
      sudo apt-get install envoy
      envoy --version

## Envoy.yaml

      static_resources:
        listeners:            
        # ingress
        - name: football_sidecar_listener
          address:     ------------------> what address are we listening on    
            socket_address:     -------------> socket address
              # Entrypoint for service through Envoy
              address: 0.0.0.0      ---------->  listening on all interfaces(all ips) 
              port_value: 8080      -----------> listening on port 
          filter_chains:            ------------> filter chains at address level
          - filters:                
            - name: envoy.filters.network.http_connection_manager
              typed_config:            ---------> which exact type pulling for(you can also use this: type.googleapis.com/envoy.config.filters.network.http_connection_manager.v2.HttpConnectionManager)         
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                # used when emitting stats
                stat_prefix: football_sidecar_hcm_filter   --------> just giving the name
                http_filters:
                - name: envoy.filters.http.router
                  typed_config:
                    "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
                route_config:                               --------> routing listerner traffic to backend
                  name: football_sidecar_http_route_config   ---------> route name
                  virtual_hosts:                             ----------> which is your backend cluster
                  # name used when emitting stats, not imp for routing itself
                     - name: football_sidecar_virtual_host
                       domains:                                 ----------> here you basically filter what domain you gonna match on... rightnow we do not have any domain, so we use all "*".
                          - "*"
                       routes:          --------> here we will be matching 
                          - name:
                            match:
                              prefix: "/"   --------> anything come with "/" prefix will go to the backend cluster.
                           route:
                              cluster: allbackend_cluster       ----->backend cluster name "allbackend_cluster" .
                http_filters:   --->http filter name
                  -   name: envoy.filters.http.router

## here we are builder our all backend cluster
        clusters:
        - name: allbackend_cluster      ----> cluster name
          connect_timeout: 1s           -----> if not connect to the 1s  then request will dead.
          type: STRICT_DNS                 or write strict_dns
          lb_policy: ROUND_ROBIN            or write round_robin
          load_assignment:
            cluster_name: allbackend_cluster
            endpoints:             -----------> endpoint where we listening too..
            - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      # reroute to service container in the same K8s deployment
                      address: 127.0.0.1               ---> endpoint address 
                      port_value: 6200                 ----> endpoint port..  

remember for multiple endpoints, you just need to copy and paste the endpoint section as it is and change the address and port accordingly...

      this section..            
                  - endpoint:
                        address:
                          socket_address:
                            # reroute to service container in the same K8s deployment
                            address: 127.0.0.1               ---> endpoint address 
                            port_value: 6200                 ----> endpoint port..     
## Command to start envoy

      envoy --config-path "file-name like envoy.yaml"

## Spliting Traffic Feature

      static_resources:
        listeners:            
        # ingress
        - name: football_sidecar_listener
          address:     ------------------> what address are we listening on    
            socket_address:     -------------> socket address
              # Entrypoint for service through Envoy
              address: 0.0.0.0      ---------->  listening on all interfaces(all ips) 
              port_value: 8080      -----------> listening on port 
          filter_chains:            ------------> filter chains at address level
          - filters:                
            - name: envoy.filters.network.http_connection_manager
              typed_config:            ---------> which exact type pulling for(you can also use this: type.googleapis.com/envoy.config.filters.network.http_connection_manager.v2.HttpConnectionManager)         
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                # used when emitting stats
                stat_prefix: football_sidecar_hcm_filter   --------> just giving the name
                http_filters:
                - name: envoy.filters.http.router
                  typed_config:
                    "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
                route_config:                               --------> routing listerner traffic to backend
                  name: football_sidecar_http_route_config   ---------> route name
                  virtual_hosts:                             ----------> which is your backend cluster
                  # name used when emitting stats, not imp for routing itself
                     - name: football_sidecar_virtual_host
                       domains:                                 ----------> here you basically filter what domain you gonna match on... rightnow we do not have any domain, so we use all "*".
                          - "*"
                       routes:          --------> here we will be matching 
                          - name:
                            match: { prefix: "/app1"}   --> anything come with "/app1" prefix will go to app1_cluster
                            route:
                               cluster: app1_cluster
                          - name:
                            match: { prefix: "/app2"}  --> anything come with "/app2" prefix will go to app2_cluster    
                            route:
                               cluster: app2_cluster   
                          - name:
                            match:
                              prefix: "/"   --------> anything come with "/" prefix will go to the backend cluster.
                            route:
                                 cluster: allbackend_cluster       ----->backend cluster name "allbackend_cluster" .     
                               
                http_filters:   --->http filter name
                  -   name: envoy.filters.http.router

## here we are builder our all backend cluster
        clusters:
        - name: allbackend_cluster      ----> cluster name
          connect_timeout: 1s           -----> if not connect to the 1s  then request will dead.
          type: STRICT_DNS                 or write strict_dns
          lb_policy: ROUND_ROBIN            or write round_robin
          load_assignment:
            cluster_name: allbackend_cluster
            endpoints:             -----------> endpoint where we listening too..
            - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      # reroute to service container in the same K8s deployment
                      address: 127.0.0.1               ---> endpoint address 
                      port_value: 6200                 ----> endpoint port..  

        - name: app1_cluster      ----> cluster name
          connect_timeout: 1s           -----> if not connect to the 1s  then request will dead.
          type: STRICT_DNS                 or write strict_dns
          lb_policy: ROUND_ROBIN            or write round_robin
          load_assignment:
            cluster_name: app1_cluster
            endpoints:             -----------> endpoint where we listening too..
            - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                         # reroute to service container in the same K8s deployment
                      address: 127.0.0.1               ---> endpoint address 
                      port_value: 6200                 ----> endpoint port..  
   
         - name: app2_cluster      ----> cluster name
           connect_timeout: 1s           -----> if not connect to the 1s  then request will dead.
           type: STRICT_DNS                 or write strict_dns
           lb_policy: ROUND_ROBIN            or write round_robin
           load_assignment:
             cluster_name: app2_cluster
             endpoints:             -----------> endpoint where we listening too..
             - lb_endpoints:
               - endpoint:
                  address:
                   socket_address:
                      # reroute to service container in the same K8s deployment
                     address: 127.0.0.1               ---> endpoint address 
                     port_value: 6200                 ----> endpoint port..  

         we can also add multiple end points on each cluster..

## Block Certain request


## Troubleshoot Envoy
   
         install package in container using terminal 
         kubectl exec -it pod/envoy-686984d4c-9bw9c -- bash -c "apt-get update && apt-get install -y curl"
         kubectl exec -it pod/envoy-686984d4c-9bw9c -- apt-get update
         kubectl exec -it pod/envoy-686984d4c-9bw9c -- apt-get install curl -y
## Command to test http2 protocal
   
         curl -v --http2 http://<your-envoy-ip>:<port>

## with this way configmap will get the values from helm values.yaml

      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: envoy-config
      data:
      {{- range $key, $value := .Values.files }}
        {{ $key }}: |-
      {{ $value | default "" | indent 4 }}
      {{- end -}}   

## Command to manually test the certificate

   curl -vI https://envoy.disearch.ai or curl -kv https://envoy.disearch.ai --> -kv ingnore the certificate
    
   *   Trying 34.117.212.151:443...
   * TCP_NODELAY set
   * Connected to envoy.disearch.ai (34.117.212.151) port 443 (#0)
   * ALPN, offering h2
   * ALPN, offering http/1.1
   * successfully set certificate verify locations:
   *   CAfile: /etc/ssl/certs/ca-certificates.crt
     CApath: /etc/ssl/certs
   * TLSv1.3 (OUT), TLS handshake, Client hello (1):
   * TLSv1.3 (IN), TLS handshake, Server hello (2):
   * TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
   * TLSv1.3 (IN), TLS handshake, Certificate (11):
   * TLSv1.3 (IN), TLS handshake, CERT verify (15):
   * TLSv1.3 (IN), TLS handshake, Finished (20):
   * TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
   * TLSv1.3 (OUT), TLS handshake, Finished (20):
   * SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
   * ALPN, server accepted to use h2
   * Server certificate:
   *  subject: CN=envoy.disearch.ai
   *  start date: Oct  8 17:25:10 2024 GMT
   *  expire date: Jan  6 18:16:42 2025 GMT
   *  subjectAltName: host "envoy.disearch.ai" matched cert's "envoy.disearch.ai"
   *  issuer: C=US; O=Google Trust Services; CN=WR3
   *  SSL certificate verify ok.
   * Using HTTP2, server supports multi-use
   * Connection state changed (HTTP/2 confirmed)
   * Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0
   * Using Stream ID: 1 (easy handle 0x558f5d3a5340)
   > HEAD / HTTP/2
   > Host: envoy.disearch.ai
   > user-agent: curl/7.68.0
   > accept: */*
   > 
   * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
   * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
   * old SSL session ID is stale, removing
   * Connection state changed (MAX_CONCURRENT_STREAMS == 100)!
   < HTTP/2 200 
   HTTP/2 200 
   < server: envoy
   server: envoy
   < date: Tue, 08 Oct 2024 21:27:50 GMT
   date: Tue, 08 Oct 2024 21:27:50 GMT
   < content-type: text/html
   content-type: text/html
   < content-length: 615
   content-length: 615
   < last-modified: Wed, 02 Oct 2024 15:13:19 GMT
   last-modified: Wed, 02 Oct 2024 15:13:19 GMT
   < etag: "66fd630f-267"
   etag: "66fd630f-267"
   < accept-ranges: bytes
   accept-ranges: bytes
   < x-envoy-upstream-service-time: 0
   x-envoy-upstream-service-time: 0
   < via: 1.1 google
   via: 1.1 google
   < alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
   alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
   
   <
   * Connection #0 to host envoy.disearch.ai left intact  
   

## TESTING

   Command to test envoy rate limit.  GO inside any gke pod and use this.. it will send traffic to your service running envoy. and you can test the envoy rate limit feature
   
      while true; do curl http://envoy-service:10000/headers; done

   Bash script to test rate limiting 

      # Initialize counters
      count_200=0
      count_429=0
      count_503=0
      count_502=0
      count_other=0
      
      # Loop to send 60 requests
      for i in {1..60}; do
        echo "Request $i:"
        
        # Send request and capture the HTTP response code
        response=$(curl -s -o /dev/null -w "%{http_code}" -I -X GET https://envoy.disearch.ai/)
      
        # Display the response code for each request
        echo "Response code: $response"
        
        # Increment counters based on response code
        if [ "$response" -eq 200 ]; then
          ((count_200++))
        elif [ "$response" -eq 429 ]; then
          ((count_429++))
        elif [ "$response" -eq 503 ]; then
          ((count_503++))
        elif [ "$response" -eq 502 ]; then
          ((count_502++))
        else
          ((count_other++))
        fi
        
        echo ""  # Add a blank line between results for readability
      done
      
      # Print the counts at the end
      echo "Summary:"
      echo "200 responses: $count_200"
      echo "429 responses: $count_429"
      echo "503 responses: $count_503"
      echo "502 responses: $count_502"
      echo "Other responses: $count_other"

      Example Scenario
      Time Frame: 30 seconds
      Configured Limit: 10 requests
      Sequence of Requests
      0-30 seconds: Send 10 requests
      
      Responses: 10 × 200 OK
      30 seconds: Send 1 more request (11th request)
      
      Response: 429 Too Many Requests
      31 seconds: Send another request (12th request)
      
      Response: 429 Too Many Requests
      31-60 seconds: Wait for 30 seconds to allow the rate limit to reset.
      
      60 seconds: Send a request
      
      Response: 200 OK (rate limit reset)
      Summary
      You will not get multiple 429 Too Many Requests responses in rapid succession; it generally only applies to the first request that exceeds the limit.
      After the initial 429, all subsequent requests will continue to receive 429 responses until the rate limit reset occurs after the fill interval.
      Once the limit is reset, you can start sending requests again, and they will return 200 OK until you exceed the limit once more.

