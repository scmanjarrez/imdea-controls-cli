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

echo -e -n "${HEADER}\t[+] Updating apt... please type your pass..."
sudo apt-get update -qq

if [ $? -eq 0 ]; then
    echo -e "${OK}OK${ENDC}"
else
    echo -e "${ERROR}ERROR${ENDC}"
fi

# TODO: check if python is python 2.7
echo -e -n "${HEADER}\t[+] Checking if python is installed..."
dpkg -s python >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo -e -n "${ERROR}FAIL\n\t${HEADER}\t[-] Installing python..."

    sudo apt-get install -y -qq python

    if [ $? -eq 0 ]; then
	    echo -e "${OK}OK${ENDC}"
    else
        echo -e "${ERROR}ERROR${ENDC}"
    fi
else
    echo -e "${OK}OK${ENDC}"
fi

echo -e -n "${HEADER}\t[+] Checking if python-pip is installed..."
dpkg -s python-pip >/dev/null 2>&1

if [ $? -ne 0 ]; then
    echo -e -n "${ERROR}FAIL\n\t${HEADER}\t[-] Installing python-pip..."

    sudo apt-get install -y -qq python-pip

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
    pip install --user requests >/dev/null 2>&1

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

alias_def="icp"
alias_long="imdea-control"
alias_final="" # to set with the final alias added in ~/.aliases
echo -e -n "${HEADER}\t[+] Checking if alias $alias_def already exists in ~/.aliases file...${ENDC}"
grep -Fx "alias $alias_def" ~/.aliases

if [ $? -eq 0 ]; then
    echo -e "${ERROR}FAIL${ENDC}"
    echo -e "${HEADER}\t[-] Setting $alias_long as alias...${OK}OK${ENDC}"
    echo "alias $alias_long='${PWD}/control.py'" >> ~/.aliases
    alias_final=$alias_long
    
else
    echo -e "${OK}OK${ENDC}"
    echo -e "${HEADER}\t[-] Setting $alias_def as alias...${OK}OK${ENDC}"
    echo "alias $alias_def='${PWD}/control.py'" >> ~/.aliases
    alias_final=$alias_def
fi

echo -e -n "${HEADER}\t[+] Checking if alias already exists in .bashrc...${ENDC}"
grep -Fx "source ~/.aliases" ~/.bashrc

if [ $? -eq 0 ]; then
    echo -e "${OK}OK${ENDC}"
else
    echo -e "${ERROR}FAIL${ENDC}"
    echo -e "${HEADER}\t[-] Adding alias to .bashrc...${OK}OK${ENDC}"
    echo "source ~/.aliases" >> ~/.bashrc    
fi


echo -e -n "${HEADER}\t[+] Checking if alias already exists in .bashrc...${ENDC}"
grep -Fx "source ~/.aliases" ~/.zshrc

if [ $? -eq 0 ]; then
    echo -e "${OK}OK${ENDC}"
else
    echo -e "${ERROR}FAIL${ENDC}"
    echo -e "${HEADER}\t[-] Adding alias to .zshrc...${OK}OK${ENDC}"
    echo "source ~/.aliases" >> ~/.zshrc
fi

echo -e "${HEADER}"
echo -e -n "Installation finished, run your script with \"$alias_final\" command"
echo -e "${ENDC}"
echo ""


echo -e "${HEADER}[++] Running './control.py -h' script...${ENDC}"
echo ""
python ${PWD}/control.py -h
