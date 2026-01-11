#!/bin/bash

HWMON="/sys/class/hwmon/hwmon5"

echo 2 | sudo tee $HWMON/pwm1_enable
echo 2 | sudo tee $HWMON/pwm2_enable
echo 2 | sudo tee $HWMON/pwm3_enable

echo "Auto mode"

