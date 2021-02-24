#!/usr/bin/python3

"""
pip3 install pycryptodome
"""

import xml.etree.ElementTree as ET
import argparse, sys
import os
import configparser
import getopt
from Crypto.Cipher import DES3
import subprocess
from subprocess import Popen
import base64
from os.path import expanduser
import platform

home = expanduser("~")
dublicate = []
global password_value
global password
password = False
required = False
if platform.system() == "Windows":
    outputfile = "Remmina"
help_text = """
MremoteNG to Remmina Config Converter.

Usage:
mremote_to_remmina.py -i mremote.xml
mremote_to_remmina.py -i mremote.xml -o "~/Desktop"
mremote_to_remmina.py -i mremote.xml -o "~/Desktop" -p
mremote_to_remmina.py -i mremote.xml -p

Options:
-h --help         Show this screen.
-i --inputFile    Location of XML File
-o --outputFolder Folder to Save .Remmina Files (DEFUALT is ~/.local/share/remmina)
-p --password     If You Want To Include Password *Must Be On Target Machine*
"""

try:
    opts, args = getopt.getopt(
        sys.argv[1:], "hi:o:p", ["help", "ifile=", "ofolder=", "password"]
    )
except getopt.GetoptError as err:
    # print help information and exit:
    print(
        f"""*******************************************
    {err}
*******************************************{help_text}"""
    )  # will print something like "option -a not recognized"
    sys.exit(2)

if opts == []:
    print(help_text)
    sys.exit(2)

for opt, arg in opts:
    if opt == "":
        print(help_text)
        sys.exit()
    if opt == "-h":
        print(help_text)
        sys.exit()
    if opt in ("-i", "--inputFile"):
        inputfile = arg
        required = True
    if opt in ("-o", "--ofolder"):
        outputfile = arg
    if opt in ("-p", "--password"):
        try:
            password = True
            config = configparser.ConfigParser()
            config.read(f"{home}/.config/remmina/remmina.pref")
            password_value = config["remmina_pref"]["secret"]
            try:
                outputfile
            except:
                outputfile = f"{home}/.local/share/remmina/"

            # print(password_value)
        except:
            print(
                """Remmina isn't installed please install before running the script:

            sudo apt install Remmina
            sudo dnf install Remmina
            pacman -Sy Remmina
            zypper in Remmina
            """
            )
            sys.exit(2)

    if required == False:
        print("you must enter -i <inputFile>")
        sys.exit()
path = os.getcwd()

tree = ET.parse(f"{inputfile}")
root = tree.getroot()

# print(root.tag)


def encryptRemminaPass(secret_password, plain):
    plain = plain.encode("utf-8")
    secret = base64.b64decode(secret_password)
    key = secret[:24]
    iv = secret[24:]
    plain = plain + b"\0" * (8 - len(plain) % 8)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    result = cipher.encrypt(plain)
    result = base64.b64encode(result)
    result = result.decode("utf-8")
    return result


def create_connection(item, parents):
    global dublicate

    for this_name in dublicate:
        if this_name != item.attrib["Name"]:
            continue
        else:
            print("DUBLICATE: ", item.attrib["Name"])
            return
    config = configparser.ConfigParser()
    config["remmina"] = {}
    conf = config["remmina"]
    if (
        (item.attrib["Protocol"] == "SSH")
        | (item.attrib["Protocol"] == "SSH1")
        | (item.attrib["Protocol"] == "SSH2")
    ):
        conf["protocol"] = "SSH"
        # Theme
        conf["ssh_color_scheme"] = "3"
    elif item.attrib["Protocol"] == "RDP":
        conf["protocol"] = "RDP"
    elif item.attrib["Protocol"] == "HTTP":
        conf["protocol"] = "HTTP"
    else:
        return

    conf["name"] = item.attrib["Name"]
    conf["server"] = item.attrib["Hostname"]
    conf["group"] = parents

    parents = parents.replace("/", "").replace("\\", "").replace("\t", "")
    name = item.attrib["Name"].replace("/", "").replace("\\", "").replace("\t", "")

    if password == True:
        if item.attrib["Password"] != "":
            # print(pp)
            p = subprocess.Popen(
                ["python3", "decrypt.py", "-s" f"{item.attrib['Password']}"],
                stdout=subprocess.PIPE,
            )
            out = p.stdout.read()
            out = out.split()
            # print(out)
            out = out[1]
            out = encryptRemminaPass(password_value, out.decode("utf-8"))
            print(out)
        else:
            out = b"nothing"

        try:
            if conf["protocol"] == "SSH":
                conf["ssh_username"] = item.attrib["Username"]
                conf["ssh_password"] = out
            elif conf["protocol"] == "RDP":
                if item.attrib["Username"] == "ldapname if you want":
                    # Change any RDP Password that is have ldap username
                    #? Change this if You want other wise keep same
                    conf["username"] = ""
                    conf["password"] = encryptRemminaPass(password_value, " ")
                else:
                    conf["username"] = item.attrib["Username"]
                    conf["password"] = out
            print(conf["name"], " ***SUCCESS***")
        except:
            print(conf["name"], " ***ERROR: No Password***")
            print(conf["protocol"])
            print("Password: ", item.attrib["Password"])
    # print(dublicate)
    for this_name in dublicate:
        if this_name != item.attrib["Name"]:
            with open(f"{outputfile}{parents} $ {name}.remmina", "w") as configfile:
                config.write(configfile)
                configfile.close
        else:
            print("DUBLICATE: ", f"{outputfile}{parents} $ {name}.remmina")
    dublicate.append(item.attrib["Name"])

    # file = open(f"{outputfile}/{parents} $ {name}.remmina", "w+")
    # file.write(config)
    # file.close


def check_connection(items, parents):
    for item in items:
        if item.attrib["Type"] == "Connection":
            if len(parents) == 0:
                create_connection(item, f"{items.attrib['Name']}")
            else:
                create_connection(item, parents + f" #{items.attrib['Name']}")
        else:
            if len(parents) == 0:
                check_connection(item, parents + f"{items.attrib['Name']}")
            else:
                check_connection(item, parents + f" #{items.attrib['Name']}")


for item in root:
    check_connection(item, "")
