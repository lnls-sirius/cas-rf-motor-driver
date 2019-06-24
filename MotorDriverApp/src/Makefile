TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = MotorDriver
# MotorDriver.dbd will be created and installed
DBD += MotorDriver.dbd

# MotorDriver.dbd will be made up from these files:
MotorDriver_DBD += base.dbd
MotorDriver_DBD += calcSupport.dbd
MotorDriver_DBD += asSupport.dbd
MotorDriver_DBD += asyn.dbd
MotorDriver_DBD += stream.dbd
MotorDriver_DBD += drvAsynIPPort.dbd

# Include dbd files from all support applications:
MotorDriver_LIBS += calc
MotorDriver_LIBS += autosave
MotorDriver_LIBS += asyn
MotorDriver_LIBS += stream

# Add all the support libraries needed by this IOC
#MotorDriver_LIBS += xxx

# MotorDriver_registerRecordDeviceDriver.cpp derives from MotorDriver.dbd
MotorDriver_SRCS += MotorDriver_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
MotorDriver_SRCS_DEFAULT += MotorDriverMain.cpp
MotorDriver_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#MotorDriver_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
MotorDriver_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

