#!/bin/bash

user_check() {
	if [ $(id -u) -ne 0 ]; then
		printf "Script must be run as root. Try 'sudo ./install.sh'\n"
		exit 1
	fi
}

success() {
	echo -e "$(tput setaf 2)$1$(tput sgr0)"
}

inform() {
	echo -e "$(tput setaf 6)$1$(tput sgr0)"
}

warning() {
	echo -e "$(tput setaf 1)$1$(tput sgr0)"
}

user_check

inform "Installing systemd service...\n"
cp grow-recorder.service /etc/systemd/system/
systemctl reenable grow-recorder.service
systemctl start grow-recorder.service

inform "\nSuccessfully installed grow-recorder as a systemd service.\n"