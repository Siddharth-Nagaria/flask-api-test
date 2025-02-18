# import json
# import os

# vpc_id = os.getenv('CONNECTION_ID', '__VPC_ID__')
# load_balancer_listener = os.getenv('LOAD_BALANCER_LISTNER', '__LOAD_BALANCER_LISTNER__')
# domain_name = os.getenv('DOMAIN_NAME', '__DOMAIN_NAME__')

# with open('api_gateway_config.json') as file:
#     config = json.load(file)

# # extracting path, method, type and description
# paths = config['paths']

# paths_section = ""
# for item in paths:
#     path = item['path']
#     method = item['method'].lower()
#     description = item['Description']

# # OpenAPI paths and methods structure
# paths_section += f"  {path}:\n"
# paths_section += f"    {method}:\n"
# paths_section += f"      responses:\n"
# paths_section += f"        default:\n"
# paths_section += f"          description: \"Default response for {method.upper()} {path}\"\n"
# paths_section += f"      x-amazon-apigateway-integration:\n"
# paths_section += f"        responseParameters:\n"
# paths_section += f"          '200':\n"
# paths_section += f"            remove:header.apigw: \"''\"\n"
# paths_section += f"            remove:header.server: \"''\"\n"
# paths_section += f"            remove:header.RequestId: \"''\"\n"
# paths_section += f"            remove:header.vary: \"''\"\n"
# paths_section += f"        payloadFormatVersion: \"1.0\"\n"
# paths_section += f"        connectionId: {vpc_id}\n"
# paths_section += f"        type: \"http_proxy\"\n"
# paths_section += f"        httpMethod: \"ANY\"\n"
# paths_section += f"        uri: {load_balancer_listener}\n"
# paths_section += f"        timeoutInMillis: 30000\n"
# paths_section += f"        tlsConfig:\n"
# paths_section += f"          serverNameToVerify: {domain_name}\n"

# with open('Jenkinsfile', 'r') as jenkinsfile:
#     content = jenkinsfile.read()

# content = content.replace('${paths}', paths_section)

# with open('Jenkinsfile', 'w') as jenkinsfile:
#     jenkinsfile.write(content)

# print("Jenkinsfile updated successfully.")


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
yaml_file_path = f"api_gateway_config_{vpc_id}.yaml"
with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)

print(f"YAML file '{yaml_file_path}' generated successfully.")