#!/usr/bin/python3
from string import Template
adc = Template('''
record(calc, "$(P)$(R)${PV}"){
    field(CALC, "((A/10)/4095.)*5.")
    field(INPA, "$(P)$(R)Data-Mon.VAL[${N}] CP MSS")
}
''')

if __name__ == '__main__':
    db = ''
    kwargs = {}

    for i in range(16):
        kwargs['N'] = i
        kwargs['PV'] = ('ADC1_value{}-Mon'.format(i)) if i < 8 else ('ADC2_value{}-Mon'.format(i-8))
        db += adc.safe_substitute(**kwargs)

    print(db)
