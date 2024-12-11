pipeline {
    agent any

    environment {
        production_server = "52.60.169.243"  // Staging server IP address
        production_server_CREDENTIALS = "production_server"  // Staging server credentials
        IMAGE_NAME = "saravana227/custom-wordpress:staging"
        DOCKER_HUB_CREDENTIALS = "dockerhub-auth"  // Docker Hub credentials
        REPO_PATH = "/opt/project/"
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
                sshagent([production_server_CREDENTIALS]) {
                    sh """
                    scp -r * root@${production_server}:${REPO_PATH}
                    """
                }
            }
        }
        stage('Pull Docker Image from Docker Hub') {
            steps {
                sshagent([production_server_CREDENTIALS]) {
                    withCredentials([usernamePassword(credentialsId: DOCKER_HUB_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh """
                        ssh root@${production_server} "
                            cd ${REPO_PATH} &&
                            echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin &&
                            docker pull ${IMAGE_NAME}
                        "
                        """
                    }
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                sshagent([production_server_CREDENTIALS]) {
                    sh """
                    ssh root@${production_server} "
                     cd ${REPO_PATH} &&
                     chmod 777 * && 
                    docker-compose down -v && 
                    if [ \$(docker ps -q) ]; then
                    docker stop \$(docker ps -q);
                    docker rm -f \$(docker ps -a -q);
                    fi &&
                    docker-compose up -d
                    "
                    """
                }
            }
        }

        stage('Test Deployment') {
            steps {
                sshagent([production_server_CREDENTIALS]) {
                    sh """
                    curl -I http://${production_server}:80 || exit 1
                    """
                }
            }
        }
    }
}
