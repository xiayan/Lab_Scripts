"""Calculate concentration from bradford absorbtions"""
#!/usr/bin/env python

from ast import literal_eval

# a and b defines as the value in y = ax + b
# range is 0ug/ml to 500ug/ml. Reading: 0 to 0.62

a = 0.0012
b = 0.0048

def isnumeric(value):
    """Test if a string is numeric"""
    return str(value).replace(".", "").replace("-", "").isdigit()

def main():
    data = raw_input("Enter readings: ")
    while data == "":
        data = raw_input("Need at least one numeric input: ")
    readings = data.split()

    while True:
        all_digits = True
        for read in readings:
            if not isnumeric(read):
                all_digits = False
                data = raw_input("Enter all numeric values: ")
                readings = data.split(' ')
                break
        if all_digits:
            break

    results = []
    mol_weight = raw_input("Enter molecular weight: ")
    more_info = False
    if mol_weight == "":
        more_info = False
    else:
        more_info = True

    dilution = raw_input("Enter dilution factor: ")
    if dilution == "":
        dilution = 1
    else:
        dilution = literal_eval(dilution)

    if a > 0.09:
        magnitude = 1000000.0
        unit = 'm'
    else:
        magnitude = 1000.0
        unit = 'u'
    for read in readings:
        conc = (literal_eval(read) - b) / a * dilution
        if more_info:
            mol_conc = conc / literal_eval(mol_weight) * magnitude
        else:
            mol_conc = 0.0
        results.append((conc, mol_conc))

    for (conc, mol_conc) in results:
        print ("%0.2f" %conc) + ' ' + unit + 'g/ml'
        if more_info:
            print ("%0.2f" %mol_conc) + ' ' + unit + 'M'
        print "\n"

main()
