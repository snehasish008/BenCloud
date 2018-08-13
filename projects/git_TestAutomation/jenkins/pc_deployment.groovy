import groovy.json.JsonSlurper

node('devops-slave-1') {
    try {
        // Adds timestamps to the output logged by steps inside the wrapper.
        timestamps {
            // Set Env and Checkout Repositories
            stage('Clone sources') {
                dir('test-automation') {
                    // Clean the current directory
                    deleteDir()
                    git branch: "${env.TEST_BRANCH}", credentialsId: '6d7f65a6-b7a7-4ace-9a4a-8cffd00bca04', url: 'git@gitlab.corp.cloudsimple.com:cloudsimple/test-automation.git'
                }
                dir('deployment') {
                    // Clean the current directory
                    deleteDir()
                    git branch: "${env.DEPLOYMENT_BRANCH}", credentialsId: '6d7f65a6-b7a7-4ace-9a4a-8cffd00bca04', url: 'git@gitlab.corp.cloudsimple.com:cloudsimple/deployment.git'
                }
            }

            // Install Dependencies
            stage('Install Dependencies') {
                sh(
                '''
                # Install all dependencies 
                sudo pip install --upgrade pip
                sudo pip install -r ${WORKSPACE}/test-automation/requirements.txt
                '''
                )    
            }
    
            // Create dynamic testbed config
            stage("Create Config") {
                dir('deployment') {
                    sh(
                    '''
                    # Create and copy the config file to the config directory
                    ./scripts/device42_import/gen_pc_config.py --sheet ${SHEET_ID} --envname ${ENVIRONMENT} \
                        --filename ../test-automation/config/${ENVIRONMENT}  --atuser ${ANSIBLE_USER} \
                        --atpwd ${ANSIBLE_PASSWORD} --atip ${ANSIBLE_TOWER} --param ../test-automation/config/pc_param.yml
                    '''
                    )
                }
            }
 
            // Run the tests through ansible tower
            stage("Run Tests") {
                dir('test-automation') {
                    sh(
                    '''
                    # Test ansible workflows
                    python -m pytest -m regression -x -v --html=devops-sanity-report.html --self-contained-html --confcutdir=tests/devops/ \
                        tests/devops/test_deployment.py
                    '''
                    )
                }
            }
        }
    } catch (e) {
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
    } finally {
        timestamps {
            // Publish HTML Report
            stage('Publish Report') {
                publishHTML([
                    allowMissing: false, 
                    alwaysLinkToLastBuild: false, 
                    keepAll: false, 
                    reportDir: 'test-automation',
                    reportFiles: 'devops-sanity-report.html', 
                    reportName: 'DevOps_Sanity_Report', 
                    reportTitles: 'DevOps_Sanity_Report'
                ])
            }
            
            // Notify by Email, Slack
            stage('Send Notification') {
                dir('test-automation') {
                    // Success or failure, always send notifications
                    notifyBuild(currentBuild.result)
                }
            }
        }
    }
}

def notifyBuild(String buildStatus) {
    // build status of null means successful
    buildStatus =  buildStatus ?: 'SUCCESS'
 
    // Default values
    def colorName = 'RED'
    def colorCode = '#FF0000'
    def subject = "${buildStatus}: Job '${env.JOB_NAME}' Build ${env.BUILD_NUMBER}"
    def summary = "${subject} (${env.BUILD_URL})"
    def reportFile = 'devops-sanity-report.html'
    def details = """
         <p>Check console output at "<a href="${env.BUILD_URL}">${env.BUILD_URL}</a>"</p>
    """
    if (fileExists(reportFile)) {
        details = readFile file: reportFile        
    }
 
    // Override default values based on build status
    if (buildStatus == 'SUCCESS') {
        slackSend (
            color: '#00FF00',
            message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Success (<${env.BUILD_URL}|Open>)"
        )
    } else {
        slackSend (
            color: '#FF0000',
            message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failure (<${env.BUILD_URL}|Open>)"
        )
    }
 
    emailext (
        subject: subject,
        body: details,
        mimeType: 'text/html',
        attachmentsPattern: 'config/${ENVIRONMENT}.yml',
        to: 'g-jenkins-notify@cloudsimple.com'
    )
}