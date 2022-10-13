#!/bin/bash

wget -O - https://learncertstore.blob.core.windows.net/supercert/supercert.pem > $LOCAL_PATH/supercert.pem
wget -O - https://learncertstore.blob.core.windows.net/supercert/supercert.key > $LOCAL_PATH/supercert.key

