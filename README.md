# rosnetSetup

This python script is intended to ease the setup of the ros net.
In particular, it will set the environment variables:

* ROS_IP
* ROS_MASTER_URI

## Requirements

install:
* python
* PyQt4/PyQt5

add in the end of your ~/.bashrc (as for ros setup files):
* source $HOME/.ros/rosnetSetup.bash

## How to run it

either:
* add this file in a ubuntu launcher, and run it
or:
* run it directly as: `python rosnetSetup.py`

## WHAT IT WILL DO

This script will spawn a GUI that will write the env variables in the file "$HOME/.ros/rosnetSetup.bash"
If you source this file in your ~/.bashrc (see on top), your will configure the ros network.

## GUI EXPLAINATION

it is composed of:

* network ip comboxbox
* ros_ip label
* checkbox whether or not you want to define ROS_MASTER_URI
* two edit boxes with: rosmaster_ip & rosmater_port
* apply button, to write configuration in the file "$HOME/.ros/rosnetSetup.bash"
* spawn roscore button, to spawn a terminal which execute a roscore command


the combobox gives you all the available ip of your networks.
when you change it, it will automatically change the ros_ip label
if you want another ip, select "other..." in the combobox and write your desired ip

* in rosmaster_ip editbox, your can write ips as "192.168.1.10", or hostnames as "myComputer", "localhost", etc.
* spawn roscore button will automatically apply the current settings before starting