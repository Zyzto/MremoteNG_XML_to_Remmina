# Convert Mremote xml to Remmina files

This script is working on **RDP SSH** files only and will ignore any other type

## Usage
Clone localy\
`git clone http://git/ziad.alshanbari/mremote_to_remmina.git`

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