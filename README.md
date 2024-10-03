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

Install envoy on ubuntu focal:

      wget -O- https://apt.envoyproxy.io/signing.key | sudo gpg --dearmor -o /etc/apt/keyrings/envoy-keyring.gpg
      echo "deb [signed-by=/etc/apt/keyrings/envoy-keyring.gpg] https://apt.envoyproxy.io focal main" | sudo tee /etc/apt/sources.list.d/envoy.list
      sudo apt-get update
      sudo apt-get install envoy
      envoy --version
      

