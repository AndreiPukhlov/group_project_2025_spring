pipeline {
    agent {
        docker {
            image 'your-custom-python-image'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
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