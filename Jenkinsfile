// pipeline {
//     agent any
    
//     environment {
//         CONFIG_FILE = 'nginix_config.yaml'
//     }

//     stages {
//         stage('Clone Repository') {
//             steps {
//                 echo 'Cloning the repository'
//                 script{
//                     sh'''
//                         rm -rf flask-api-test
//                         git clone https://github.com/Siddharth-Nagaria/flask-api-test.git
//                      '''
//                 }
//             }
//         }
//         stage('Setup Virtual Environment and Install Dependencies') {
//             steps {
//                     sh 'cd flask-api-test'
//                     sh 'python3 -m venv ${VENV_DIR}'
//                     sh './${VENV_DIR}/bin/pip install --upgrade pip'
//                     sh './${VENV_DIR}/bin/pip install -r requirements.txt'
//             }
//         }
//         stage('Run Unit tests') {
//             steps {
//                 echo 'Unit tests running'
//                 script {
//                     sh 'cd flask-api-test'
//                     sh './${VENV_DIR}/bin/pytest flask-api-test/tests/test_main.py --junitxml=pytest-report.xml -s --log-cli-level=INFO --log-file=pytest-log.txt'
//                 }
//             }
//         }
//         stage('Build Docker Image') {
//             steps {
//                 echo 'Building a docker Image'
//                 script{
//                     sh 'docker build -t env.${IMAGE_NAME} flask-api-test'
//                 }
//             }
//         }
//         stage('Run Unit tests under docker') {
//             steps {
//                 echo 'Unit tests running'
//                 script {
//                     sh 'docker run --rm env.${IMAGE_NAME} pytest tests/test_main.py'
//                 }
//             }
//         }

//         stage('Stop Existing Container') {
//             steps {
//                 script {
//                     sh 'docker stop ${CONTAINER_NAME} || true'
//                     sh 'docker rm ${CONTAINER_NAME} || true'
//                 }
//             }
//         }

//         stage('Deploy Container') {
//             steps {
//                 script {
//                     sh 'docker run -d -p 5000:5000 --name env.${CONTAINER_NAME} env.${IMAGE_NAME}'
//                 }
//             }
//         }
//     }

//     post {

//         always {
//             archiveArtifacts artifacts: 'pytest-report.xml', fingerprint: true
//             junit 'pytest-report.xml'
            
//             withAWS(credentials: 'aws-credentials-uat', region: 'ap-south-1') {
//             s3Upload(file: 'pytest-report.xml', bucket: 'data-engg-uat', path: 'mlops/flask-test-results/')
//             s3Upload(file: 'pytest-log.txt', bucket: 'data-engg-uat', path: 'mlops/flask-test-results/')
//             }
//         }
        
//         success {
//             echo "CD Pipeline successful! Docker Image running in the container"
//         }
//         failure {
//             echo "CD Pipeline failed!"
//         }
//     }
// }



pipeline {
    agent any
    
    environment {
        CONFIG_FILE = 'flask-api-test/nginix_config.yaml'
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

        stage('Build Docker Image') {
            steps {
                echo 'Building a docker Image'
                script {
                    sh "docker build -t ${IMAGE_NAME.toLowerCase()} flask-api-test"
                }
            }
        }

        stage('Run Unit tests under Docker') {
            steps {
                echo 'Unit tests running under Docker'
                script {
                    sh "docker run --rm ${IMAGE_NAME.toLowerCase()} pytest tests/test_main.py"
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    sh "docker run -d -p 5000:5000 --name ${CONTAINER_NAME.toLowerCase()} ${IMAGE_NAME.toLowerCase()}"
                }
            }
        }
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
