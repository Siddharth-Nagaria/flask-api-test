pipeline {
    agent any

    parameters {
        string(name: 'CI_BUILD_NUMBER', defaultValue: '', description: 'Build number from CI pipeline to deploy')
    }
    
    environment {
        CONFIG_FILE = 'nginix_config.yaml'
        NEXUS_URL = 'https://nexusbiuprod.piramal.com/'
        STACK_NAME = "stack_name"
        // STACK_NAME later to be exracted from environment variables 
        REPO_NAME = "openapi-config"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository'
                script {
                    sh '''
                        rm -rf flask-api-test
                        git clone https://github.com/Siddharth-Nagaria/flask-api-test.git
                    '''
                }
            }
        }

        stage('Load Config') {
            steps {
                script {
                def config = readYaml file: "${CONFIG_FILE}"
                env.APP_NAME = config.jenkins.environment.app_name
                env.IMAGE_NAME = config.jenkins.environment.image_name
                env.CONTAINER_NAME = config.jenkins.environment.container_name
                env.VENV_DIR = config.jenkins.environment.venv_dir
                }
                echo "App Name: ${APP_NAME}"
                echo "Image Name: ${IMAGE_NAME}"
                echo "Container Name: ${CONTAINER_NAME}"
                echo "Virtual Environment Directory: ${VENV_DIR}"
            }
        }

        stage('Setup Virtual Environment and Install Dependencies') {
            steps {
                script {
                    sh '''
                        cd flask-api-test
                        python3 -m venv ${VENV_DIR}
                        ./${VENV_DIR}/bin/pip install --upgrade pip
                        ./${VENV_DIR}/bin/pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Unit tests') {
            steps {
                echo 'Unit tests running'
                script {
                    sh '''
                        cd flask-api-test
                        ./${VENV_DIR}/bin/pytest tests/test_main.py --junitxml=pytest-report.xml -s --log-cli-level=INFO --log-file=pytest-log.txt
                    '''
                }
            }
        }

        stage('Load Build Artifacts') {
            steps {
                script {
                    // Copy build artifacts from config-json job
                    copyArtifacts(
                        projectName: 'json-upload', 
                        selector: lastSuccessful(),
                        filter: 'api-gateway-config.json'
                    )
                    
                    // Load build info JSON
                    def buildInfo = readJSON file: 'api-gateway-config.json'
                    echo "Loaded json configuration"
                }
            }
        }



        stage('YAML File generation'){
            steps{
                script {
            // Creating the JSON file dynamically and generating YAML
                    sh '''
                        python3 openapi_config.py api-gateway-config.json
                        
                        if [ -e "api-gateway-config.yaml" ]; then
                            echo "YAML file Generated"
                        else
                            echo "YAML file not Generated"
                        fi
                        
                        echo "Generated YAML Configuration file : api-gateway-config.yaml"
                        cat api-gateway-config.yaml
                     '''
                }
            }
        }

        stage('Create Raw Repository') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(credentialsId: "nexus-credentials", usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD'),
                        file(credentialsId: 'nexus-certificate', variable: 'CA_CERT_PATH')])
                    {

                        def repoConfig = """
                        {
                            "name": "${REPO_NAME}",
                            "online": true,
                            "storage": {
                                "blobStoreName": "default",
                                "strictContentTypeValidation": true,
                                "writePolicy": "ALLOW"
                            }
                        }
                        """

                        def response = sh(
                            script: """curl -u ${NEXUS_USERNAME}:${NEXUS_PASSWORD} -X POST -H "Content-Type: application/json" -d '${repoConfig}' ${NEXUS_URL}/service/rest/v1/repositories/raw/hosted""",
                            returnStatus: true
                        )

                        if (response != 0) {
                            echo "Repository ${REPO_NAME} might already exist."
                        }
                    }
                }
            }
        }


        stage('Upload to PyPI') {
            steps {
            withCredentials([
                    usernamePassword(credentialsId: "nexus-credentials", usernameVariable: 'NEXUS_USERNAME', passwordVariable: 'NEXUS_PASSWORD'),
                    file(credentialsId: 'nexus-certificate', variable: 'CA_CERT_PATH')
                ]) {
                    def YAML_FILE = "api-gateway-config.yaml"
                    def folder = "${STACK_NAME}-openapi-config"
                    def filePath = "${folder}/${YAML_FILE}"  // Creates a folder with stack name
                    
                    sh """
                    curl -u ${NEXUS_USERNAME}:${NEXUS_PASSWORD} --upload-file ${YAML_FILE} ${NEXUS_URL}/repository/${REPO_NAME}/${filePath}
                    """

                    echo "Uploaded ${YAML_FILE} to Nexus at ${NEXUS_URL}/repository/${REPO_NAME}/${filePath}"

                }
            }
        }




    //     stage('Build Docker Image') {
    //         steps {
    //             echo 'Building a docker Image'
    //             script {
    //                 sh "docker build -t ${IMAGE_NAME} flask-api-test"
    //             }
    //         }
    //     }

    //     stage('Run Unit tests under Docker') {
    //         steps {
    //             echo 'Unit tests running under Docker'
    //             script {
    //                 sh 'docker run --rm $IMAGE_NAME pytest tests/test_main.py'
    //             }
    //         }
    //     }

    //     stage('Stop Existing Container') {
    //         steps {
    //             script {
    //                 sh '''
    //                     docker stop ${CONTAINER_NAME} || true
    //                     docker rm ${CONTAINER_NAME} || true
    //                 '''
    //             }
    //         }
    //     }

    //     stage('Deploy Container') {
    //         steps {
    //             script {
    //                 sh """
    //                 docker ps --filter "publish=5000" -q | xargs -r docker stop
    //                 docker ps -a --filter "publish=5000" -q | xargs -r docker rm
    //                 docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}
    //                 """
    //             }
    //         }
    //     }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pytest-report.xml', fingerprint: true
            junit 'pytest-report.xml'
            
            withAWS(credentials: 'aws-credentials-uat', region: 'ap-south-1') {
                s3Upload(file: 'pytest-report.xml', bucket: 'data-engg-uat', path: 'mlops/flask-test-results/')
                s3Upload(file: 'pytest-log.txt', bucket: 'data-engg-uat', path: 'mlops/flask-test-results/')
            }
        }
        
        success {
            echo "CD Pipeline successful! Docker Image running in the container"
        }
        failure {
            echo "CD Pipeline failed!"
        }
    }
}
