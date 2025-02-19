import json
import os
import yaml

# Retrieve environment variables
vpc_id = os.getenv('CONNECTION_ID', '__VPC_ID__')
load_balancer_listener = os.getenv('LOAD_BALANCER_LISTNER', '__LOAD_BALANCER_LISTNER__')
domain_name = os.getenv('DOMAIN_NAME', '__DOMAIN_NAME__')

# Read the JSON configuration file
with open('api_gateway_config.json') as file:
    config = json.load(file)

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

    # Construct the path and method structure
    yaml_data['paths'][path] = {
        method: {
            'responses': {
                'default': {
                    'description': f"Default response for {method.upper()} {path}"
                }
            },
            'x-amazon-apigateway-integration': {
                'responseParameters': {
                    '200': {
                        'remove:header.apigw': "''",
                        'remove:header.server': "''",
                        'remove:header.RequestId': "''",
                        'remove:header.vary': "''"
                    }
                },
                'payloadFormatVersion': "1.0",
                'connectionId': vpc_id,
                'type': "http_proxy",
                'httpMethod': "ANY",
                'uri': load_balancer_listener,
                'timeoutInMillis': 30000,
                'tlsConfig': {
                    'serverNameToVerify': domain_name
                }
            }
        }
    }

# Output the YAML to a file
yaml_file_path = f"api_gateway_config.yaml"
with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)

print(f"YAML file '{yaml_file_path}' generated successfully.")