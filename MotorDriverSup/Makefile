TOP=..
include $(TOP)/configure/CONFIG
#=======================================

# Install .dbd and .db files
DB_INSTALLS += $(TOP)/MotorDriverSup/MotorDriver.db
DB_INSTALLS += $(TOP)/MotorDriverSup/MotorDriverData.db
DB_INSTALLS += $(TOP)/MotorDriverSup/MotorDriver.proto

#=======================================
.PHONY: db
db:
	python3 $(TOP)/MotorDriverSup/db.py > $(TOP)/MotorDriverSup/MotorDriverData.db

include $(TOP)/configure/RULES
