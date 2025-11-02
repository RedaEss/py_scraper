// Jenkinsfile - VERSION PYTHON 
pipeline {
    agent {
        docker {
            image 'python:3.9-slim'  // ← Image Python légère
            args '-u root'  // Permissions root
        }
    }
    
    options {
        timeout(time: 10, unit: 'MINUTES')  
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }
    
    parameters {
        choice(
            name: 'BRANCH',
            choices: ['development', 'main'],
            description: 'Branche à builder'
        )
    }
    
    triggers {
        pollSCM('H/15 * * * *')
    }
    
    environment {
        DOCKER_IMAGE = 'basta-scraper-python'  
        RESULTS_DIR = 'jenkins-results'
    }
    
    stages {
        stage('Checkout & Setup') {
            steps {
                checkout scm
                script {
                    if (params.BRANCH != 'development') {
                        sh "git checkout ${params.BRANCH}"
                        echo "✅ Branche changée vers: ${params.BRANCH}"
                    }
                }
                sh """
                    echo "=== VARIABLES PYTHON ==="
                    echo "DOCKER_IMAGE: ${DOCKER_IMAGE}"
                    echo "BRANCH: ${params.BRANCH}"
                    python --version
                    pip --version
                """
            }
        }
        
        stage('Build Image') {
            steps {
                sh "docker build -t ${env.DOCKER_IMAGE} ."
            }
        }
        
        stage('Run Scraper') {
            steps {
                sh """
                    mkdir -p ${env.RESULTS_DIR}
                    docker run --rm \
                      -v \$(pwd)/${env.RESULTS_DIR}:/results \
                      ${env.DOCKER_IMAGE}
                """
            }
        }
        
        stage('Validate Results') {
            steps {
                sh """
                    echo "🔍 Validation des résultats Python..."
                    if ls ${env.RESULTS_DIR}/*.csv 1> /dev/null 2>&1; then
                        echo " SUCCÈS : Fichiers CSV générés"
                        echo " Contenu :"
                        ls -la ${env.RESULTS_DIR}/
                    else
                        echo " ÉCHEC : Aucun fichier CSV trouvé"
                        exit 1
                    fi
                """
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: "${env.RESULTS_DIR}/*", fingerprint: true
        }
        
        success {
            echo "✅ Pipeline Python réussi - Branche: ${params.BRANCH}"
        }
        
        failure {
            echo " Pipeline Python échoué - Branche: ${params.BRANCH}"
        }
    }
}