import subprocess
import re


def connectToNetwork(net_SSID, net_PWD):
    bashCommand = "wpa_passphrase" + " " + \
        str(net_SSID) + " " + str(net_PWD) + \
        " | " + "awk \'FNR == 4 {print}\'"

    process = subprocess.run(bashCommand, shell=True, check=True,
                             executable='/bin/bash', stdout=subprocess.PIPE)
    if (process.returncode != 0):
        print("Error while executing BASH command on Connect button")
    else:
        #print("Process returncode:" + str(process.returncode))
        print(str(process.stdout))

        retOut = str(process.stdout)
        psk = re.findall("psk=([a-z|A-Z|0-9]*)", retOut)

        # print(str(psk))
        bashCommand = "echo \"" + \
            "network={\
                \n\tssid=\\\"" + str(net_SSID) + \
            "\\\"\n\tpsk=\\\"" + str(psk.pop()) + \
            "\\\"\n}" \
            "\" > ./provaPSK.txt"
        print(bashCommand)
        # sudo nano / etc/wpa_supplicant/wpa_supplicant.conf
        process = subprocess.run(
            bashCommand, shell=True, check=True, executable='/bin/bash', stdout=subprocess.PIPE)
    if (process.returncode != 0):
        print("Error while executing BASH command on Connect button")
