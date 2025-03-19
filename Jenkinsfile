pipeline {
    agent any  // Runs the pipeline on any available agent

    environment {
        // Add environment variables that are needed globally, if required
        SELENIUM_HEADLESS = 'true'  // Example to force headless mode
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository to the Jenkins workspace
                git 'https://github.com/AndreiPukhlov/group_project_2025_spring.git'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    // Check if the virtual environment exists
                    if (!fileExists('.venv')) {
                        // If .venv doesn't exist, create it and install dependencies
                        sh 'python3 -m venv .venv'  // Create the virtual environment
                        sh '.venv/bin/pip install --upgrade pip'  // Upgrade pip
                        sh '.venv/bin/pip install -r requirements.txt'  // Install dependencies
                    }
                }
            }
        }

        stage('Load Environment Variables') {
            steps {
                script {
                    // Check if the .env file exists and load it
                    if (fileExists('.env')) {
                        sh 'export $(cat .env | grep -v "^#" | xargs)'  // Export env variables from .env file
                    } else {
                        echo ".env file not found"
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Activate the virtual environment and run tests with pytest
                    sh '.venv/bin/pytest -m "regression and not bug and not skip"'
                }
            }
        }
    }

    post {
        always {
            // Optional: Clean up or report results
            echo 'Cleaning up after tests...'
        }
        success {
            echo 'Tests passed!'
        }
        failure {
            echo 'Tests failed!'
        }
    }
}
