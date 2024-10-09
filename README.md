# Deploying envoy proxy with helm chart

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
    
    
