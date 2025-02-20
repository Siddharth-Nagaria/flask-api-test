import json
import os
import yaml

vpc_id = os.getenv('CONNECTION_ID','__VPC_ID__')
load_balancer_listener = os.getenv('LOAD_BALANCER_LISTNER', '__LOAD_BALANCER_LISTNER__')
domain_name = os.getenv('DOMAIN_NAME','__DOMAIN_NAME__')
stack_name = os.getenv('STACK_NAME','__STACK_NAME__')


# The substituted values need to be removed once the variables are initialized

if vpc_id is None:
    raise ValueError("vpc_id not found")

if load_balancer_listener is None:
    raise ValueError("load_balancer_listener not found")

if domain_name is None:
    raise ValueError("domain_name not found")

if stack_name is None:
    raise ValueError("stack_name not found")

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
        **({'security': [ { f"{stack_name}_dynamic_auth": [] } ]} if path_type == 'External' else {}),
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
            'overwrite:path' : '$request.path'
            },
            'payloadFormatVersion': "1.0",
            'connectionId': vpc_id,
            'type': "http_proxy",
            'httpMethod': "ANY",
            'uri': load_balancer_listener,
            'connectionType':"VPC_LINK",
            'timeoutInMillis': 30000,
            'tlsConfig': {
                    'serverNameToVerify': domain_name
            }
        }
    }


yaml_data["components"] = {
    "securitySchemes": {
        f"{stack_name}_dynamic_auth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "x-amazon-apigateway-authorizer": {
                "identitySource": "$request.header.Authorization",
                "authorizerUri": "arn:aws:apigateway:ap-south-1:lambda:path/2015-03-31/functions/arn:aws:lambda:ap-south-1:581962035245:function:validate_dynamic_bearer_token/invocations",
                "authorizerPayloadFormatVersion": "2.0",
                "authorizerResultTtlInSeconds": 0,
                "type": "request",
                "enableSimpleResponses": False
            }
        }
    }
}

# Output the YAML to a file
yaml_file_path = f"api-gateway-config.yaml"
with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)

print(f"YAML file '{yaml_file_path}' generated successfully.")