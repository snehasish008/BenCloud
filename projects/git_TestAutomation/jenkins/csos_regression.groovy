import groovy.json.JsonSlurper

node('autoscale') {
    try {
        // Adds timestamps to the output logged by steps inside the wrapper.
        timestamps {
            // Set Env and Checkout Repositories
            stage('Clone sources') {

                dir('CSOS') {
                    // Clean the current directory
                    deleteDir()
                    git credentialsId: '6d7f65a6-b7a7-4ace-9a4a-8cffd00bca04', url: 'git@gitlab.com:cloudsimple/control-plane.git'
                }

                dir('TestAutomation') {
                    // Clean the current directory
                    deleteDir()
                    git credentialsId: '6d7f65a6-b7a7-4ace-9a4a-8cffd00bca04', url: 'git@gitlab.com:cloudsimple/test-automation.git'
                }

            }

            // Install Dependencies
            stage('Install Dependencies') {
                sh(
                '''
                # Install all dependencies
                apk add --no-cache \
                   py-pip \
                   linux-headers \
                   build-base \
                   libffi-dev \
                   musl-dev \
                   jq \
                   openssh \
                   mariadb-dev \
                   mysql-client

                # Start sshd manually
                /usr/bin/ssh-keygen -A
                /usr/sbin/sshd

                sleep 10

                #Install all dependencies
                pip install --upgrade pip
                pip install docker-compose
                pip install pytest
                pip install pyVmomi
                pip install pytest-html
                pip install prettytable
                pip install requests
                pip install -r ${WORKSPACE}/TestAutomation/requirements.txt
                '''
                )
            }

            // Build CSOS Binaries
            stage('Login to the CloudSimple Docker Registry') {
                dir('CSOS') {
                    sh(
                    """
                    # Docker login to "registry.gitlab.com"
                    docker login -u=${GITLAB_REGISTRY_LOGIN} -p=${GITLAB_REGISTRY_PASSWD} registry.gitlab.com
                    """
                    )
                }
            }

            // Deploy the containers
            stage('Deploy TestBed') {
                dir('CSOS') {
                    sh(
                    """
                    # Clean-up previous deployment if any
                    cd docker && docker-compose down && cd -
                    sleep 5

                    # Deploy the new environment
                    #until [[ \$(docker-compose -f docker/docker-compose.yml ps | grep init | grep -ic 'exit 0') -gt "0" ]]; do echo "Waiting for CSOS initialization..."; sleep 1; done
                    docker-compose -f docker/docker-compose.yml up -d
                    sleep 90

                    # Copy the testbed config to 'rim' service
                    #if [[ \$(docker cp ../TestAutomation/config/ansible_tower_pcs.json rim:/opt/rim/config/) -gt "0" ]]; then echo "Testbed config copy failed.."; fi
                    docker cp ../TestAutomation/config/ansible_tower_pcs.json rim:/opt/rim/config/
                    docker cp ../TestAutomation/config/rim.yml rim:/opt/rim/config/
                    docker restart rim
                    sleep 60
                    """
                    )
                }
            }

            // Login to API Service
            stage('Run End-to-End Tests') {
                // Get the API Service IP
                API_SERVICE_IP = sh(
                        script: "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api",
                        returnStdout: true
                ).trim()

                echo "API Service IP: ${API_SERVICE_IP}"

                dir('TestAutomation') {
                    sh(
                    """
                    # Edit the e2e config file and replace the API Service IP
                    sed -i 's/API_SERVICE_IP/${API_SERVICE_IP}/g' config/csos_e2e.json

                    # Remove migrate-to-dvs from the verification steps
                    sed -i '/migrate-to-dvs/d' config/csos_e2e.json

                    # Temporary Steps
                    # The api server login is not running. Use the alternate version of the test file.
                    #cat /var/configs/tests/test_privatecloud.py > tests/csos/e2e_tests/test_privatecloud.py

                    # Run the tests
                    python -m pytest -v --html=automation_logs/csos-e2e-test-report.html --self-contained-html \
        	            tests/csos/e2e_tests/test_privatecloud.py
                    """
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
            // Clean-up the TestBed
            stage('Teardown TestBed') {
                dir('CSOS') {
                    sh(
                    """
                    # Collect logs
                    docker-compose -f docker/docker-compose.yml logs

                    # Clean-up the Testbed
                    cd docker && docker-compose down && cd -

                    # Remove the deployed containers
                    docker rmi -f \$(docker images | grep control-plane | grep -v csos_base | awk '{ print \$3 }')
                    """
                    )
                }
            }

            // Publish HTML Report
            stage('Publish Report') {
                dir('TestAutomation') {
                    publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: false,
                            keepAll: false,
                            reportDir: 'automation_logs',
                            reportFiles: 'csos-e2e-test-report.html',
                            reportName: 'CSOS_End-to-End_Tests_Report',
                            reportTitles: 'CSOS_End-to-End_Tests'
                    ])
                }
            }

            // Notify by Email, Slack
            stage('Send Notification') {
                dir('TestAutomation') {
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
    def reportFile = 'automation_logs/csos-e2e-test-report.html'
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
                message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failed (<${env.BUILD_URL}|Open>)"
        )
    }

    emailext (
            subject: subject,
            body: details,
            mimeType: 'text/html',
            to: 'g-jenkins-notify@cloudsimple.com'
    )
}
