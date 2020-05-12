pipeline {
    agent {
        node {
            label 'linuxVM'
        }
    }
    stages {
            stage("Run Tests") {
                printMessage("haha no testing here")
            }

            stage("Deploy") {
                if (env.BRANCH_NAME == "master") {
                    printMessage("deploying master branch")
                    dir('/home/joel/Projects/python/nhl_lights/') {
                            deleteDir()
                            printMessage("deploying develop branch")
                            gitSSH()
                            virtualenv()

                            withCredentials([file(credentialsId: '3aef7477-0710-48ee-b0de-fb207aeeb069', variable: 'FILE')]) {
                                sh 'cp $FILE config.ini'
                        }
                     }
                } else if (env.BRANCH_NAME == 'develop') {
                dir('/home/joel/Projects/tmp/nhl_lights/') {
                    deleteDir()
                        printMessage("deploying develop branch")
                        gitSSH()
                        virtualenv()

                        withCredentials([file(credentialsId: '3aef7477-0710-48ee-b0de-fb207aeeb069', variable: 'FILE')]) {
                            sh 'cp $FILE config.ini'
                        }

                }

                } else {
                    printMessage("no deployment specified for this branch")
                }
            }
    }
    post {
        always {
            deleteDir()
            printMessage("Pipeline End")
        }
    }
}

def printMessage(message) {
    echo "${message}"
}

def gitSSH() {
    git branch: env.BRANCH_NAME,
        credentialsId: '14bc68af-bf7a-4bf6-aa8a-6e99940d3413',
        url: 'ssh://git@github.com/BoxenOfDonuts/nhl_lights.git'
}

def virtualenv() {
    sh """
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    """
}