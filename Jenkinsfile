pipeline {
    agent any

    environment {
        DEV_SERVER = "3.99.104.202"  // Update with your dev server IP
        DEV_SERVER_CREDENTIALS = "development_server"
        REPO_PATH = "/opt/project"
        IMAGE_NAME = "custom-wordpress:latest"
        DOCKER_HUB_CREDENTIALS = 'dockerhub-auth' // Add this if it's not already set
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                cleanWs()  // Cleanup workspace
            }
        }

        stage('Code Checkout') {
            steps {
                checkout scm  // Checkout the source code from the repository
            }
        }

        stage('Copy Files to Dev Server') {
            steps {
                sshagent([DEV_SERVER_CREDENTIALS]) {
                    sh """
                    scp -r * root@${DEV_SERVER}:${REPO_PATH}
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sshagent([DEV_SERVER_CREDENTIALS]) {
                    sh """
                    ssh root@${DEV_SERVER} "
                        cd ${REPO_PATH} &&
                        docker build -t ${IMAGE_NAME} .
                    "
                    """
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                sshagent([DEV_SERVER_CREDENTIALS]) {
                    sh """
                    ssh root@${DEV_SERVER} "
                        cd ${REPO_PATH} &&
                        docker-compose down &&
                        docker-compose up -d
                    "
                    """
                }
            }
        }

        stage('Test Deployment') {
            steps {
                sshagent([DEV_SERVER_CREDENTIALS]) {
                    sh """
                    curl -I http://${DEV_SERVER}:8080 || exit 1
                    """
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Push the image to Docker Hub
                    sshagent([DEV_SERVER_CREDENTIALS]) {
                        withCredentials([usernamePassword(credentialsId: DOCKER_HUB_CREDENTIALS, usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                            sh """
                            ssh root@${DEV_SERVER} "docker login -u \$USERNAME -p \$PASSWORD"
                            ssh root@${DEV_SERVER} "docker push ${IMAGE_NAME}"
                            """
                        }
                    }
                }
            }
        }
    }
}
