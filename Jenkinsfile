
node('linuxVM') {
    printMessage("Pipeline Start")

    stage("Fetch Source Code") {
        git "https://github.com/BoxenOfDonuts/nhl_lights"
    }

    stage("Install Requirements") {
        sh 'make install'
    }

    stage("Run Tests") {
        sh 'python test_functions.py'
    }

    stage("Deploy") {
        if (env.BRANCH_NAME == "master") {
            printMessage("deploying master branch")
        } elseif (env.BRANCH_NAME == 'develop')
            printMessage("deploying develop branch")

            sh 'cd /home/joel/Projects/tmp/'
            git "https://github.com/BoxenOfDonuts/nhl_lights"
            sh 'make install'

        } else {
            printMessage("no deployment specified for this branch")
        }
    }

    printMessage("Pipeline End")
}

def printMessage(message) {
    echo "${message}"
}