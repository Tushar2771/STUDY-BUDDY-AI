pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "tushar2301/studdybuddy"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout Github') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Tushar2771/STUDY-BUDDY-AI.git']])
            }
        }        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:${IMAGE_TAG}")
                }
            }
        }
        stage('Push Image to DockerHub') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    docker.withRegistry('https://registry.hub.docker.com' , "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push("${IMAGE_TAG}")
                    }
                }
            }
        }
        stage('Update Deployment YAML with New Tag') {
            steps {
                script {
                    sh """
                    sed -i 's|image: tushar2301/studdybuddy:[^"]*|image: tushar2301/studdybuddy:${IMAGE_TAG}|' manifests/deployment.yaml

                    """
                }
            }
        }

        stage('Commit Updated YAML') {
    steps {
        script {
            withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                sh '''
                git config user.name "Tushar2771"
                git config user.email "tusharrane2301@gmail.com"

                # Only commit & push if file changed
                if ! git diff --quiet manifests/deployment.yaml; then
                  echo "Changes detected in deployment.yaml, committing..."
                  git add manifests/deployment.yaml
                  git commit -m "Update image tag to ${IMAGE_TAG} [skip ci]"
                  git push https://${GIT_USER}:${GIT_PASS}@github.com/Tushar2771/STUDY-BUDDY-AI.git HEAD:main
                else
                  echo "No changes in deployment.yaml, skipping commit."
                fi
                '''
            }
        }
    }
}
        }
        stage('Install Kubectl & ArgoCD CLI Setup') {
            steps {
                sh '''
                echo 'installing Kubectl & ArgoCD cli...'
                curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                chmod +x kubectl
                mv kubectl /usr/local/bin/kubectl
                curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
                chmod +x /usr/local/bin/argocd
                '''
            }
        }
        stage('Apply Kubernetes & Sync App with ArgoCD') {
            steps {
                script {
                    kubeconfig(credentialsId: 'kubeconfig', serverUrl: 'https://192.168.49.2:8443') {
                        sh '''
                        argocd login 34.9.235.144:31704 --username admin --password $(kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) --insecure
                        argocd app sync studdybuddy
                        '''
                    }
                }
            }
        }
    }
}