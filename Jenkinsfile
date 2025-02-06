pipeline {
    agent any
    
    environment {
        APP_NAME ="flask-app"
        IMAGE_NAME = "flask-app:latest"
        CONTAINER_NAME = "flask-container"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repoitory'
                script{
                    git 'https://github.com/Nirmalya-Mukherjee_biuuser/flask-tests.git'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Building a docke Image'
                script{
                    sh 'docker build -t $IMAGE_NAME'
                }
            }
        }
        stage('Run Unit tests') {
            steps {
                echo 'Unit tests running'
                script {
                    sh 'docker run --rm $IMAGE_NAME pytest tests.py'
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    sh 'docker stop $CONTAINER_NAME || true'
                    sh 'docker rm $CONTAINER_NAME || true'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    sh 'docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME'
                }
            }
        }
    }
}