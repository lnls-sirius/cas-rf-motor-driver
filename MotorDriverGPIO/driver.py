#!/usr/bin/python
# -*- coding: utf-8 -*-
import Adafruit_BBIO.GPIO as GPIO
import converters
import threading
import time

# Pino de comando dos dois relês usados para habilitar/desabilitar os drivers

DRIVER_ENABLE_PIN = "P9_14"

# Inicializa o pino de comando dos relês, desabilitando em seguida os drivers

GPIO.setup(DRIVER_ENABLE_PIN,  GPIO.OUT)
GPIO.output(DRIVER_ENABLE_PIN, GPIO.HIGH)

class RF_MotorControllers_Driver():

    def __init__(self):
        self.ADC1 = converters.ADC()
        self.ADC2 = converters.ADC2()
        self.drvStsVal = 0
        self.drvEnbl(1)


    def data(self):
        ADC1_values = [0] * 8
        ADC2_values = [0] * 8

        for i in range(10):
            ADC1_readings = self.ADC1.read(range(8))
            ADC2_readings = self.ADC2.read(range(8))
            for j in range(8):
                ADC1_values[j] += ADC1_readings[j]
                ADC2_values[j] += ADC2_readings[j]

        return str(ADC1_values + ADC2_values)

    def drvSts(self):
        return 'DRV_ENBL {}'.format(self.drvStsVal)

    def drvEnbl(self, value):
        if (value == 1):
            GPIO.output(DRIVER_ENABLE_PIN, GPIO.LOW)
            self.drvStsVal = 1
        else:
            GPIO.output(DRIVER_ENABLE_PIN, GPIO.HIGH)
            self.drvStsVal = 0

        return 'DRV_ENBL {}'.format(self.drvStsVal)

