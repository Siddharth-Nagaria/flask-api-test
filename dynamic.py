import json
import os
import yaml
from collections import OrderedDict


# Read the JSON configuration file
with open('api-gateway-config.json') as file:
    config = json.load(file)

# response codes listed here
response_codes = [200,201,400,500,204,403]

# Extracting paths, method, type, and description
paths = config['paths']

# Prepare the YAML structure
yaml_data = {
    'paths': {}
}

for item in paths:
    path = item['path']
    method = item['method'].lower()
    description = item['Description']
    path_type = item['Type']

    if path not in yaml_data['paths']:
        yaml_data['paths'][path] = {}

    # Construct the path and method structure
    yaml_data['paths'][path][method] ={
        'responses': {
            'default': {
                    'description': f"Default response for {method.upper()} {path}"
                }
        },
        **({'security': [ { "openapi_config": [] } ]} if path_type == 'External' else {}),
        'x-amazon-apigateway-integration':{
            'responseParameters': {
                str(code): {
                    'remove:header.apigw': "''",
                    'remove:header.server': "''",
                    'remove:header.RequestId': "''",
                    'remove:header.vary': "''"
                } for code in response_codes
            },
            'requestParameters' : {
            'append:header.username' : '$context.authorizer.username',
            'overwrite:path' : path
            },
            'payloadFormatVersion': "1.0",
            'connectionId': 'zblprn',
            'type': "http_proxy",
            'httpMethod': "ANY",
            'uri': 'arn:aws:elasticloadbalancing:ap-south-1:581962035245:listener/app/fs-services-jenkins-v2-ALB/d51ecb12b6abeb19/febb90681043995b',
            'connectionType':"VPC_LINK",
            'timeoutInMillis': 30000,
            'tlsConfig': {
                    'serverNameToVerify': 'biuuatapi.piramalfinance.com'
            }
        }
    }

# Output the YAML to a file
yaml_file_path = f"api-gateway-config.yaml"
with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)

print(f"YAML file '{yaml_file_path}' generated successfully.")