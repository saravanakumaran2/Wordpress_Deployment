pipeline {
    agent any
    environment {
        SONAR_PROJECT_KEY = 'website'
        SONAR_HOST_URL = 'http://15.223.157.208:9000'
        SONAR_CREDENTIALS_ID = 'sonar-token'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    if (env.GIT_BRANCH != 'origin/development') {
                        error "Skipping code quality analysis for branch: ${env.GIT_BRANCH}"
                    }
                }
            }
        }
        stage('Build') {
            steps {
                echo "Building the project..."
            }
        }
        stage('Test') {
            steps {
                echo "Running tests..."
            }
        }
        stage('SonarQube Analysis') {
            steps {
                echo "Running SonarQube analysis for branch: ${env.GIT_BRANCH}"
                withCredentials([string(credentialsId: SONAR_CREDENTIALS_ID, variable: 'SONAR_TOKEN')]) {
                    sh '''
                    sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline completed."
        }
        success {
            echo "Pipeline executed successfully."
        }
        failure {
            echo "Pipeline execution failed."
        }
    }
}
