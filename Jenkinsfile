pipeline {
    agent any

    environment {
        STAGING_SERVER = "52.60.108.120"  // Staging server IP address
        STAGING_SERVER_CREDENTIALS = "staging_server"  // Staging server credentials
        IMAGE_NAME = "saravana227/custom-wordpress:latest"
        DOCKER_HUB_CREDENTIALS = "dockerhub-auth"  // Docker Hub credentials
        REPO_PATH = "/opt/project"
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
                sshagent([STAGING_SERVER_CREDENTIALS]) {
                    sh """
                    sudo mkdir -p /opt/project
                    scp -r docker-compose.yml root@${STAGING_SERVER}:${REPO_PATH}
                    """
                }
            }
        }
        stage('Pull Docker Image from Docker Hub') {
            steps {
                sshagent([STAGING_SERVER_CREDENTIALS]) {
                    withCredentials([usernamePassword(credentialsId: DOCKER_HUB_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh """
                        ssh root@${STAGING_SERVER} "
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
                sshagent([STAGING_SERVER_CREDENTIALS]) {
                    sh """
                    ssh root@${STAGING_SERVER} "
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
                sshagent([STAGING_SERVER_CREDENTIALS]) {
                    sh """
                    curl -I http://${STAGING_SERVER}:80 || exit 1
                    """
                }
            }
        }
    }
}
