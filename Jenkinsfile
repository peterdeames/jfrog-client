String upload = BRANCH_NAME == 'main' ? 'python3 -m twine upload --repository pypi dist/*' : 'python3 -m twine upload --repository testpypi dist/*'
def VERSION

pipeline {
  agent any
  options{
    timestamps()
    buildDiscarder logRotator(artifactDaysToKeepStr: '1', artifactNumToKeepStr: '', daysToKeepStr: '7', numToKeepStr: '')
    disableConcurrentBuilds()
    timeout(time: 5, unit: 'MINUTES')
  }
  stages {
    stage('Setup'){
      steps {
        sh 'python3 -m pip install --upgrade pip'
        sh 'pip3 install -r requirements.txt'
        script {
          VERSION = sh (script: 'python3 setup.py --version', returnStdout: true).trim()
        }
      }
    }
    stage('Testing'){
      parallel{
        stage('Quality Testing'){
          stages{
            stage('Pylint') {
              steps {
                sh 'python3 -m pylint jfrog --fail-under=9.0 --output-format=parseable:pylint-report.txt,colorized'
              }
            }
            stage('Unit Tests') {
              steps {
                sh 'python3 -m coverage run --source=jfrog  -m nose2 --verbosity=2'
                sh 'python3 -m coverage xml'
                sh 'python3 -m coverage report -m'
              }
            }
            stage('SonarQube analysis') {
              steps {
                script {
                  def scannerHome = tool 'SonarScanner';
                  withSonarQubeEnv('SonarCloud') {
                    sh "${tool("SonarScanner")}/bin/sonar-scanner -Dsonar.organization=peterdeames -Dsonar.projectKey=peterdeames_jfrog-client -Dsonar.sources=. -Dsonar.branch.name='${env.BRANCH_NAME}' -Dsonar.projectVersion='${VERSION}' -Dsonar.host.url=https://sonarcloud.io -Dsonar.python.version=3.8 -Dsonar.scm.provider=git -Dsonar.python.coverage.reportPaths=coverage.xml -Dsonar.python.bandit.reportPaths=bandit_report.xml -Dsonar.python.pylint.reportPath=pylint-report.txt"
                  }
                }
              }
            }
            stage('Quality gate') {
              steps {
                script {
                  for(int i = 0;i<9;i++) {
                    sleep(10)
                    qualitygate = waitForQualityGate();
                    if(qualitygate.status == 'OK')
                      break;
                  }
                  if (qualitygate.status != "OK") {
                    waitForQualityGate abortPipeline: true
                  }
                }
              }
            }
          }
        }
        stage('Security'){
          stages{
            stage('Bandit'){
              steps{
                echo 'Run Security Tests'
                sh 'python3 -m bandit -r -f xml -o bandit_report.xml .'
                /* snykSecurity (
                  organisation: 'peterdeames',
                  projectName: 'dronedemo',
                  severity: 'critical',
                  snykInstallation: 'Snyk-1.1032.0',
                  snykTokenId: 'Snyk Token',
                  failOnError: False
                ) */
              }
            }
          }
        }
      }
    }
    stage('Build'){
      steps{
        sh 'python3 -m build'
      }
    }
    stage('Publish'){
      when {
        expression { BRANCH_NAME ==~ /(main|develop)/ }
      }
      steps{
        sh "${upload}"
      }
    }
  }
}
