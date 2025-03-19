pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/user/repo.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Regression Tests') {
            steps {
                sh 'pytest -m regression --junitxml=report.xml'
            }
        }
        stage('Publish Reports') {
            post {
                always {
                    junit 'report.xml'
                }
            }
        }
    }
}
