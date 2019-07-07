import subprocess
import re
import socket
import time

import os
from PyQt5 import QtCore, QtGui, QtWidgets

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

net_SSID = ""
net_PWD = ""
isConnected = False


def connectToNetwork():

    if (checkSSID(net_SSID) == 0):  # Ok, il SSID è corretto


        # Vecchio comando, rischioso
        
        # bashCommand = "sudo echo \"ctrl_interface=/run/wpa_supplicant\nupdate_config=1\ncountry=IT\n\" > /etc/wpa_supplicant/wpa_supplicant.conf && echo \"Prima parte conf scritta\" > loggino && sudo su && echo \"Sudo su fatto\" >> loggino && sudo wpa_passphrase \"" + \
        #     str(net_SSID) + "\" \"" + str(net_PWD) + \
        #     "\" >> /etc/wpa_supplicant/wpa_supplicant.conf && echo \"Passphrase e scrittura fatta\" >> loggino && sudo wpa_cli terminate >> loggino && echo \"Wpa_cli terminate fatto\" >> loggino && sleep 2 && sudo wpa_supplicant -B -Dnl80211,wext -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf >> loggino && echo \"Wpa_supplicant ricaricato\" >> loggino && sleep 2 && sudo wpa_cli reassociate >> loggino && echo \"Reassociate fatto, finito\" >> loggino"

        # Per fare il seguente comando eseguire sul rasp (non c'è bisogno di sudo su):
        # sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf
        # runnare la gui lanciando il comando sudo python3 ..../gui.py &
        bashCommand = "sudo echo \"ctrl_interface=/run/wpa_supplicant\nupdate_config=1\ncountry=IT\n\" > /etc/wpa_supplicant/wpa_supplicant.conf && echo \"Prima parte conf scritta\" > loggino && sudo wpa_passphrase \"" + \
            str(net_SSID) + "\" \"" + str(net_PWD) + \
            "\" >> /etc/wpa_supplicant/wpa_supplicant.conf && echo \"Passphrase e scrittura fatta\" >> loggino && sudo wpa_cli terminate >> loggino && echo \"Wpa_cli terminate fatto\" >> loggino && sleep 2 && sudo wpa_supplicant -B -Dnl80211,wext -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf >> loggino && echo \"Wpa_supplicant ricaricato\" >> loggino && sleep 2 && sudo wpa_cli reassociate >> loggino && echo \"Reassociate fatto, finito\" >> loggino && exit"

        print("Tentativo di connessione in corso, eseguo i comandi Bash")

        try:
            connectionProcess = subprocess.run(bashCommand, shell=True, check=True,
                                               executable="/bin/bash", stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("Eccezione durante il tentativo di connessione, ritorno 1")
            return 1

        print("Ora faccio il check rete")

        # Vecchia roba, il secondo una volta funzionava

        # bashCheckConnection = "echo \"Check rete\" >> loggino && sleep 5 && echo \"ho dormito 5 secs\" >> loggino && iw dev wlan0 link | grep SSID && echo \"SSID letto, finito\" >> loggino"

        # bashCheckConnection = "echo \"Check rete\" >> loggino && sleep 10 && echo \"ho dormito 5 secs\" >> loggino && iwconfig wlan0 | grep ESSID && echo \"SSID letto, finito\" >> loggino"

        # bashCheckConnection = "echo \"Check rete\" >> loggino && sleep 10 && echo \"ho dormito 5 secs\" >> loggino && iw dev wlan0 link | grep SSID && echo \"SSID letto, finito\" >> loggino"

        time.sleep(10)

        if (is_connected() == True):
            print("Connesso!")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setInformativeText(
                "Connesso alla rete!")
            msg.setWindowTitle("Info")
            msg.exec_()
            return 0
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setInformativeText(
                "Errore nella connesione alla rete!")
            msg.setWindowTitle("Error")
            msg.exec_()
            return -1

    # vecchia roba, funzionava con il secondo comando

    #     checkConnectionProcess = subprocess.run(bashCheckConnection, shell=True, check=True,
    #                                              executable="/bin/bash", stdout=subprocess.PIPE)

    #     returnedString = str(checkConnectionProcess.stdout)
    #     print(returnedString)
    #     # pattern = "ESSID:\"([\\x20-\\x5B \\x5D-\\x7F]+)\""
    #     pattern = "SSID: ([\\x20-\\x5B \\x5D-\\x7F]+)"

    #     matchList = re.findall(pattern, returnedString)
    #     print(matchList)
    #     print("SSID trovato: " + net_SSID)

    #     if len(matchList) != 0:
    #         if (net_SSID in matchList):
    #             # SSID esistente
    #             print("SSID esistente")
    #             print("Connesso!")
    #             msg = QtWidgets.QMessageBox()
    #             msg.setIcon(QtWidgets.QMessageBox.Information)
    #             msg.setInformativeText(
    #                 "Connesso alla rete!")
    #             msg.setWindowTitle("Info")
    #             msg.exec_()
    #             return 0
    #         else:  # SSID NON esistente
    #             print("SSID NON esistente")
    #             print("ERRORE! Non connesso!")
    #             msg = QtWidgets.QMessageBox()
    #             msg.setIcon(QtWidgets.QMessageBox.Critical)
    #             msg.setInformativeText(
    #                 "Errore nella connesione alla rete!")
    #             msg.setWindowTitle("Error")
    #             msg.exec_()
    #             return -1
    #     else:  # SSID NON esistente
    #         print("SSID NON esistente")
    #         return -1

    else:  # Not OK, ĺSSID era errato
        print("ERRORE! Rete non trovata...")
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setInformativeText(
            "SSID non trovato, sistema non connesso alla rete")
        msg.setWindowTitle("Error")
        msg.exec_()
        return -1


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def checkSSID(net_SSID):

    print("Faccio il pre-check del SSID")

    bashCommand = "sudo iwlist wlan0 scan | grep \"" + str(net_SSID) + "\""

    try:
        process = subprocess.run(bashCommand, shell=True, check=True,
                                 executable="/bin/bash", stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return -1

    returnedString = str(process.stdout)
    print("Stringa ritornata da iwlist wlan0 scan: " + returnedString)
    pattern = "ESSID:\"([\x00 -\x7F]+)\""
    matchList = re.findall(pattern, returnedString)
    print(matchList)
    print("SSID trovato: " + net_SSID)

    if len(matchList) != 0:
        if (net_SSID in matchList):
            # SSID esistente
            print("SSID esistente")
            return 0
        else:  # SSID NON esistente
            print("SSID NON esistente")
            return -1
    else:  # SSID NON esistente
        print("SSID NON esistente")
        return -1


def checkNetworkConnection():

    bashCheckConnection = "echo \"PreCheck rete\" >> loggino && iwconfig wlan0 | grep ESSID && echo \"PreCheck finito\" >> loggino && exit"

    checkConnectionProcess = subprocess.run(bashCheckConnection, shell=True, check=True,
                                            executable="/bin/bash", stdout=subprocess.PIPE)

    returnedString = str(checkConnectionProcess.stdout)
    print(returnedString)

    pattern = "ESSID:\"([\\x20-\\x5B \\x5D-\\x7F]+)\""
    matchList = re.findall(pattern, returnedString)
    print(matchList)

    if len(matchList) != 0.:
        # SSID esistente
        print("SSID esistente")
        print("Connesso!")
        net_SSID = matchList.pop()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setInformativeText(
            "Connesso alla rete \"" + str(net_SSID) + "\"!")
        msg.setWindowTitle("Info")
        msg.exec_()
        return 0
    else:
        # SSID NON esistente
        print("SSID NON esistente")
        print("ERRORE! Non connesso!")
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setInformativeText(
            "Il sistema non è connesso alla rete")
        msg.setWindowTitle("Error")
        msg.exec_()
        return -1
