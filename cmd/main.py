
from kubernetes import client, config, watch
import os
from zapata import Zapata
from ssm import AWSSecret
CRD_DOMAIN = "woodprogrammer.io"

if __name__ == "__main__":

    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.ApiextensionsV1beta1Api(api_client)
    crds = client.CustomObjectsApi(api_client)

    aws_obj = AWSSecret()
    k8s_obj = Zapata()


    while True:
        resource_version = ''
        stream = watch.Watch().stream(crds.list_cluster_custom_object, CRD_DOMAIN, "v1", "cloudsecrets", resource_version=resource_version)
        print("Basladik aq")
        for event in stream:

            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")

            if operation == "DELETED":
                print("K8S Secret {} deleting".format(event))
            
            elif operation == "ADDED":
                try:            
                    type_of_k8s_secret = spec["type"]
                    namespace = spec["namespace"]
                    prefix_of_k8s_secret = spec["prefix"]
                    secret_name   = spec["secret_name"]

                    resp = aws_obj.convert(prefix_of_k8s_secret, secret_name, "/")

                    if type_of_k8s_secret == "file":    
                        mount_file_name = spec["mount_file_name"]
                        k8s_obj.create_secret_as_file(mount_file_name, "/tmp/{}.yaml".format(secret_name), secret_name, namespace)
                    
                    elif type_of_k8s_secret == "env":
                        k8s_obj.create_secret_as_env(secret_name, namespace)

                except Exception as exp:
                    print(exp)
