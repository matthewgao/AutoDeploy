#!/usr/bin/env bash


msg() {
    printf '%b\n' "$1" >&2
}

success() {
    if [ "$ret" -eq '0' ]; then
        msg "\33[32m[✔]\33[0m ${1}${2}"
    else
        error "Execute fail"
    fi
}

error() {
    msg "\33[31m[✘]\33[0m ${1}${2}"
    exit 1
}

msg "start to sync the code from p4" 
p4 -u shgao -P password sync //depot/Firmware/EXSeriesVPN/kanga/tip/src/avt/authentication-api/pytest/...#head
ret="$?"
success "sync code done"

msg "clean up vagrant"

cd ~/vm-imaging/vm-imaging/Firmware/EXSeriesVPN/kanga/tip/
#echo 'password' |sudo -S vagrant destroy
echo "password" | sudo vagrant up

ret="$?"
success "clean up and restart vagrant done"

msg "ssh to vagrant to compile a image"
sudo vagrant ssh -c 'cd /build && sudo make clean && sudo -E make unstripped.iso && sudo cp unstripped.iso /vagrant-build/. && exit'
ret="$?"
success "Compile done"

msg "make a VM"
../vm-imaging/make-machine.sh -n DailyBuild -i ./unstripped.iso -h 10.103.240.230
ret="$?"
success "All Done!"
