import subprocess
import re

import os
from PyQt5 import QtCore, QtGui, QtWidgets

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


def connectToNetwork(net_SSID, net_PWD):
    # bashCommand = "wpa_passphrase" + " \"" + \
    #     str(net_SSID) + "\" \"" + str(net_PWD) + \
    #     "\" | " + "awk \'FNR == 4 {print}\'"

    # process = subprocess.run(bashCommand, shell=True, check=True,
    #                          executable='/bin/bash', stdout=subprocess.PIPE)
    # if (process.returncode != 0):
    #     print("Error while executing BASH command on Connect button")
    # else:
    #     # print("Process returncode:" + str(process.returncode))
    #     # print(str(process.stdout))

    #     retOut = str(process.stdout)
    #     psk = re.findall("psk=([a-z|A-Z|0-9]*)", retOut)

    # print(str(psk))

    # TODO: Le credenziali non vengono salvate nel file /etc/wpa_supplicant/wpa_supplicant.conf
    # e non vengono quindi salvate per il prossimo riavvio.
    # Appendere le credenziali inserite nel suddetto file e lanciare subito la connessione
    # 2 modi: chiudere e riaprire la connessione con killall e sudo wpa_supplicant -B -iwlan0 -cCONFIG_FILE -Dnl80211,wext
    # oppure provare con i comandi iw[qualcosa].

    # FIXME: Se le credenziali vengono confermate errate (password o SSID) la connessione non parte ma l'interfaccia mostra "connesso!". attualmente, per reinserire delle credenziali valide l'unico modo è riavviare. Correggere almeno l'interfaccia

    # bashCommand = "sudo killall wpa_supplicant > loggino ; sleep 2 && echo \"ctrl_interface=/run/wpa_supplicant\nupdate_config=1\ncountry=IT\n\" > CONFIG_FILE && wpa_passphrase \"" + \
    #     str(net_SSID) + "\" \"" + str(net_PWD) + \
    #     "\" >> CONFIG_FILE && sudo wpa_supplicant -B -iwlan0 -cCONFIG_FILE -Dnl80211,wext >> loggino && sleep 2"

    # bashCommand = "sudo echo \"ctrl_interface=/run/wpa_supplicant\nupdate_config=1\ncountry=IT\n\" > /etc/wpa_supplicant/wpa_supplicant.conf && wpa_passphrase " + \
    #     str(net_SSID) + " " + str(net_PWD) + \
    #     " >> /etc/wpa_supplicant/wpa_supplicant.conf && sudo killall wpa_supplicant && sudo wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf -Dnl80211,wext >> loggino"

    bashCommand = "sudo echo \"ctrl_interface=/run/wpa_supplicant\nupdate_config=1\ncountry=IT\n\" > /etc/wpa_supplicant/wpa_supplicant.conf && echo \"Prima parte conf scritta\" > loggino && sudo su && echo \"Sudo su fatto\" >> loggino && sudo wpa_passphrase \"" + \
        str(net_SSID) + "\" \"" + str(net_PWD) + \
        "\" >> /etc/wpa_supplicant/wpa_supplicant.conf && echo \"Passphrase e scrittura fatta\" >> loggino && sudo wpa_cli terminate >> loggino && echo \"Wpa_cli terminate fatto\" >> loggino && sleep 2 && sudo wpa_supplicant -B -Dnl80211,wext -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf >> loggino && echo \"Wpa_supplicant ricaricato\" >> loggino && sleep 2 && sudo wpa_cli reassociate >> loggino && echo \"Reassociate fatto, finito\" >> loggino"

    # Ritorna l'SSID a cui sei attualmente collegato
    # bashCheckConnectivity = "echo \"Check SSID in corso...\" >> loggino && sleep 10 && iwgetid -r"

    # subprocess.Popen(bashCommand, shell=True, executable = "/bin/bash", stdout = subprocess.PIPE)

    checkProcess = subprocess.run(bashCommand, shell=True, check=True,
                                  executable="/bin/bash", stdout=subprocess.PIPE)

    if (checkProcess.stdout == str(net_SSID)):
        # Tutto ok, connesso
        print("Connesso!")
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setInformativeText(
            "Connesso alla rete!")
        msg.setWindowTitle("Info")
        msg.exec_()
    else:
        # Errore, non connesso
        print("ERRORE! Non connesso!")
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setInformativeText(
            "Errore nella connesione alla rete!")
        msg.setWindowTitle("Error")
        msg.exec_()
    print("")
