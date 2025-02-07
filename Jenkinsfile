pipeline {
    agent any
    
    environment {
        APP_NAME ="flask-app"
        IMAGE_NAME = "flask-app:latest"
        CONTAINER_NAME = "flask-container"
    }

    stages {
        // stage('Checkout Code') {
        //     steps {
        //         checkout([$class: 'GitSCM', 
        //         branches: [[name: '*/main']], 
        //         userRemoteConfigs: [[
        //             url: 'https://github.com/Siddharth-Nagaria/flask-api-test.git',
        //             // credentialsId: 'nirmalya-git-creds'
        //         ]]
        // ])

        //     }
        // }
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
        stage('Setup Virtual Env and Install Dependencies') {
        steps {
            sh '''
                python -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
            '''
            }
        }
        stage('Run Unit tests') {
            steps {
                echo 'Unit tests running'
                script {
                    sh 'source venv/bin/activate'
                    sh 'pytest test_main.py'
                }
            }
        }
        // stage('Build Docker Image') {
        //     steps {
        //         echo 'Building a docker Image'
        //         script{
        //             sh 'docker build -t $IMAGE_NAME'
        //         }
        //     }
        // }
        // stage('Run Unit tests under docker') {
        //     steps {
        //         echo 'Unit tests running'
        //         script {
        //             sh 'docker run --rm $IMAGE_NAME pytest test_main.py'
        //         }
        //     }
        // }

        // stage('Stop Existing Container') {
        //     steps {
        //         script {
        //             sh 'docker stop $CONTAINER_NAME || true'
        //             sh 'docker rm $CONTAINER_NAME || true'
        //         }
        //     }
        // }

        // stage('Deploy Container') {
        //     steps {
        //         script {
        //             sh 'docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME'
        //         }
        //     }
        // }
    }
}
