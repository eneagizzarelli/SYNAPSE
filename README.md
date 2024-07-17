<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License: CC BY-NC-SA 4.0][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/eneagizzarelli/SYNAPSE">
    <img src="SYNAPSE_logo.png" alt="Logo" width="220" height="220">
  </a>

  <h3 align="center">SYNAPSE: SYNthetic AI Pot for Security Enhancement</h3>

  <p align="center">
    <a href="https://github.com/eneagizzarelli/SYNAPSE/issues/new?labels=bug&template=bug_report.md">Report Bug</a>
    ·
    <a href="https://github.com/eneagizzarelli/SYNAPSE/issues/new?labels=enhancement&template=feature_request.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About the project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#use-cases">Use cases</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contacts">Contacts</a></li>
    <li><a href="#other-projects">Other projects</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About the project

**SYNAPSE** is a 
- low-interaction 
- server
- dynamic

**honeypot** acting as a Linux OS terminal. It is entirely written in Python. Instead of relying on a real terminal, SYNAPSE works with **generative AI** (currently _GPT-4o_ model) to answer with realistic terminal outputs, as if the user was connecting to a real Linux OS using SSH. It currently implements the simulation of two services:
 - SSH Server
 - MySQL Server.

Generative AI, in this context, will be used to generate responses to issued commands both for the simulated Linux terminal and for the fake MySQL service, leveraging **prompt engineering** techniques. [shelLM](https://github.com/stratosphereips/SheLLM) project was used as a starting point to implement SYNAPSE code.

**SYNAPSE-to-MITRE** extension automatically maps logs collected by SYNAPSE into attacks of the [**MITRE ATT&CK**](https://attack.mitre.org) database, leveraging **machine learning** technologies. More in detail, a MLP classifier has been trained to achieve the desired behaviour. The dataset used to train the model is the one proposed by [cti-to-mitre-with-nlp](https://github.com/dessertlab/cti-to-mitre-with-nlp), re-created using the (currently) last version of the MITRE ATT&CK database (_enterprise-attack-15.1_). Generative AI, in this context, will be used both for deciding if an attack happened or not, and to generate a brief sentence summing up the eventual attack.

[GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) database is used to obtain geolocation information about the connected IP address. [VirusTotal](https://www.virustotal.com/gui/home/upload) APIs are used to get client IP address reputation among the other data extracted by the honeypot. Also, for each log of commands, reputations of IPs and domains entered by the user/attacker (e.g. _ping_ to a certain IP address or _wget_ from a certain domain) are fetched. All these information will be provided to the AI as additional factors to decide whether an attack happened or not.

Among its features, SYNAPSE supports **multiple sessions** for the same user. Each IP address will have its own simulated file system for each subsequent session. Different users will never see modifications done by others. File system file and directories together with MySQL databases and tables will be populated creatively (dinamically) by generative AI.

With the aim of a **comparative evaluation**, a static equivalent of SYNAPSE has been implemented: [**DENDRITE**](https://github.com/eneagizzarelli/DENDRITE).

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

3. Create a .env file (in my configuration under `/home/enea/.env`) and add your OpenAI and VirusTotal API keys
   ```sh
   OPENAI_API_KEY='YOUR KEY'
   VIRUSTOTAL_API_KEY='YOUR KEY'
   ```
   
**Note 1**: in my configuration, SYNAPSE project folder has been cloned under the specific path `/home/enea/SYNAPSE`. Every script/source file in this project refers to other scripts/source file using the above absolute path as a base path. If you plan to use an alternative configuration, like different location or user, remember to change the paths and to replace _enea_ everywhere.

4. Copy `configSYNAPSE.sh` script from `scripts/` folder outside the `SYNAPSE` directory and, after assigning the necessary permissions, run it
   ```sh
   chmod +x configSYNAPSE.sh
   ./configSYNAPSE.sh
   ```
    This will complete the configuration of SYNAPSE, creating the necessary folders, downloading GeoLite2 database and assigning ownership and permissions to user _enea_ (or the one you specifically decided).

5. Modify your `/etc/ssh/sshd_config` file in order to run `startSYNAPSE.sh` script (after assigning the necessary permissions) and to disable many SSH parameters (not handled by the code) whenever user _enea_ (or the one you specifically decided) connects to your machine using SSH:
   ```sh
   Match User enea
      ForceCommand /home/enea/SYNAPSE/scripts/startSYNAPSE.sh
      X11Forwarding no
      AllowTcpForwarding no
      AllowAgentForwarding no
      PermitTunnel no
      PermitOpen none
   ```

**Note 2**: if you are hosting the code on a VM like _AWS EC2_ and you want to allow password authentication, remember to change your `/etc/ssh/sshd_config.d/50-cloud-init.conf` file setting `PasswordAuthentication yes` (`60-cloudimg-settings.conf` for _Oracle Cloud Infrastructure_).

6. Restart your SSH service
   ```sh
   systemctl restart sshd
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Adopting the aforementioned configuration will run SYNAPSE "fake" terminal instead of the real one whenever user _enea_ (or the one you specifically decided) connects to your SSH server.

While SYNAPSE is running, many _classification files_ will be created in the `logs` directory. Those files will have a name format like `IPaddr_classification_history_NUM.txt`, and will contain the history of commands the user with IP address _IPaddr_ issued on its session number _NUM_. Over those files **SYNAPSE-to-MITRE** extension will operate. After assigning the necessary permissions, executing the script `./startSYNAPSE-to-MITRE.sh` will automatically convert _classification files_ into _attack files_ containing the corresponding MITRE ATT&CK object content, if AI thinks the attack happened.

If you plan to rebuild the dataset from scratch, the `startDatasetBuild.sh` script can be run. You'll need to replace _capec_ or _enterprise-attack_ databases in the `SYNAPSE-to-MITRE/data` folder with the versions you prefer (you can download them from the repositories linked in the below _acknowledgments_ section). Make sure to leave file and folder names unchanged. In the end, the model can be trained with the newly generated dataset using the `startModelTraining.sh` script.

**Note 3**: if you experience an error like `Resource SOMETHING not found` and, further on, `>>> nltk.download('SOMETHING')` when using SYNAPSE-to-MITRE, please try the following command: `python3 -m nltk.downloader SOMETHING`. It should happen only for resources _punkt_ and _wordnet_.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Use cases

Some experiments, or **use cases**, have been carried out over SYNAPSE to stress its functionalities:

- **AI vs SYNAPSE** - **basic interaction**: SYNAPSE is dinamically generating the content of file system and MySQL service, an additional AI interacts with it and navigates through the various file, folders, databases, tables and so on. Everything is automated, with the new **AI replacing user-interaction**.

- **AI vs SYNAPSE** - **attacker interaction**: SYNAPSE is dinamically generating the content of file system and MySQL service, an additional AI tries to attack and corrupt it with _N_ different attack strategies, where _N_ can be customized. Everything is automated, with the new **AI replacing user-interaction**. After the execution of this script, that will stop autonomously when the _N_-th attack ends, SYNAPSE-to-MITRE extension can be run to map the attacks performed by the AI to the MITRE ATT&CK database.

The code implemented to perform the above tests can be found under `use_cases/` folder and can be run by simply typing (e.g. if we want to execute the attacker interaction):
   ```sh
   python3 AI_vs_SYNAPSE_attacker_interaction.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contacts

Enea Gizzarelli - eneagizzarelli2000@gmail.com

LinkedIn - https://linkedin.com/in/eneagizzarelli

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- OTHER PROJECTS -->
## Other projects

**DENDRITE**: [https://github.com/eneagizzarelli/DENDRITE](https://github.com/eneagizzarelli/DENDRITE)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

- [shelLM](https://github.com/stratosphereips/SheLLM)
- [cti-to-mitre-with-nlp](https://github.com/dessertlab/cti-to-mitre-with-nlp)
- [GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb)
- [VirusTotal](https://www.virustotal.com)
- [attack-stix-data/enterprise-attack](https://github.com/mitre-attack/attack-stix-data/tree/master/enterprise-attack)
- [cti/capec](https://github.com/mitre/cti/tree/master/capec)
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

[license-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg?style=for-the-badge
[license-url]: https://github.com/eneagizzarelli/synapse/blob/main/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/eneagizzarelli
