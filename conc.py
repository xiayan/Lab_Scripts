#!/usr/bin/env python

# a and b defines as the value in y = ax + b

#a = 0.0008
#b = 0.0309
a = 0.7774
b = 0.02

def isnumeric(value):
  return str(value).replace(".", "").replace("-", "").isdigit()

def main():
	data = raw_input("Enter readings: ")
	while data == "":
		data = raw_input("Need at least one numeric input: ")
	readings = data.split()
    
	while True:
		allDigit = True
		for r in readings:
			if (not isnumeric(r)):
				allDigit = False
				data = raw_input("Enter all numeric values: ")
				readings = data.split(' ')
				break
		if allDigit:
			break

	results = []
	mw = raw_input("Enter molecular weight: ")
	if mw == "":
		moreInfo = False
	else:
		moreInfo = True

	dilution = raw_input("Enter dilution factor: ")
	if dilution == "":
		dilution = 1
	else:
		dilution = eval(dilution)

	if a > 0.09:
		magnitude = 1000000.0
		unit = 'm'
	else:
		magnitude = 1000.0
		unit = 'u'
	for r in readings:
		conc = (eval(r) - b) / a * dilution
		if moreInfo:
			molConc = conc / eval(mw) * magnitude
		else:
			molConc = 0.0
		results.append((conc, molConc))

	for (conc, molConc) in results:
		print ("%0.2f" %conc) + ' ' + unit + 'g/ml'
		if moreInfo:
			print ("%0.2f" %molConc) + ' ' + unit + 'M'
		print "\n"

main()
