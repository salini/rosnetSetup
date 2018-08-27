#!/usr/bin/env python

""" ROS NET SETUP
This python script is intended to ease the setup of the ros net.
In particular, it will set the environment variables:

* ROS_IP
* ROS_MASTER_URI

REQUIREMENTS
============

install:
* python
* PyQt4/PyQt5

add in the end of your ~/.bashrc (as for ros setup files):
* source $HOME/.ros/rosnetSetup.bash

HOW TO RUN IT
=============

either:
* add this file in a ubuntu launcher, and run it
or:
* run it directly as: `python rosnetSetup.py`

WHAT IT WILL DO
===============

This script will spawn a GUI that will write the env variables in the file "$HOME/.ros/rosnetSetup.bash"
If you source this file in your ~/.bashrc (see on top), your will configure the ros network.

GUI EXPLAINATION
================

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

in rosmaster_ip editbox, your can write ips as "192.168.1.10", or hostnames as "myComputer", "localhost", etc.

* spawn roscore button will automatically apply the current settings before starting


"""


import sys, os
from netifaces import interfaces, ifaddresses, AF_INET

try:
    from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QLabel, QPushButton, QMessageBox, QApplication
    from PyQt5.QtGui import QIntValidator
except ImportError:
    from PyQt4.QtGui import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QIntValidator, QLabel, QPushButton, QMessageBox, QApplication



try:
    os.mkdir(os.path.join(os.path.expanduser('~'), ".ros"))
except:
    pass

ROSNETFILENAME=os.path.join(os.path.expanduser('~'), ".ros","rosnetSetup.bash")


def ip4_addresses():
    ip_list = {}
    for interface in interfaces():
        if AF_INET in ifaddresses(interface):
            links = ifaddresses(interface)[AF_INET]
            if len(links) == 1:
                ip_list[interface] = links[0]['addr']
            else:
                for idx, link in enumerate(links):
                    ip_list[interface+"."+str(idx)] = link['addr']
    return ip_list



def getRosnetConfigData():
    if os.path.exists(ROSNETFILENAME):
        if os.path.isfile(ROSNETFILENAME):
            pass
        else:
            raise RuntimeError()
    else:
        data = {"ROS_IP":"127.0.0.1", "ROS_MASTER_IS_SET":True, "ROS_MASTER_IP":"127.0.0.1", "ROS_MASTER_PORT":11311}
        setRosnetConfigData(data)

    data = {}
    with open(ROSNETFILENAME, "r") as f:
        for l in f.readlines():
            if "ROS_IP" in l:
                data["ROS_IP"] = l.partition("ROS_IP")[2].partition("=")[2].strip()
            if "ROS_MASTER_URI" in l:
                ll = l.strip()
                if ll[0] == "#":
                    data["ROS_MASTER_IS_SET"] = False
                else:
                    data["ROS_MASTER_IS_SET"] = True
                rmuri = ll.partition("ROS_MASTER_URI")[2].partition("=")[2].strip()
                data["ROS_MASTER_URI"] = rmuri
                rmuri = rmuri.partition("http://")[2].strip()
                ip, sep, port = rmuri.partition(":")
                data["ROS_MASTER_IP"] = ip
                data["ROS_MASTER_PORT"] = port

    return data



def setRosnetConfigData(data):
    rosIP, masterIsSet, masterIP, masterPort = [data[n] for n in ["ROS_IP", "ROS_MASTER_IS_SET", "ROS_MASTER_IP", "ROS_MASTER_PORT"]]
    mset = "" if masterIsSet else "#"
    towrite="""
export ROS_IP={0}
{1}export ROS_MASTER_URI=http://{2}:{3}
""".format(rosIP, mset, masterIP, masterPort)
    with open(ROSNETFILENAME, "w") as f:
      f.write(towrite)




