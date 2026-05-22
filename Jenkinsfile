pipeline {
    agent any

    stages {
        stage('Deploy to EC2') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    bat """
                        ssh -i %SSH_KEY% -o StrictHostKeyChecking=no ubuntu@32.197.189.124 "cd satellite-anomaly-detector && git pull && docker compose down && docker compose up --build -d"
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}