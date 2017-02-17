#!/bin/bash

HEADER='\033[1;34m'
ERROR='\033[1;31m'
OK='\033[1;32m'
ENDC='\033[0m'

echo -e -n "${HEADER}"
echo "#######################################################"
echo "##     Welcome to IMDEA Controls Python installer    ##"
echo "#######################################################"

echo ""

echo -n "[++] Checking for dependencies..."
echo -e "${ENDC}"

echo -e -n "${HEADER}\t[+] Checking if python-pip is installed..."
dpkg -s python-pip >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo -e -n "${ERROR}FAIL\n\t${HEADER}Installing python-pip..."

    sudo apt-get install -y python-pip >/dev/null 2>&1
    
    if [ $? -eq 0 ]; then
	echo -e "${OK}OK${ENDC}"
    else
	echo -e "${ERROR}ERROR${ENDC}"
    fi
else
    echo -e "${OK}OK${ENDC}"
fi

echo -e -n "${HEADER}\t[+] Checking if python module requests is installed..."
python -c "import requests" >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo -e -n "${ERROR}FAIL\n\t${HEADER}\t[-] Installing requests module..."
    pip install requests >/dev/null 2>&1

    if [ $? -eq 0 ]; then
	echo -e "${OK}OK${ENDC}"
    else
	echo -e "${ERROR}ERROR${ENDC}"
    fi
else
    echo -e "${OK}OK${ENDC}"
fi

echo ""
echo -e -n "${HEADER}[++] Setting alias for control.py...${ENDC}"

echo "alias icp='${PWD}/control.py'" >> ~/.aliases

if [ $? -eq 0 ]; then
    echo -e "${OK}OK${ENDC}"
else
    echo -e "${ERROR}ERROR${ENDC}"
fi


echo -e -n "${HEADER}\t[+] Adding alias to .bashrc and .zshrc...${ENDC}"

echo "source ~/.aliases" >> ~/.bashrc && echo "source ~/.aliases" >> ~/.zshrc

if [ $? -eq 0 ]; then
    echo -e "${OK}OK${ENDC}"
else
    echo -e "${ERROR}ERROR${ENDC}"
fi

echo -e "${HEADER}"
echo -e -n "Installation finished, run your script with \"icp\" command"
echo -e "${ENDC}"
echo ""

echo -e "${HEADER}[++] Running help of control.py script...${ENDC}"
echo ""
python ${PWD}/control.py -h
