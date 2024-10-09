Deploying envoy proxy with helm chart

## Command to test Cors

  -> curl -i -X OPTIONS https://envoy.disearch.ai -H "Origin: http://test-origin-1.com" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: content-type"

    **Cors Response after successfull completion with set origin http://test-origin-1.com**  
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
    
  ->  curl -i -X OPTIONS https://envoy.disearch.ai -H "Origin: http://test-host-2.com" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: content-type"
    
    **Cors Response after successfull completion with set origin: http://test-host-2.com**
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


