#!/bin/bash
# -----------params------------
name=$1

switch_domain() {
    conf_file="/opt/challenge/ctf.sh"
    sed -i "s/Bytectf.*!/Bytectf, $name!/" "$conf_file"
}

# 调用函数
switch_domain
