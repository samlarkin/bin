#!/usr/bin/env bash
reflector --latest 20 --protocol https --sort rate --save /etc/pacman.d/mirrorlist
