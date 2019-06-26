# CAS RF Motor Driver
Authors: Claudio Carneiro, Eduardo Coelho

## Requirements

|Module|Path|
|:----:|:--:|
|EPICS_BASE|/opt/epics-R3.15.5/base|
|ASYN|/opt/epics-R3.15.5/modules/asyn4-35|
|CALC|/opt/epics-R3.15.5/modules/synApps/calc-R3-7-1|
|STREAM|/opt/epics-R3.15.5/modules/StreamDevice-2.8.8|
|AUTOSAVE|/opt/epics-R3.15.5/modules/autosave-R5-9|

[https://wiki-sirius.lnls.br/mediawiki/index.php/CON:Setting_up_EPICS](Setting up EPICS)

## Installation
```
make clean
make dist-clean
cd MotorDriverSup
make db
cd ..
make
```
Install the systemd services. There is a service file for each `iocBoot/MotorDriver/*.cmd`, the EPICS engineer should install the corresponding one. DEVICE is a placeholder. 
```
cp services/cas-rf-motor-driver-gpio.service /etc/systemd/system/cas-rf-motor-driver-gpio.service
cp services/cas-rf-motor-driver-ioc-<DEVICE>.service /etc/systemd/system/cas-rf-motor-driver-ioc-<DEVICE>.service

systemctl daemon-reload
systemctl enable cas-rf-motor-driver-gpio.service
systemctl enable cas-rf-motor-driver-ioc-<DEVICE>.service

systemctl start cas-rf-motor-driver-gpio.service
systemctl start cas-rf-motor-driver-ioc-<DEVICE>.service
```
Check for errors
```
systemctl status cas-rf-motor-driver-gpio.service
systemctl status cas-rf-motor-driver-ioc-<DEVICE>.service
```

