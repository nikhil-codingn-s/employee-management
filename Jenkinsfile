pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker compose'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nikhil-codingn-s/employee-management.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'sudo ${DOCKER_COMPOSE} build'
            }
        }

        stage('Deploy Containers') {
            steps {
                sh 'sudo ${DOCKER_COMPOSE} down'
                sh 'sudo ${DOCKER_COMPOSE} up -d'
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed!'
        }
    }
}
