
node('linuxVM') {
    printMessage("Pipeline Start")

    stage("Fetch Source Code") {

        gitSSH()

    }

    //stage("Install Requirements") {
    //    sh 'make install'
    //}

    stage("Run Tests") {
        printMessage("haha no testing here")
    }

    stage("Deploy") {
        if (env.BRANCH_NAME == "master") {
            printMessage("deploying master branch")
        } else if (env.BRANCH_NAME == 'develop') {
        dir('/home/joel/Projects/tmp/') {
                printMessage("deploying develop branch")
                gitSSH()
                virtualenv()
         }

        } else {
            printMessage("no deployment specified for this branch")
        }
    }

    printMessage("Pipeline End")
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
    . venv/bin/activate
    pip install -r requirements.txt
    """
}