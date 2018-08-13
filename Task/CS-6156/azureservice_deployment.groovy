import groovy.json.JsonSlurper

node('autoscale'){
    try {
        timestamp {
            stage('Clone Repository') {
                dir('test-autmation') {
                    deleteDir()
                    git branch: "${env.BRANCH}", credentialsId: '6d7f65a6-b7a7-4ace-9a4a-8cffd00bca04', url :'git@gitlab.corp.cloudsimple.com:cloudsimple/test-automation.git'
                }
            }
            stage('Tar repository') {
                sh(
                '''
                tar -cvzf test-auto.tgz test-automation/
                '''
                )
            }
            stage('Copy to jumpbox') {
                sh(
                '''
                scp test-auto.tgz swati@52.183.83.17:/home/swati/snehasish/
                '''
                )
            }
        }
    } catch (e) {
         currentBuild.result = "FAILED"
         throw e
      }
}
                
node('network-slave'){
    try {
        timestamps {
            stage('Clone repository') {
                dir('test-automation') {
                //Delete the existing contents
                // deleteDir()
                sh(
                '''
                tar -xvzf /home/swati/snehasish/test-auto.tgz -C ${WORKSPACE}
                '''
                )
              } 
            }

            stage("Install Dependencies"){
                sh(
                '''
                echo "installing dependencies"
                pip install --upgrade pip
                pip install -r ${WORKSPACE}/test-automation/ssh_requirements.txt
                '''
                )
            }

            stage("Run tests"){
              dir('test-automation'){
                    sh(
                    '''
                    python /home/swati/snehasish/ssh.py
                    '''
                    )
                }
            }
         }
    } catch (e) {
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
    }
}

