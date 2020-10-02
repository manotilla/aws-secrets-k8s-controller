
from kubernetes import client, config, watch
import os
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
                    prefix_of_k8s_secret = spec["prefix"]
                    print(type_of_k8s_secret)
                except Exception as exp:
                    print(exp)
