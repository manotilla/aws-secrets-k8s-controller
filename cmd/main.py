
from kubernetes import client, config, watch
CRD_DOMAIN = "woodprogrammer.cloudops.local"

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
        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")
            print(spec)