# SDS-Mininet-WiFi
Software Defined Systems support Extension for Mininet-WiFi Emulator

### What is this repository for? ###

* Quick summary
* Systems Support

This repo holds the outcome of the collaborative work on supporting software defined systems as an extension to the well-known Network SDN Emulator Mininet-wifi.

The list of supported systems are as follows: 

1. VANET-based Software Defined Content Delivery Systems for cooperative mobile Edge Computing
2. [Software Defined Storage for Cooperative Mobile Edge Computing Systems.](https://www.researchgate.net/publication/317421285_Software_Defined_Storage_for_cooperative_Mobile_Edge_Computing_systems) 

Cite @ [SDStorage, J.Albadarneh et.al](http://ieeexplore.ieee.org/document/7939160/)



### How do I get set up? ###

* Summary of set up

    There is no special configurations required to run the system, all you've to do is to clone the repo and cd into the system directory (ex. SDCD) and run the experiment.
* Configuration

    - you've to follow the configuration required by Mininet-WiFi
* Dependencies

    As stated in the description, the proposed systems support works as an extension to mininet wifi. so you should have mininet-wifi installed inside your machine.
    you'll need: 
    - Mininet-wifi (latest version) can be cloned at: [Mininet-WiFi](https://github.com/intrig-unicamp/mininet-wifi)
    - SUMO Urban simulator version >= 0.28.0
    - Distributed Internet Traffic Generator (D-ITG) (latest version) can be found at: [D-ITG](http://traffic.comics.unina.it/software/ITG/download.php)
    - octave (latest version), can be found at: [Octave](http://www.octave.org/)
    - <strong> Both Storage and Content Delivery Experimetns requires `Python2.7` </strong>
    - ~~any future dependencies will be added here~~
* How to run tests  

    In order to run the experiments, follow these instructions:
    
    1) for V-SDCD, navigate to the system directory (SDCD):
    `cd SDCD` then run the experiment via `sudo python2.7 sdcd_experimental.py`.
    - The terminal will guide you to choose your experiment.
    - The Map files are hosted inside Mininet-WiFi. Once you have it installed, Mininet environment variables will be able to locate the files and grab them. 
    They can be found [here](https://github.com/intrig-unicamp/mininet-wifi/blob/master/mininet/sumo/data/new-york.rou.xml)
    
    2) for SDStorage experiment, navigate to system directory (SDStorage):
    `cd SDStorage` then run the experiment via `sudo python2.7 sdstorage_experimental.py`
    - Right after initializing the environemnt, a plot will be shown asking for drawing some roads for the cars. (10 roads - 4 mec nodes - 5 cars). Draw roads as connected points, and then place the mec nodes among those roads. After placing the last MEC node, the cars will be placed on the roads with random positions and speeds. 
    > please note that, for you to be able to run the experiments properly, you need to wait for car1 to be connected to one of the mec node. -a nice tip here is to place the MEC nodes near to each other-.
    
    - Once `car1` is in range of any MEC node, enter the amount of storage units the car is willing to store. Note that Each MEC node is set to have a predefined capacity of 125000 storage units. As specified in the study, auto-scaling storage capacity for MEC nodes will be triggered on-demand.

* If you encountered problems with your wifi-drivers which might stops the nodes from getting connected to the experiment basestations, you need to stop your network manager and use __wpa_supplicant__ to retain your interenet connection which is needed to load the simulation environment map.    

### Having some troubles!! ###
Don't hesitiate and go ahead submit your PRs

### Who do I talk to? ###

* Repo owner or admin (Jafar Albadarneh)

Collaborators
---
- __Jafar albadarneh__, _Email_: jafar92.jaa@gmail.com, Jordan University of Science and Technology
- __Yaser Jararweh__, _Email_:yaser.amd@gmail.com,  Carnegie Mellon University
- __Mahmoud Alayyoub__, _Email_:maalshbool@just.edu.jo, Jordan University of Science and Technology
- __Mohammad Alsmadi__, _Email_:maalsmadi9@just.edu.jo, Jordan University of Science and Technology
- __Ramon Fontes__, _Email_:ramonrf@dca.fee.unicamp.br, University of Campinas, Campinas, Brazil
- __Christian Rothenberg__, _Email_:chesteve@dca.fee.unicamp.br ,University of Campinas, Campinas, Brazil
