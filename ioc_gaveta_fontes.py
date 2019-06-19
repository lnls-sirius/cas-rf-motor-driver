#!/usr/bin/python
# -*- coding: utf-8 -*-

from pcaspy import Driver, SimpleServer
import Adafruit_BBIO.GPIO as GPIO
import converters
import threading
import time

# Pino de comando dos dois relês usados para habilitar/desabilitar os drivers

DRIVER_ENABLE_PIN = "P9_14"

# Inicializa o pino de comando dos relês, desabilitando em seguida os drivers

GPIO.setup(DRIVER_ENABLE_PIN, GPIO.OUT)
GPIO.output(DRIVER_ENABLE_PIN, GPIO.HIGH)

# PVs servidas por este programa

PVs = {}

# PVs para monitoração das fontes de tensão

PVs["RA-RaBO01:RF-LLRFPlDrivers:VoltPos5V-Mon"] = { "type" : "float", "prec" : 3, "unit" : "V" }
PVs["RA-RaBO01:RF-LLRFPlDrivers:Current5V-Mon"] = { "type" : "float", "prec" : 3, "unit" : "A" }
PVs["RA-RaBO01:RF-LLRFPlDrivers:VoltPos48V-Mon"] = { "type" : "float", "prec" : 2, "unit" : "V" }

# PV usada para habilitar ou desabilitar os drivers de motor

PVs["RA-RaBO01:RF-LLRFPlDrivers:DrEnbl-Sel"] = { "type" : "enum", "enums" : ["Enabled", "Disabled"] }

# PVs usadas para monitorar cada um dos drivers: estado (habilitado/desabilitado), sinal de falha
# (operação normal/falha), corrente consumida e posição do plunger correspondente.

PVs["RA-RaBO01:RF-LLRFPlDrivers:Dr1Enbl-Mon"] = { "type" : "enum", "enums" : ["Enabled", "Disabled"] }
PVs["RA-RaBO01:RF-LLRFPlDrivers:Dr1Flt-Mon"] = { "type" : "enum", "enums" : ["Normal", "Fail"] }
PVs["RA-RaBO01:RF-LLRFPlDrivers:Dr1Current-Mon"] = { "type" : "float", "prec" : 3, "unit" : "A" }
PVs["BO-05D:RF-P5Cav:Pl1Pos-Mon"] = { "type" : "float", "prec" : 3, "unit" : "V" }

PVs["RA-RaBO01:RF-LLRFPlDrivers:Dr2Enbl-Mon"] = { "type" : "enum", "enums" : ["Enabled", "Disabled"] }
PVs["RA-RaBO01:RF-LLRFPlDrivers:Dr2Flt-Mon"] = { "type" : "enum", "enums" : ["Normal", "Fail"] }
PVs["RA-RaBO01:RF-LLRFPlDrivers:Dr2Current-Mon"] = { "type" : "float", "prec" : 3, "unit" : "A" }
PVs["BO-05D:RF-P5Cav:Pl2Pos-Mon"] = { "type" : "float", "prec" : 3, "unit" : "V" }

class RF_MotorControllers_Driver(Driver):

    def __init__(self):

        Driver.__init__(self)

        self.ADC1 = converters.ADC()
        self.ADC2 = converters.ADC2()

        self.setParam("RA-RaBO01:RF-LLRFPlDrivers:DrEnbl-Sel", 1)

        self.process_thread = threading.Thread(target = self.processThread)
        self.process_thread.setDaemon(True)
        self.process_thread.start()

    def processThread(self):

        timestamp = time.time()

        while (True):

            ADC1_values = [0] * 8
            ADC2_values = [0] * 8

            for i in range(10):
                ADC1_readings = self.ADC1.read(range(8))
                ADC2_readings = self.ADC2.read(range(8))
                for j in range(8):
                    ADC1_values[j] += ADC1_readings[j]
                    ADC2_values[j] += ADC2_readings[j]

            for i in range(8):
                ADC1_values[i] = ((ADC1_values[i] / 10.0) / 4095.0) * 5.0
                ADC2_values[i] = ((ADC2_values[i] / 10.0) / 4095.0) * 5.0
            ADC2_values[1] = ADC2_values[1] * 11

            self.setParam("RA-RaBO01:RF-LLRFPlDrivers:VoltPos5V-Mon", ADC2_values[0])
            self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Current5V-Mon", (ADC2_values[2] - 0.5) / 0.4)
            self.setParam("RA-RaBO01:RF-LLRFPlDrivers:VoltPos48V-Mon", ADC2_values[1])

            if (ADC1_values[4] > 2.5):
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr1Enbl-Mon", 1)
            else:
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr1Enbl-Mon", 0)
            if (ADC1_values[5] > 2.5):
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr1Flt-Mon", 1)
            else:
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr1Flt-Mon", 0)
            self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr1Current-Mon", (ADC1_values[3] - 0.5) / 0.4)
            self.setParam("BO-05D:RF-P5Cav:Pl1Pos-Mon", ADC1_values[6])

            if (ADC2_values[4] > 2.5):
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr2Enbl-Mon", 1)
            else:
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr2Enbl-Mon", 0)
            if (ADC2_values[5] > 2.5):
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr2Flt-Mon", 1)
            else:
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr2Flt-Mon", 0)
            self.setParam("RA-RaBO01:RF-LLRFPlDrivers:Dr2Current-Mon", (ADC2_values[3] - 0.5) / 0.4)
            self.setParam("BO-05D:RF-P5Cav:Pl2Pos-Mon", ADC2_values[6])

            self.updatePVs()

            if ((self.getParam("RA-RaBO01:RF-LLRFPlDrivers:Dr1Flt-Mon") == 1) or (self.getParam("RA-RaBO01:RF-LLRFPlDrivers:Dr2Flt-Mon") == 1)):
                GPIO.output(DRIVER_ENABLE_PIN, GPIO.HIGH)
                self.setParam("RA-RaBO01:RF-LLRFPlDrivers:DrEnbl-Sel", 1)

            timestamp = timestamp + 1
            time.sleep(timestamp - time.time())

    def write(self, reason, value):
        if (reason == "RA-RaBO01:RF-LLRFPlDrivers:DrEnbl-Sel"):
            self.setParam(reason, value)
            if (value == 0):
                GPIO.output(DRIVER_ENABLE_PIN, GPIO.LOW)
            else:
                GPIO.output(DRIVER_ENABLE_PIN, GPIO.HIGH)
            return(True)
        else:
            return(False)

if (__name__ == "__main__"):

    CAserver = SimpleServer()
    CAserver.createPV("", PVs)
    driver = RF_MotorControllers_Driver()

    while (True):
        CAserver.process(0.1)
