import pyBioLCCC

def process_peptides(length, diameter, pore_size, bmin, bmax, gradient_time,
    delay_time, flow_rate, acna, acnb, chromatography_type, peptides,
    is_alkylated):

    chromatograph = pyBioLCCC.ChromoConditions(
        length, diameter, pore_size,
        pyBioLCCC.Gradient(bmin, bmax, gradient_time),
        acna, acnb, delay_time, flow_rate, flow_rate / 20.0)

    chembasis = pyBioLCCC.ChemicalBasis()
    if chromatography_type == 'RP/ACN+FA':
        chembasis.set_min_inf(
            {'pS' : 0.55,
             'pT' : 0.59,
             'pY' : 0.92,
             'Ac-' : -0.05,
             'camC' : 0.24,
             'secondSolventBindEnergy' : 2.4,
             '-COOH' : 1.02,
             'persistentLength' : 1,
             'segmentLength' : 4.0,
             'A' : 0.81,
             'C' : 0.90,
             'E' : 0.62,
             'D' : 0.60,
             'G' : 0.47,
             'F' : 2.65,
             'I' : 2.2,
             'H' : -0.77,
             'K' : -0.64,
             'M' : 1.73,
             'L' : 2.38,
             'N' : 0.28,
             'Q' : 0.47,
             'P' : 0.62,
             'S' : 0.5,
             'R' : -0.59,
             'T' : 0.69,
             'W' : 2.87,
             'V' : 1.49,
             'Y' : 1.40,
             '-NH2' : 0.55,
             'oxM' : 1.82,
             'adsorbtionLayerWidth' : 16.0 ,
             'H-' : -2.39,
             'model' : 'RodBoltzmann'})

    output = []
    for sequence in peptides.replace('\r', '').split('\n'):
        if is_alkylated:
            # Several replacements are done in the sake of parseability.
            sequence = sequence.replace('camC', 'C').replace('C', 'camC')
            sequence = sequence.replace('-camC','-C')
        peptide_properties = {'sequence': sequence}
        peptide_properties['RT'] = (round(
            pyBioLCCC.calculateRT(
                str(sequence.strip()), chromatograph, chembasis), 2))
        peptide_properties['monoisotopicMass'] = (
            pyBioLCCC.calculateMonoisotopicMass(
                str(sequence.strip()), chembasis))
        output.append(peptide_properties)

    return output

