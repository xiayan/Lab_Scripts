"""
This script parse ATOM lines in PDB files
"""

def parse_pdb(line):
    """parse line of pdb"""
    parsed_pdb = {}
    parsed_pdb['atomType'] = line[:6].strip()
    parsed_pdb['serialNo'] = line[6:11].strip()
    parsed_pdb['atomName'] = line[12:16].strip()
    parsed_pdb['altLoc']   = line[16]
    parsed_pdb['resName']  = line[17:20].strip()
    parsed_pdb['chainID']  = line[21]
    parsed_pdb['resSeqNo'] = line[22:26].strip()
    parsed_pdb['iCode']    = line[26]
    parsed_pdb['xCoord']   = line[30:38].strip()
    parsed_pdb['yCoord']   = line[38:46].strip()
    parsed_pdb['zCorrd']   = line[46:54].strip()
    parsed_pdb['occup']    = line[54:60].strip()
    parsed_pdb['tempFctr'] = line[60:66].strip()
    parsed_pdb['segID']    = line[72:76].strip()
    parsed_pdb['element']  = line[76:78].strip()
    parsed_pdb['charge']   = line[78:80].strip()

    return parsed_pdb

def combine_line(parsed_pdb):
    """combine fields in dictionary back to line"""
    fields = ''
    fields += '{:<6}'.format(parsed_pdb['atomType'])
    fields += '{:>5}'.format(parsed_pdb['serialNo']) + ' '
    fields += '{:^4}'.format(parsed_pdb['atomName'])
    fields += parsed_pdb['altLoc']
    fields += '{:^3}'.format(parsed_pdb['resName'])
    fields += ' ' + parsed_pdb['chainID']
    fields += '{:>4}'.format(parsed_pdb['resSeqNo'])
    fields += parsed_pdb['iCode'] + '   '
    fields += '{:>8}'.format(parsed_pdb['xCoord'])
    fields += '{:>8}'.format(parsed_pdb['yCoord'])
    fields += '{:>8}'.format(parsed_pdb['zCorrd'])
    fields += '{:>6}'.format(parsed_pdb['occup'])
    fields += '{:>6}'.format(parsed_pdb['tempFctr']) + '      '
    fields += '{:<4}'.format(parsed_pdb['segID'])
    fields += '{:>2}'.format(parsed_pdb['element'])
    fields += '{:<2}'.format(parsed_pdb['charge'])

    return fields
