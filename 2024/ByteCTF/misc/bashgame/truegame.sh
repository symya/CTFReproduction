#!/bin/bash

if [[ "$1" -eq 1 ]]; then
    sudo cat "$1"
else
    echo 'wrong'
fi
