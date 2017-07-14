# SDS-Mininet-WiFi
Software Defined Systems support Extension for Mininet-WiFi Emulator

### What is this repository for? ###

* Quick summary
* Systems Support

This repo holds the outcome of the collaborative work on supporting software defined systems as an extension to the well-known Network SDN Emulator Mininet-wifi.

The list of supported systems are as follows: 

1. VANET-based Software Defined Content Delivery Systems for cooperative mobile Edge Computing



### How do I get set up? ###

* Summary of set up

    There is no special configurations required to run the system, all you've to do is to clone the repo and cd into the system directory (ex. SDCD) and run the experiment.
* Configuration

    you've to follow the configuration required by Mininet-WiFi
* Dependencies

    As stated in the description, the proposed systems support works as an extension to mininet wifi. so you should have mininet-wifi installed inside your machine.
    you'll need: 
    - Mininet-wifi (latest version) can be cloned at: [Mininet-WiFi](https://github.com/intrig-unicamp/mininet-wifi)
    - SUMO Urban simulator version >= 0.28.0
    - ~~any future dependencies will be added here~~
* How to run tests  

    In order to run the experiment for V-SDCD, navigate to the system directory:
    `cd SDCD` then run the experiment `sudo python sdcd_experimental.py`.
    The terminal will guide you to choose your experiment.
* Known Issues

    - If you encountered problems with your wifi-drivers which might stops the nodes from getting connected to the experiment basestations, you need to stop your network manager and use __wpa_supplicant__ to retain your interenet connection which is needed to load the simulation environment map.    

### Contribution guidelines ###


### Who do I talk to? ###

* Repo owner or admin (Jafar Albadarneh)

Collaborators
---
- __Jafar albadarneh__, _Email_: jafar92.jaa@gmail.com, Jordan University of Science and Technology
- __Ramon Fontes__, _Email_:ramonrf@dca.fee.unicamp.br, University of Campinas, Campinas, Brazil
- __Yaser Jararweh__, _Email_:yaser.amd@gmail.com,  Carnegie Mellon University
- __Mahmoud Alayyoub__, _Email_:maalshbool@just.edu.jo, Jordan University of Science and Technology
- __Mohammad Alsmadi__, _Email_:maalsmadi9@just.edu.jo, Jordan University of Science and Technology
- __Christian Rothenberg__, _Email_:chesteve@dca.fee.unicamp.br ,University of Campinas, Campinas, Brazil
