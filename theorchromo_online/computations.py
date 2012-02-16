import pyteomics.biolccc as pyBioLCCC

def process_peptides(length, diameter, pore_size, bmin, bmax, gradient_time,
    delay_time, flow_rate, acna, acnb, chromatography_type, peptides,
    is_alkylated):

    chromatograph = pyBioLCCC.ChromoConditions(
        length, diameter, pore_size,
        pyBioLCCC.Gradient(bmin, bmax, gradient_time),
        acna, acnb, delay_time, flow_rate, flow_rate / 20.0)

    if chromatography_type == 'RP/ACN+FA':
        chembasis = pyBioLCCC.rpAcnFaRod
    elif chromatography_type == 'RP/ACN+TFA':
        chembasis = pyBioLCCC.rpAcnTfaChain
    
    output = []
    for sequence in peptides.replace('\r', '').split('\n'):
        if is_alkylated:
            # Several replacements are done in the sake of parseability.
            sequence = sequence.replace('camC', 'C').replace('C', 'camC')
        peptide_properties = {'sequence': sequence}
        try:
            peptide_properties['RT'] = (round(
                pyBioLCCC.calculateRT(
                    str(sequence.strip()), chembasis, chromatograph, 21), 2))
            peptide_properties['monoisotopicMass'] = (
                pyBioLCCC.calculateMonoisotopicMass(
                    str(sequence.strip()), chembasis))
        except:
            peptide_properties['RT'] = 'sequence'
            peptide_properties['monoisotopicMass'] = 'cannot be parsed'
        output.append(peptide_properties)

    return output

