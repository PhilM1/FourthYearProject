#!/bin/bash
if [ "$1" == "-u" ]
then
    echo "Unmounting bucket..."
    fusermount -u ~/bucket
else
    echo "Mounting bucket..."
    gcsfuse --implicit-dirs metasurface_data ~/bucket
fi