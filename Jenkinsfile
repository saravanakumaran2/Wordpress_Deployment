pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = 'dockerhub-auth'
        SONARQUBE_SERVER = 'SonarQube'
        SONARQUBE_TOKEN = credentials('sonar-token-id')
        DEV_SERVER = "34.200.161.17"
        DEV_SERVER_CREDENTIALS = "development_server"
        REPO_PATH = "/root/Wordpress_Deployment/"
	}

    stages {
        stage('Code Checkout') {
            steps {
                // Pull the latest code from Git
                checkout scm
            }
        }

        stage('Build Docker Image on Dev Server') {
            steps {
                script {
                    // Dynamically generate the Docker image name
                    def imageName = "your-dockerhub-username/my-image:${env.BUILD_NUMBER}"
                    env.IMAGE_NAME = imageName

                    // SSH into the dev server and build the Docker image
                    sshagent([DEV_SERVER_CREDENTIALS]) {
                        sh """
                        ssh root@${DEV_SERVER} "cd ${REPO_PATH} && docker build -t ${env.IMAGE_NAME} ."
                        """
                    }
                }
            }
        }

        stage('Deploy Container on Dev Server') {
            steps {
                script {
                    // Stop and remove existing container, then run the new one
                    sshagent([DEV_SERVER_CREDENTIALS]) {
                        sh """
                        ssh root@${DEV_SERVER} "docker stop dev-container || true"
                        ssh root@${DEV_SERVER} "docker rm dev-container || true"
                        ssh root@${DEV_SERVER} "docker run --name dev-container -d -p 8082:80 ${env.IMAGE_NAME}"
                        """
                    }
                }
            }
        }

        stage('Test Deployment') {
            steps {
                // Test if the deployment is accessible
                sh '''
                curl -I http://${DEV_SERVER}:8082 || exit 1
                '''
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Push the image to Docker Hub
                    sshagent([DEV_SERVER_CREDENTIALS]) {
                        sh """
                        ssh root@${DEV_SERVER} "docker login -u your-dockerhub-username -p \$(cat /path/to/dockerhub-password-file)"
                        ssh root@${DEV_SERVER} "docker push ${env.IMAGE_NAME}"
                        """
                    }
                }
            }
        }        
    }    
}
