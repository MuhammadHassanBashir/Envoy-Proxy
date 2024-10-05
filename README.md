You can give envoy.yaml file through configmap to envoy pod by creating and mount volume to pod, and then pod container will get envoy file from specfic set directory.

or 

You can provide the envoy.yaml file to the Envoy pod by creating a ConfigMap and mounting a volume to the pod. This way, the container within the pod will retrieve the envoy.yaml file from the specified directory.
