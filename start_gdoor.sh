#!/bin/bash -e

#Adapted from http://www.armhf.com/using-beaglebone-black-gpios/

if [ "$(id -u)" != "0" ]; then
  echo "Requires super user"
  exit 1
fi

#Setup gpio for output
if [ ! -d /sys/class/gpio/gpio48 ]; then echo 48 > /sys/class/gpio/export; fi
#if [ ! -d /sys/class/gpio/gpio50 ]; then echo 50 > /sys/class/gpio/export; fi
#if [ ! -d /sys/class/gpio/gpio51 ]; then echo 51 > /sys/class/gpio/export; fi
#if [ ! -d /sys/class/gpio/gpio60 ]; then echo 60 > /sys/class/gpio/export; fi

#To set a gpio as output, we set its direction as in or out. For outputs there is an alternative nomenclature where output direction can be set instead as high or low to help with glitch free operation.

#intialize output as low
echo low > /sys/class/gpio/gpio48/direction
#echo low > /sys/class/gpio/gpio50/direction
#echo low > /sys/class/gpio/gpio51/direction
#echo low > /sys/class/gpio/gpio60/direction

#for (( i=0 ; ; ++i ))
#do
#   if (( i > 0x0f )); then
#      i=0
#      printf '\n[press  + c to stop]\n\n'
#   fi
#
#   bit0=$(( (i & 0x01) > 0 ))
#   bit1=$(( (i & 0x02) > 0 ))
#   bit2=$(( (i & 0x04) > 0 ))
#   bit3=$(( (i & 0x08) > 0 ))
#   echo $bit3 $bit2 $bit1 $bit0
#
#   echo $bit0 > /sys/class/gpio/gpio60/value
#   echo $bit1 > /sys/class/gpio/gpio50/value
#   echo $bit2 > /sys/class/gpio/gpio48/value
#   echo $bit3 > /sys/class/gpio/gpio51/value
#
#   sleep .2
#done

python /home/ubuntu/gdoor_server/gdoor_server.py
