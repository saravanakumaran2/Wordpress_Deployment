pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "flask-app"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Cleanup') {
            steps {
                cleanWs() 
            }
        }

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Copy Files to Remote Server') {
            steps {
                sshagent(['development_server']) {
                    sh '''
                    scp -r * root@3.99.104.202:/opt/project/
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sshagent(['development_server']) {
                    sh '''
                    ssh root@3.99.104.202 "cd /opt/project/app && docker build -t ${DOCKER_IMAGE_NAME} ."
                    '''
                }
            }
        }

        stage('Deploy to Development Server') {
            steps {
                sshagent(['development_server']) {
                    sh '''
                    ssh root@3.99.104.202 'docker pull ${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:latest'
                    ssh root@3.99.104.202 'cd /opt/project && docker-compose -f ${DOCKER_COMPOSE_FILE} up -d'
                    '''
                }
            }
        }

        stage('Test Website') {
            steps {
                sshagent(['development_server']) {
                    sh '''
                    ssh root@3.99.104.202 "curl -I http://3.99.104.202:5000"
                    '''
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                sshagent(['development_server']) {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-auth', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh '''
                        ssh root@3.99.104.202 "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        ssh root@3.99.104.202 "docker tag ${DOCKER_IMAGE_NAME}:latest ${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:latest"
                        ssh root@3.99.104.202 "docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:latest"
                        '''
                    }
                }
            }
        }

    }

    post {
        success {
            echo 'Pipeline finished successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}
