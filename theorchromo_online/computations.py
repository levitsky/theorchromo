import pyBioLCCC

def process_peptides(length, diameter, pore_size, bmin, bmax, gradient_time,
    delay_time, flow_rate, acna, acnb, peptides):

    chromatograph = pyBioLCCC.ChromoConditions(
        length, diameter, pore_size,
        pyBioLCCC.Gradient(bmin, bmax, gradient_time),
        acna, acnb, delay_time, flow_rate, flow_rate / 20.0)

    output = []
    for sequence in peptides.replace('\r', '').split('\n'):
        peptide_properties = {'sequence': sequence}
        peptide_properties['RT'] = (round(
            pyBioLCCC.calculateRT(str(sequence.strip()), chromatograph), 2))
        peptide_properties['monoisotopicMass'] = (
            pyBioLCCC.calculateMonoisotopicMass(str(sequence.strip())))
        output.append(peptide_properties)

    return output
    

