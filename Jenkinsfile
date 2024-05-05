pipeline {
    agent any

    stages {
        stage('Check Python Version') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('Install Requirements') {
            steps {
                withPythonEnv('python3') {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Run Pre-commit Hooks') {
            steps {
                sh 'pre-commit run --all-files'
            }
        }
        stage('Run Python Scripts') {
            steps {
                withPythonEnv('python3') {
                    sh 'python3 -m behave'
                }
            }
        }
        stage('Generate Reports') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure/results']]
                    ])
                }
            }
        }
    }
}
