import base64
import json
import yaml

from kubernetes import client, config

class Zapata(object):
    def __init__(self):
        pass
    
    def create_secret_as_file(self, mount_file_secret, mount_file_name, secret_name, namespace):

        config.load_kube_config()
        v1 = client.CoreV1Api()
        tmp_content = open(mount_file_name, "r")

        data = {mount_file_secret: tmp_content.read() }
         
        secret = client.V1Secret(
            api_version="v1",
            string_data=data,
            kind="Secret",
            metadata=dict(name=secret_name, namespace=namespace),
            type="Opaque",
        )
        
        response = v1.create_namespaced_secret(namespace, body=secret)
        tmp_content.close()
        return response

    def create_secret_as_env(self, secret_name, namespace):

        config.load_kube_config()
        v1 = client.CoreV1Api()
        tmp_content = open("/tmp/{}.yaml".format(secret_name), "r")

        tmp_yaml = yaml.safe_load(tmp_content)
        tmp_arr = {}

        for item, doc in tmp_yaml.items():
            tmp_encode = base64.b64encode(str.encode(doc))
            tmp_arr[item] = tmp_encode.decode()

        secret = client.V1Secret(
            api_version="v1",
            data=tmp_arr,
            kind="Secret",
            metadata=dict(name=secret_name, namespace=namespace),
            type="Opaque",
        )
        
        response = v1.create_namespaced_secret(namespace, body=secret)
        tmp_content.close()
        tmp_arr = {}
        return response

