pipeline {
    agent any

    stages {
        stage('Deploy to EC2') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    bat """
                        icacls %SSH_KEY% /inheritance:r
                        icacls %SSH_KEY% /remove "BUILTIN\\Users"
                        icacls %SSH_KEY% /grant:r "SYSTEM:(R)"
                        icacls %SSH_KEY% /grant:r "Administrators:(R)"
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