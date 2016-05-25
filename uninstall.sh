#!/bin/bash

echo "UNINSTALLING THE TOOL..."
echo
echo "planning to do the following:"
echo "============================================="
cat uninstall_helper.sh
echo "============================================="
echo
read -r -p "Really want it? [y/N] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]; then
	echo "OK.";
	source uninstall_helper.sh
	rm uninstall_helper.sh
else
	echo "CANCELLED."
	exit 0
fi
