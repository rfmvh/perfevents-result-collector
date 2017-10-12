#!/bin/bash

# configuration
export TOOL_PREFIX=${TOOL_PREFIX:-rcl}
export TOOL_NAME="results-collector"
export INSTALL_PATH=${INSTALL_PATH:-/usr/local/bin}
export SHARE_PATH="/usr/share"

assert_error()
{
	if [ $1 -eq 0 ]; then
		echo "$2 ... OK"
	else
		echo "ERROR: $2 $3"
		exit 1
	fi
}

assert_warn()
{
	if [ $1 -eq 0 ]; then
		echo "$2 ... ok"
	else
		echo "WARNING: $2 $3"
	fi
}

# check for Python PostgreSQL interface
python -c 'import psycopg2' 2> /dev/null
assert_error $? "python-psycopg2" "is a hard requirement"

# check if the installation path exists
test -d $INSTALL_PATH
assert_error $? "installation path existence" "(installation path must exist)"

# check if the installation path is in $PATH
echo $PATH | grep -q $INSTALL_PATH:
assert_warn $? "install path in PATH" "(installation path should be in PATH)"

# check if the installation path is writeable
test -w $INSTALL_PATH
assert_error $? "installation path write rights" "(you do not have enough rights to write to the installation path)"

# check if the prefix can cause a collision
! ls $INSTALL_PATH/$TOOL_PREFIX-* &>/dev/null
assert_warn $? "name prefix collision" "(there are some tools that have $TOOL_PREFIX- prefix in $INSTALL_PATH, it might cause a collision)"

# check if the share path exists
test -d $SHARE_PATH
assert_error $? "share path existence" "(share path must exist)"

# SHARE_PATH must NOT be ""
! test -z "$SHARE_PATH"
assert_error $? "share path not null" "(share path MUST NOT be empty, otherwise you would not like the uninstallation script)"

# TOOL_NAME must NOT be ""
! test -z "$TOOL_NAME"
assert_error $? "tool name not null" "(tool name MUST NOT be empty, otherwise you would not like the uninstallation script)"

# check if the share path is writeable
test -w $SHARE_PATH
assert_error $? "share path write rights" "(you do not have enough rights to write to the share path)"

# check the uninstallation script
test -e uninstall.sh
assert_error $? "uninstallation script" "(I need it in order to grant a clean uninstallation)"

# do the installation
mkdir $SHARE_PATH/$TOOL_NAME 2> /dev/null
assert_error $? "share path dir creation" "($SHARE_PATH/$TOOL_NAME already exists)"
echo "rm -rf $SHARE_PATH/$TOOL_NAME" >> uninstall_helper.sh

mkdir $SHARE_PATH/$TOOL_NAME/modules 2> /dev/null
cp perfresultcollector/dbinterface.py $SHARE_PATH/$TOOL_NAME/modules/ 2> /dev/null
assert_error $? "installation of the DB interface" "(unable to copy dbinterface.py to $SHARE_PATH/$TOOL_NAME/modules)"

to_be_installed=`ls perfresultcollector/*.py`
to_be_installed=${to_be_installed/perfresultcollector\/dbinterface.py/}

# fix the python paths
mkdir temp
cp $to_be_installed temp/
sed -i "4isys.path.append(\"$SHARE_PATH/$TOOL_NAME/modules\")" temp/*
to_be_installed=`echo $to_be_installed | sed 's/perfresultcollector\//temp\//g'`
for script in $to_be_installed; do
	BN=`basename $script .py`
	cp $script $INSTALL_PATH/$TOOL_PREFIX-$BN
	assert_error $? "installation of $TOOL_PREFIX-$BN" "I was not able to install the file to $INSTALL_PATH"
	echo "rm -f $INSTALL_PATH/$TOOL_PREFIX-$BN" >> uninstall_helper.sh
done
rm -rf temp

# FINAL announcement that installation passed
echo "INSTALLATION SUCCESSFUL. For uninstalling the tool use the uninstall.sh script."
exit 0
