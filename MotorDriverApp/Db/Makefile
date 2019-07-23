TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

#----------------------------------------------------
#  Optimization of db files using dbst (DEFAULT: NO)
#DB_OPT = YES

#----------------------------------------------------
# Create and install (or just install) into <top>/db
# databases, templates, substitutions like this
#DB += xxx.db

#----------------------------------------------------
# If <anyname>.db template is not named <anyname>*.template add
# <anyname>_template = <templatename>


# Install .dbd and .db files
DB += MotorDriver.db
DB += MotorDriverData.db
DB += MotorDriver.proto

#=======================================
.PHONY: db
db:
	python3 db.py > MotorDriverData.db


include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

