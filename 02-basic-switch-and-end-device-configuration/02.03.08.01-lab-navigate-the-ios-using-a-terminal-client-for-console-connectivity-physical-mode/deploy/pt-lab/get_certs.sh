#!/bin/bash
curl -o $LOCAL_PATH/supercert.pem https://learncertstore.blob.core.windows.net/supercert/supercert.pem --retry 3 --retry-all-errors --retry-delay 2
curl -o $LOCAL_PATH/supercert.key https://learncertstore.blob.core.windows.net/supercert/supercert.key --retry 3 --retry-all-errors --retry-delay 2