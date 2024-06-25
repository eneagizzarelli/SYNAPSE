<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/eneagizzarelli/synapse">
    <img src="SYNAPSE_logo.png" alt="Logo" width="220" height="220">
  </a>

  <h3 align="center"><strong>SYNAPSE: SYNthetic AI Pot for Security Enhancement</strong></h3>

  <p align="center">
    <a href="https://github.com/eneagizzarelli/synapse/issues/new?labels=bug&template=bug_report.md">Report Bug</a>
    ·
    <a href="https://github.com/eneagizzarelli/synapse/issues/new?labels=enhancement&template=feature_request.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About the project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About the project

**SYNAPSE** is a 
- low-interaction 
- server
- dynamic

**honeypot** acting as a Linux OS terminal. It is entirely written in Python. Instead of relying on a real terminal, SYNAPSE works with **generative AI** (currently _GPT 4o_ model) to answer with realistic terminal outputs, as if the user was connecting to a real Linux OS using SSH. It currently implements the simulation of two services:
 - SSH Server
 - MySQL Server
 
SYNAPSE leverages the [**SYNAPSE-to-MITRE**](https://github.com/eneagizzarelli/SYNAPSE-to-MITRE.git) submodule to automatically map collected logs into attack techniques of the [**MITRE ATT&CK**](https://attack.mitre.org) database. For a more detailed description of SYNAPSE-to-MITRE project, installation, usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation

1. Clone this repository
   ```sh
   git clone https://github.com/eneagizzarelli/SYNAPSE.git
   ```
2. Enter the project folder and install requirements
   ```sh
   pip install -r requirements.txt
   ```
4. Create a .env file and add your OpenAI key
   ```js
   OPENAI_API_KEY='YOUR KEY';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage 

Modify your `/etc/ssh/sshd_config` file in order to run `startSYNAPSE.sh` script whenever a user connects to your machine using SSH. Example:
```sh
Match User enea
	ForceCommand /home/enea/SYNAPSE/scripts/startSYNAPSE.sh
	X11Forwarding no
	AllowTcpForwarding no
	AllowAgentForwarding no
	PermitTunnel no
	PermitOpen none
```
In our configuration, SYNAPSE project folder has been cloned in a machine under the specific path _/home/enea/SYNAPSE_. Every script/source file in this project refers to other scripts/source files using the above absolute path as a base path. If you use a different configuration, remember to change the path everywhere.

Also, if you are hosting the code on a VM like AWS EC2 and you want to allow password authentication, remember to change your `/etc/ssh/sshd_config.d/50-cloud-init.conf` file setting `PasswordAuthentication yes`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Enea Gizzarelli - eneagizzarelli2000@gmail.com

[LinkedIn](https://linkedin.com/in/eneagizzarelli)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- OTHER PROJECTS -->
## Other projects

**SYNAPSE**: [https://github.com/eneagizzarelli/SYNAPSE](https://github.com/eneagizzarelli/synapse)

**SYNAPSE-to-MITRE**: [https://github.com/eneagizzarelli/SYNAPSE-to-MITRE](https://github.com/eneagizzarelli/synapse-to-mitre)

**DENDRITE**: [https://github.com/eneagizzarelli/DENDRITE](https://github.com/eneagizzarelli/dendrite)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

- [shelLM](https://github.com/stratosphereips/SheLLM)
- [GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS -->
[contributors-shield]: https://img.shields.io/github/contributors/eneagizzarelli/synapse.svg?style=for-the-badge
[contributors-url]: https://github.com/eneagizzarelli/synapse/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/eneagizzarelli/synapse.svg?style=for-the-badge
[forks-url]: https://github.com/eneagizzarelli/synapse/network/members

[stars-shield]: https://img.shields.io/github/stars/eneagizzarelli/synapse.svg?style=for-the-badge
[stars-url]: https://github.com/eneagizzarelli/synapse/stargazers

[issues-shield]: https://img.shields.io/github/issues/eneagizzarelli/synapse.svg?style=for-the-badge
[issues-url]: https://github.com/eneagizzarelli/synapse/issues

[license-shield]: https://img.shields.io/github/license/eneagizzarelli/synapse.svg?style=for-the-badge
[license-url]: https://github.com/eneagizzarelli/synapse/blob/main/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/eneagizzarelli
