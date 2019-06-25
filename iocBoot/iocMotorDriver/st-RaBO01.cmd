#!../../bin/linux-arm/MotorDriver

< envPaths

cd "${TOP}"

epicsEnvSet("P","RA-RaBO01:")
epicsEnvSet("R","")

## Register all support components
dbLoadDatabase "dbd/MotorDriver.dbd"
MotorDriver_registerRecordDeviceDriver pdbbase

drvAsynIPPortConfigure("L0", "unix://$(TOP)/MotorDriverGPIO/unix-socket")

## Load record instances
dbLoadRecords("db/MotorDriverData.db","P=$(P),R=$(R),PORT=L0,A=0")
dbLoadRecords("db/MotorDriver.db"    ,"P=$(P),R=$(R),PORT=L0,A=0")

cd "${TOP}/iocBoot/${IOC}"
iocInit
