pipeline {
    agent any

    environment {
        DEV_SERVER = "3.99.104.202"  // Update with your dev server IP
        DEV_SERVER_CREDENTIALS = "development_server"
        REPO_PATH = "/opt/project"
        IMAGE_NAME = "saravana227/custom-wordpress:latest"
        IMAGE_NAME_STAGING = "saravana227/custom-wordpress:staging"
        DOCKER_HUB_CREDENTIALS = 'dockerhub-auth' // Add this if it's not already set
        SONARQUBE_TOKEN = credentials('sonar-token')  // Assuming you've created a Jenkins credential with the SonarQube token
        SONAR_SCANNER_PATH = '/opt/sonar-scanner/bin/sonar-scanner'
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

        stage('SonarQube Analysis') {
    steps {
        script {
            // This triggers the SonarQube analysis with hard-coded authentication details
            sh '''
            sonar-scanner \
                -Dsonar.projectKey=Project \
                -Dsonar.projectName="Project" \
                -Dsonar.projectVersion=1.0.0 \
                -Dsonar.sources=. \
                -Dsonar.php.version=7.4 \
                -Dsonar.host.url=http://15.223.157.208:9000 \
                -Dsonar.login=admin \  # Hard-coded username
                -Dsonar.password=123  # Hard-coded password
            '''
        }
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
                        # Build the 'staging' tag
                        docker build -t ${IMAGE_NAME_STAGING} .
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
                    docker-compose down -v && 
                    if [ \$(docker ps -q) ]; then
                    docker stop \$(docker ps -q);
                    docker rm -f \$(docker ps -a -q);
                    fi &&
                    ssh root@${DEV_SERVER} "docker push ${IMAGE_NAME_STAGING}"
                    docker-compose up -d --build
                    "
                    """
                }
            }
        }

        stage('Test Deployment') {
            steps {
                sshagent([DEV_SERVER_CREDENTIALS]) {
                    sh """
                    curl -I http://${DEV_SERVER}:80 || exit 1
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
