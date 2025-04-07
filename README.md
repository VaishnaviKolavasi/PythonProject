###### PythonProject – SAST with SonarQube & GitHub Actions #######
 
This project showcases how to catch security issues early using Static Application Security Testing (SAST) with SonarQube Cloud and GitHub Actions.
It includes a simple, intentionally vulnerable Flask app to demonstrate how tools can spot common coding flaws automatically.

##### What’s Inside
- vuln_code.py: Sample Flask app with known security issues
- .github/workflows/build.yml: GitHub Actions workflow for SAST
- sonar-project.properties: Config for SonarQube scanning

#### How Security Scanning Works
SonarQube + GitHub Actions
SAST scans run automatically on every push to main and during pull requests.

using the actions:
actions/checkout@v4 – Checks out your code
sonarsource/sonarqube-scan-action@v5 – Runs the scan

#### Secrets Used (set in GitHub secrects)
SONAR_TOKEN: Auth token for SonarQube
SONAR_HOST_URL: URL of your SonarQube instance

#### Run It Locally

$ git clone https://github.com/VaishnaviKolavasi/PythonProject.git
$ cd PythonProject
$ python vuln_code.py



