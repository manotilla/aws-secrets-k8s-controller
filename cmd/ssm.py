import boto3

class AWSSecret(object):
    def __init__(self):
        self.ssm_client = boto3.client('ssm')

    def _single_parameter(self, parameter_name):
        
        data = self.ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return data["Parameter"]["Value"]

    def convert(self, parameter_prefix, secret_name, splitter):
        file_name = "/tmp/"+secret_name+".yaml"
        with open(file_name, "a+") as file_ptr:
            paginator = self.ssm_client.get_paginator('describe_parameters')
            recursive_ssm = paginator.paginate(
                ParameterFilters=[
                    dict(Key="Path", Option="Recursive", Values=[parameter_prefix])
                ]
            )
            for rs in recursive_ssm:
                for parameter in rs['Parameters']:
                    value = self._single_parameter(parameter["Name"])
                    key = parameter["Name"].split(splitter)
                    file_ptr.write("{}: {}\n".format(key[len(key)-1], value))
        return file_name
