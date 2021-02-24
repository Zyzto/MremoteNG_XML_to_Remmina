# This repo uses script from [haseebT](https://github.com/haseebT) to decrpyt the passwords from xml file

# Convert Mremote xml to Remmina files

This script is working on **RDP SSH** files only and will ignore any other type

## Usage
Clone localy\
`git clone https://github.com/Zyzto/Mremoteng_ConvertTO_Remmina.git`

Change Directory \
`cd mremote_to_remmina`

Pip Install\
`pip install -r requirements.txt `

Commands 

    mremote_to_remmina.py -i mremote.xml
    mremote_to_remmina.py -i mremote.xml -o "~/Desktop"
    mremote_to_remmina.py -i mremote.xml -o "~/Desktop" -p
    mremote_to_remmina.py -i mremote.xml -p

Options:

    -h --help         Show usage information.
    -i --inputFile    Location of XML File
    -o --outputFolder Folder to Save .Remmina Files
    -p --password     If You Want To Include Password *Must Be On Target Machine*
