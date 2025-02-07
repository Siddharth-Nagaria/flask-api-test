pipeline {
    agent any
    
    environment {
        APP_NAME ="flask-app"
        IMAGE_NAME = "flask-app:latest"
        CONTAINER_NAME = "flask-container"
        VENV_DIR = "my_venv"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository'
                script{
                    sh'''
                        rm -rf flask-api-test
                        git clone https://github.com/Siddharth-Nagaria/flask-api-test.git
                     '''
                }
            }
        }
        stage('Setup Virtual Environment and Install Dependencies') {
            steps {
                    sh 'cd flask-api-test'
                    sh 'python3 -m venv ${VENV_DIR}'
                    sh './${VENV_DIR}/bin/pip install --upgrade pip'
                    sh './${VENV_DIR}/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Unit tests') {
            steps {
                echo 'Unit tests running'
                script {
                    sh 'cd flask-api-test'
                    sh './${VENV_DIR}/bin/pytest flask-api-test/tests/test_main.py'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Building a docker Image'
                script{
                    sh 'docker build -t ${IMAGE_NAME} flask-api-test'
                }
            }
        }
        stage('Run Unit tests under docker') {
            steps {
                echo 'Unit tests running'
                script {
                    sh 'docker run --rm ${IMAGE_NAME} pytest tests/test_main.py'
                }
            }
        }

        // stage('Stop Existing Container') {
        //     steps {
        //         script {
        //             sh 'docker stop ${CONTAINER_NAME} || true'
        //             sh 'docker rm ${CONTAINER_NAME} || true'
        //         }
        //     }
        // }

        stage('Deploy Container') {
            steps {
                script {
                    sh 'docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME}'
                }
            }
        }
    }
}
