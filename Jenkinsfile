pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker compose'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out the latest code from GitHub...'
                git branch: 'main', url: 'https://github.com/nikhil-codingn-s/employee-management.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🐳 Building Docker images...'
                sh '''
                    ${DOCKER_COMPOSE} build
                '''
            }
        }

        stage('Deploy Containers') {
            steps {
                echo '🚀 Deploying updated containers...'
                sh '''
                    echo "🧹 Stopping old containers..."
                    ${DOCKER_COMPOSE} down || true

                    echo "🧽 Cleaning up old containers, networks, and volumes..."
                    docker container prune -f || true
                    docker network prune -f || true
                    docker volume prune -f || true

                    echo "⚙️ Starting new containers..."
                    ${DOCKER_COMPOSE} up -d

                    echo "✅ All containers are up and running!"
                    docker ps
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 ✅ Deployment completed successfully!'
        }
        failure {
            echo '❌ Deployment failed! Check Jenkins logs for details.'
        }
        always {
            echo '📜 Pipeline execution finished.'
        }
    }
}

