pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/AndreiPukhlov/group_project_2025_spring.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Regression Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    python -m pytest tests/
                '''
            }
        }
    }

    post {
        always {
            junit '**/test-results.xml'
        }
    }
}