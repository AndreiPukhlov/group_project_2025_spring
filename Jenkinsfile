pipeline {
    agent any

    stages {
        stage('Debug Workspace') {
            steps {
                sh '''#!/bin/bash
                    echo "Workspace: $(pwd)"
                    ls -l
                '''
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AndreiPukhlov/group_project_2025_spring.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Regression Tests') {
            steps {
                sh '''#!/bin/bash
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