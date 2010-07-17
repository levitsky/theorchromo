from django import forms
import pyBioLCCC

class ChromoConditionsForm(forms.Form):
    error_css_class = 'error'
    length = forms.FloatField(
        label="Column length, mm",
        initial=pyBioLCCC.standardChromoConditions.columnLength(),
        min_value=0.0,
        max_value=1.0e4,
        error_messages = {
            'required' : u'Column length is required.',
            'invalid'  : u'Column length must be a number.',
            'min_value': 
                u'Column length must be greater than %(limit_value)d mm.',
            'max_value':
                u'Column length must be less than %(limit_value)d mm.'})
    diameter = forms.FloatField(
        label='Column internal diameter, mm', 
        initial=pyBioLCCC.standardChromoConditions.columnDiameter(),
        min_value=0.0,
        max_value=1.0e2,
        error_messages = {
            'required' : u'Column diameter is required.',
            'invalid'  : u'Column diameter must be a number.',
            'min_value':
                u'Column diameter must be greater than %(limit_value)d mm.',
            'max_value': 
                u'Column diameter must be less than %(limit_value)d mm.'})
    pore_size = forms.FloatField(
        label='Packing material pore size, A', 
        initial=pyBioLCCC.standardChromoConditions.columnPoreSize(),
        min_value=60.0,
        max_value=1000.0,
        error_messages = {
            'required' : u'Packing material pore size is required.',
            'invalid'  : u'Packing material pore size must be a number.',
            'min_value': u'Packing material pore size must be greater than %(limit_value)d A.',
            'max_value': u'Packing material pore size must be less than %(limit_value)d A.'})
    bmin = forms.FloatField(
        label='Initial concentration of B component, %',
        initial=(
            pyBioLCCC.standardChromoConditions.gradient()[0].concentrationB()),
        min_value=0.0,
        max_value=100.0,
        error_messages = {
            'required' : u'Initial concentration of B component is required.',
            'invalid'  : u'Initial concentration of B component must be a number.',
            'min_value': u'Initial concentration of B component must be greater than %(limit_value)d%%.',
            'max_value': u'Initial concentration of B component must be less than %(limit_value)d%%.'})
    bmax = forms.FloatField(
        label='Final concentration of B component, %',
        initial=(
            pyBioLCCC.standardChromoConditions.gradient()[1].concentrationB()),
        min_value=0.0,
        max_value=100.0,
        error_messages = {
            'required' : u'Final concentration of B component is required.',
            'invalid'  : u'Final concentration of B component must be a number.',
            'min_value': u'Final concentration of B component must be greater than %(limit_value)d%%.',
            'max_value': u'Final concentration of B component must be less than %(limit_value)d%%.'})
    gradient_time = forms.FloatField(
        initial=pyBioLCCC.standardChromoConditions.gradient()[1].time(),
        label='Gradient time, min',
        min_value=0.0, 
        max_value=1000.0,
        error_messages = {
            'required' : u'Gradient time is required.',
            'invalid'  : u'Gradient time must be a number.',
            'min_value': u'Gradient time must be greater than %(limit_value)d min.',
            'max_value': u'Gradient time must be less than %(limit_value)d min.'})
    delay_time = forms.FloatField(
        initial=pyBioLCCC.standardChromoConditions.delayTime(),
        label='Delay time, min',
        min_value=0.0,
        max_value=1000.0,
        error_messages = {
            'required' : u'Delay time is required.',
            'invalid'  : u'Delay time must be a number.',
            'min_value': u'Delay time must be greater than %(limit_value)d min.',
            'max_value': u'Delay time must be less than %(limit_value)d min.'})
    flow_rate = forms.FloatField(
        label='Flow rate, ml/min',
        initial=pyBioLCCC.standardChromoConditions.flowRate(),
        min_value=0.0,
        max_value=100.0,
        error_messages = {
            'required' : u'Flow rate is required.',
            'invalid'  : u'Flow rate must be a number.',
            'min_value': u'Flow rate must be greater than %(limit_value)d ml/min.',
            'max_value': u'Flow rate must be less than %(limit_value)d ml/min.'})
    acna = forms.FloatField(
        label='ACN concentration in A component, %',
        initial=(
            pyBioLCCC.standardChromoConditions.secondSolventConcentrationA()),
        min_value=0.0,
        max_value=100.0,
        error_messages = {
            'required' : u'ACN concentration in A component is required.',
            'invalid'  : u'ACN concentration in A component must be a number.',
            'min_value': u'ACN concentration in A component must be greater than %(limit_value)d%%.',
            'max_value': u'ACN concentration in A component must be less than %(limit_value)d%%.'})
    acnb = forms.FloatField(
        label='ACN concentration in B component, %',
        initial=(
            pyBioLCCC.standardChromoConditions.secondSolventConcentrationB()),
        min_value=0.0,
        max_value=100.0,
        error_messages = {
            'required' : u'ACN concentration in B component is required.',
            'invalid'  : u'ACN concentration in B component must be a number.',
            'min_value': u'ACN concentration in B component must be greater than %(limit_value)d%%.',
            'max_value': u'ACN concentration in B component must be less than %(limit_value)d%%.'})

class PeptideSequencesForm(forms.Form):
    peptides = forms.CharField(
        label='Peptide sequences',
        widget=forms.Textarea(attrs={'rows':11, 'cols':40}))
