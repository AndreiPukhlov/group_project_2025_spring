pipeline {
    agent any
    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin" // Adjust if needed
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AndreiPukhlov/group_project_2025_spring.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '/usr/bin/env bash -c "pip3 install -r requirements.txt"'
            }
        }
        stage('Run Regression Tests') {
            steps {
                sh 'pytest -m regression --junitxml=report.xml || true'
            }
        }
    }
    post {
        always {
            junit '**/report.xml'
        }
    }
}