class RosIPSetupWidget(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, "ros ip", parent)

        l = QVBoxLayout()
        self.setLayout(l)

        self.ip = QLineEdit("")

        self.comboip = QComboBox()
        for k, v in ip4_addresses().items():
            self.comboip.addItem(k+': '+v, v)
        self.comboip.addItem("other...", "")
        self.comboip.currentIndexChanged.connect(self.comboip_currentIndexChanged)

        l.addWidget(self.comboip)
        l.addWidget(self.ip)

    def comboipChangeIndex(self, index):
        self.comboip.setCurrentIndex(index)
        self.comboip_currentIndexChanged(index)

    def comboip_currentIndexChanged(self, index):
        if index == self.comboip.count() - 1:
            self.ip.setEnabled(True)
        else:
            self.ip.setEnabled(False)
            value = self.comboip.itemData(index)
            if not isinstance(value, basestring):
                value = value.toString() #then it should be a QVariant
            self.ip.setText(value)


    def setData(self, data):
        ip = data["ROS_IP"]
        self.ip.setText("{0}".format(ip))
        idx = self.comboip.findData(ip)
        if idx < 0:
            self.comboip.setItemData(self.comboip.count()-1, ip)
            self.comboipChangeIndex(self.comboip.count()-1)
        else:
            self.comboipChangeIndex(idx)



    def getData(self, data):
        data["ROS_IP"] = str(self.ip.text())




class RosMasterSetupWidget(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, "ros master", parent)
        self.setCheckable(True)

        l = QHBoxLayout()
        self.setLayout(l)

        self.uriip = QLineEdit()
        self.uriport = QLineEdit()
        self.uriport.setValidator(QIntValidator())

        l.addWidget(QLabel("http://"))
        l.addWidget(self.uriip)
        l.addWidget(QLabel(":"))
        l.addWidget(self.uriport)

    def setData(self, data):
        self.setChecked(data["ROS_MASTER_IS_SET"])
        self.uriip.setText(data["ROS_MASTER_IP"])
        self.uriport.setText(data["ROS_MASTER_PORT"])

    def getData(self, data):
        data["ROS_MASTER_IS_SET"] = bool(self.isChecked())
        data["ROS_MASTER_IP"] = str(self.uriip.text())
        data["ROS_MASTER_PORT"] = int(self.uriport.text())


class RoscoreConfigureWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        l = QVBoxLayout()
        self.setLayout(l)

        self.rosip = RosIPSetupWidget()
        self.rosmaster = RosMasterSetupWidget()
        self.applyBtn = QPushButton("Apply")
        self.applyBtn.clicked.connect(self.applyBtn_clicked)
        self.spwanRoscoreBtn = QPushButton("Spawn roscore")
        self.spwanRoscoreBtn.clicked.connect(self.spwanRoscoreBtn_clicked)


        l.addWidget(self.rosip)
        l.addWidget(self.rosmaster)
        l.addWidget(self.applyBtn)
        l.addWidget(self.spwanRoscoreBtn)

        data = getRosnetConfigData()
        self.rosip.setData(data)
        self.rosmaster.setData(data)

    def getData(self):
        data = {}
        self.rosip.getData(data)
        self.rosmaster.getData(data)
        #print(data)
        return data

    def applyBtn_clicked(self):
        data = self.getData()
        setRosnetConfigData(data)


    def spwanRoscoreBtn_clicked(self):
        self.applyBtn_clicked()
        data = self.getData()
        if data["ROS_MASTER_IS_SET"] and data["ROS_MASTER_IP"] not in ["localhost", "127.0.0.1", data["ROS_IP"]]:
            rep = QMessageBox.warning(self, "roscore master uri", "ROS_MASTER_URI is not set for this machine. Continue?", QMessageBox.Ok, QMessageBox.Cancel)
            if rep == QMessageBox.Ok:
                pass
            elif rep == QMessageBox.Cancel:
                return
            else:
                return
        os.system('gnome-terminal -x bash -ic "roscore; exec bash" &')



if __name__ == "__main__":

    app = QApplication(sys.argv)

    w = RoscoreConfigureWidget()
    w.show()

    app.exec_()


