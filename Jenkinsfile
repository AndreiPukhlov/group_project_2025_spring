pipeline {
    agent any

    environment {
        M2_HOME = '/path/to/maven'
        PATH = "${M2_HOME}/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AndreiPukhlov/group_project_2025_spring.git'
            }
        }
         stage('Debug Environment') {
            steps {
                sh '''#!/bin/bash
                    echo "PATH: $PATH"
                    which sh
                    which bash
                    which python3
                    which pip
                '''
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
                    python -m pytest tests/ --junitxml=test-results.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
        }
    }
}