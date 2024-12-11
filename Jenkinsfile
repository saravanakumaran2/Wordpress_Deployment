pipeline {
    agent any

    environment {
        STAGING_SERVER = "52.60.108.120"  // Staging server IP address
        STAGING_SERVER_CREDENTIALS = "staging_server"  // Staging server credentials
        IMAGE_NAME = "saravana227/custom-wordpress:latest"
    }

    stages {
        stage('Cleanup Workspace') {
            steps {
                cleanWs()  // Cleanup workspace
            }
        }

        stage('Pull Docker Image from Docker Hub') {
            steps {
                sshagent([STAGING_SERVER_CREDENTIALS]) {
                    sh """
                    ssh root@${STAGING_SERVER} "
                        docker pull ${IMAGE_NAME}
                    "
                    """
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
