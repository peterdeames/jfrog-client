<a name="readme-top"></a>
<div align="center">

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

[![Bugs][bugs-badge]][sonar-url]
[![Code Smells][codesmells-badge]][sonar-url]
[![Code Coverage][coverage-badge]][sonar-url]
[![Lines of Code][loc-badge]][sonar-url]
[![Duplicated Lines][duplicatedlines-badge]][sonar-url]
[![Vulnerabilities][vulnerabilities-badge]][sonar-url]

[![Quality Gate Status][qualitygate-badge]][sonar-url]
[![Maintainability Rating][maintainability-badge]][sonar-url]
[![Reliability Rating][reliability-badge]][sonar-url]
[![Security Rating][security-badge]][sonar-url]


<!-- PROJECT LOGO -->
<br />
<h2 align="center">JFrog Client</h2>

  <p align="center">
    API Calls to interact with Jfrog
    <br />
    <a href="https://github.com/peterdeames/jfrog-client"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/peterdeames/jfrog-client/issues">Report Bug</a>
    ·
    <a href="https://github.com/peterdeames/jfrog-client/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is collection of API calls that interact with the Jfrog Platform to help maintain daily operations such as checking the health, getting current version, getting storage usage, user details, create repos etc.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python.org]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/peterdeames/jfrog-client.git
   ```
2. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
<!-- ## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- ROADMAP -->
## Roadmap

- [ ] Platform
    - [x] Get Count of Users
    - [x] Generate Token
    - [x] Get Tokens
    - [x] Get Default Token Expiry
    - [x] Set Default Expiry
- [ ] Artifactory
    - [x] Ping Artifactory Instance
    - [x] Get Artifactory Version
    - [x] Get Artifactory Licence Details
    - [x] Get Count of Repositories
    - [x] Rename Repository
- [ ] Mission Control
    - [X] Ping Mission Control Instance
- [ ] Xray
    - [x] Ping Xray Instance
    - [x] Get Xray Version
- [ ] Migration
    - [ ] Setup and Migrate Local Repos
    - [ ] Setup Remote Repos
    - [ ] Setup Virtual Repos
    - [ ] Setup Groups
    - [ ] Setup Permissions
    - [ ] Setup Projects
    - [x] Report the repos differences between 2 JFP Instances
    - [x] Report the group differences between 2 JFP Instances
    - [x] Report the permission differences between 2 JFP Instances
    - [x] Report the artifact differences between 2 JFP Instances


See the [open issues](https://github.com/peterdeames/jfrog-client/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/peterdeames/jfrog-client](https://github.com/peterdeames/jfrog-client)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/peterdeames/jfrog-client.svg?style=for-the-badge
[contributors-url]: https://github.com/peterdeames/jfrog-client/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/peterdeames/jfrog-client.svg?style=for-the-badge
[forks-url]: https://github.com/peterdeames/jfrog-client/network/members
[stars-shield]: https://img.shields.io/github/stars/peterdeames/jfrog-client.svg?style=for-the-badge
[stars-url]: https://github.com/peterdeames/jfrog-client/stargazers
[issues-shield]: https://img.shields.io/github/issues/peterdeames/jfrog-client.svg?style=for-the-badge
[issues-url]: https://github.com/peterdeames/jfrog-client/issues
[license-shield]: https://img.shields.io/github/license/peterdeames/jfrog-client.svg?style=for-the-badge
[license-url]: https://github.com/peterdeames/jfrog-client/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-0769AD?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org

[sonar-url]: https://sonarcloud.io/summary/new_code?id=peterdeames_jfrog-client
[bugs-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=bugs
[codesmells-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=code_smells
[coverage-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=coverage
[loc-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=ncloc
[duplicatedlines-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=duplicated_lines_density
[vulnerabilities-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=vulnerabilities

[qualitygate-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=alert_status
[maintainability-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=sqale_rating
[reliability-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=reliability_rating
[security-badge]: https://sonarcloud.io/api/project_badges/measure?project=peterdeames_jfrog-client&metric=security_rating