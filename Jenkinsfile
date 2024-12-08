pipeline {
    agent any
    stages {
        stage('Info') {
            steps {
                echo "Job: ${env.JOB_NAME} is building on branch ${env.GIT_BRANCH} and build-id is ${env.BUILD_ID}"
                sh 'sleep 5'
            }
        }
        stage('Build') {
            steps {
                echo "this is build stage"
                sh 'sleep 5'
            }
        }
        stage('Test') {
            steps {
                echo "this is test stage"
                sh 'sleep 5'
            }
        }
        stage('Deploy') {
            steps {
                echo "this is deploy stage"
                sh 'sleep 5'
            }
        }
    }
}
