#!/bin/bash

#HWMON="/sys/class/hwmon/hwmon5"

echo 1 | sudo tee /sys/class/hwmon/hwmon5/pwm1_enable
echo 1 | sudo tee /sys/class/hwmon/hwmon5/pwm2_enable
echo 1 | sudo tee /sys/class/hwmon/hwmon5/pwm3_enable

for fan in 1 2 3; do
  for i in {1..8}; do
    echo 255 | sudo tee /sys/class/hwmon/hwmon5/pwm${fan}_auto_point${i}_pwm
  done
done

echo "TURBO MODE ENABLED — ALL FANS MAX SPEED (255)"

