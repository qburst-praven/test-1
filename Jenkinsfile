pipeline {
    agent any
    
    environment {
        APP_NAME = 'test-1'
        DOCKER_REGISTRY = 'ghcr.io'
        GITHUB_OWNER = 'qburst-praven'
        IMAGE_NAME = "${DOCKER_REGISTRY}/${GITHUB_OWNER}/${APP_NAME}"
    }
    
    triggers {
        // GitHub webhook trigger
        githubPush()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.SHORT_COMMIT = sh(script: "git rev-parse --short=7 HEAD", returnStdout: true).trim()
                    echo "Building commit: ${env.SHORT_COMMIT}"
                }
            }
        }
        
        stage('Build and Test') {
            steps {
                script {
                    echo "Building Python Flask application: ${APP_NAME}"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_NAME}:${env.SHORT_COMMIT}"
                    sh """
                        docker build -t ${IMAGE_NAME}:${env.SHORT_COMMIT} .
                        docker tag ${IMAGE_NAME}:${env.SHORT_COMMIT} ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    // Login to GitHub Container Registry and push images
                    withCredentials([usernamePassword(credentialsId: 'github-container-registry', 
                                                     usernameVariable: 'REGISTRY_USER', 
                                                     passwordVariable: 'REGISTRY_PASS')]) {
                        sh """
                            echo \${REGISTRY_PASS} | docker login ${DOCKER_REGISTRY} -u \${REGISTRY_USER} --password-stdin
                            docker push ${IMAGE_NAME}:${env.SHORT_COMMIT}
                            docker push ${IMAGE_NAME}:latest
                        """
                    }
                    
                    // Clean up local images
                    sh """
                        docker rmi ${IMAGE_NAME}:${env.SHORT_COMMIT} || true
                        docker rmi ${IMAGE_NAME}:latest || true
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying ${APP_NAME} to Kubernetes cluster"
                    
                    // Update deployment manifest with new image tag
                    sh """
                        yq eval '.spec.template.spec.containers[0].image = "${IMAGE_NAME}:${env.SHORT_COMMIT}"' -i k8s/deployment.yaml
                    """
                    
                    // Apply Kubernetes manifests (Jenkins runs in-cluster, so no kubeconfig needed)
                    sh """
                        # Apply Kubernetes manifests
                        kubectl apply -f k8s/namespace.yaml
                        kubectl apply -f k8s/deployment.yaml  
                        kubectl apply -f k8s/service.yaml
                        kubectl apply -f k8s/ingress.yaml
                        
                        # Wait for deployment to be ready
                        kubectl rollout status deployment/${APP_NAME} -n ${APP_NAME} --timeout=300s
                        
                        # Show deployment status
                        kubectl get pods -n ${APP_NAME} -l app=${APP_NAME}
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "Pipeline completed successfully for ${APP_NAME}!"
            echo "Image: ${IMAGE_NAME}:${env.SHORT_COMMIT}"
        }
        failure {
            echo "Pipeline failed for ${APP_NAME}"
        }
    }
} 
