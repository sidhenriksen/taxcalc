import numpy as np

def calculate_tax_rates(x,bands,maxAllowance=123000):
    
    taxBands = np.diff([0] + [k[0] for k in bands])
    taxRates = np.array([k[1] for k in bands])
    
    # tapering personal allowance
    taperedPA = np.max([0,x-maxAllowance])
    adjustedPA = taxBands[0] - taperedPA/2
    taxBands[0] = np.max([0,adjustedPA])
    
    payInBand = np.zeros(len(bands))
    remaining = x
    for i,band in enumerate(taxBands):
        
        inBand = remaining if band > remaining else band
        remaining -= inBand
        
        payInBand[i] = inBand
        
        if remaining == 0:
            break
    
    
    if x > maxAllowance:
        taxRates[0] = taxRates[1]
        
    totalTaxes = taxRates.dot(payInBand)
    
    return totalTaxes

def scotland_2018(x):
    band0 = (11850,0.0) # personal allowance
    band1 = (13850,0.19)
    band2 = (24000,0.2)
    band3 = (44273,0.21)
    band4 = (150000,0.41)
    band5 = (np.inf,0.46)
    
    bands = [band0,band1,band2,band3,band4,band5]
    return calculate_tax_rates(x,bands)

def scotland_2017(x):
    band0 = [11500,0.0]
    band1 = [43000,0.2]
    band2 = [150000,0.4]
    band3 = [np.inf,0.45]

    bands = [band0,band1,band2,band3]

    return calculate_tax_rates(x,bands)

def ruk_2018(x):
    band0 = [11850,0.0] # personal allowance
    band1 = [46350,0.2]
    band2 = [150000,0.4]
    band3 = [np.inf,0.45]
    
    bands = [band0,band1,band2,band3]
    return calculate_tax_rates(x,bands)

def ruk_2017(x):
    band0 = [11500,0.0]
    band1 = [45000,0.2]
    band2 = [150000,0.4]
    band3 = [np.inf,0.45]
    
    bands = [band0,band1,band2,band3]
    return calculate_tax_rates(x,bands)

def national_insurance(x):
    band0 = [8164,0.0]
    band1 = [45032,0.12]
    band2 = [np.inf,0.02]

    bands = [band0,band1,band2]
    return calculate_tax_rates(x,bands)
