import DarkAges
from DarkAges.model import decaying_model as mod
from DarkAges import get_redshift, transfer_functions, channel_dict, DarkAgesError

import numpy as np

alreadyCalculated = False
f_functions = None
redshift = None 

def initialize():
	global redshift
	redshift = get_redshift() 

def calculate_f_for_decay(energies, electron_spectrum, photon_spectrum, mass, lifetime):
	global f_functions
	global alreadyCalculated
	#global redshift 
	if not alreadyCalculated:
		if f_functions is None:
			f_functions = dict()
		logEnergies = np.log10(1e9*energies) 
		model = mod(1e-9*electron_spectrum, 1e-9*photon_spectrum, np.zeros_like(electron_spectrum), 1e9*mass, lifetime, logEnergies, redshift, normalize_spectrum_by='energy_integral')
		for channel, idx in channel_dict.iteritems(): 
			transfer = transfer_functions[idx]
			f = model.calc_f(transfer)[-1]
			out = np.zeros((len(f)+1), dtype=np.float64)
			out[0] = f[0]
			out[-1] = f[-2]
			out[1:-1] = f[:-1] 
			f_functions.update({channel:out})
		out = np.zeros((len(redshift)+1), dtype=np.float64)
		out[0] = 0.
		out[-1] = 1e4
		out[1:-1] = redshift[:-1] - np.ones_like(redshift[:-1])
		f_functions.update({'redshift':out})
		alreadyCalculated = True
	else:
		print 'It seems I already entered this function on a previous point. Skipping all the calculations.'

def get_result(key):
	if not alreadyCalculated or f_functions is None:
		raise DarkAgesError('The calculation of f(z) was not performed yet. Cannot return any results')
	if key in f_functions.keys():
		return f_functions.get(key)

if __name__ == '__main__':
	E = 5.*np.ones((1,)) # in GeV
	m = 10. # in GeV
	tau = 1e16 # in s
	spec_el = 0.0*np.ones((1,))*1e9 # in 1/GeV -> 1e9 * 1/eV
	spec_ph = 2.0*np.ones((1,))*1e9 # in 1/GeV -> 1e9 * 1/eV
	initialize()
	calculate_f_for_decay(E, spec_el, spec_ph, m, tau)
	print 30*'#'
	print 'redshift', get_result('redshift')[-4:]
	print 'Heat', get_result('Heat')[-4:]
	print 'Ly-A', get_result('Ly-A')[-4:]
	print 'H-Ion', get_result('H-Ion')[-4:]
	print 'He-Ion', get_result('He-Ion')[-4:]
	print 'LowE', get_result('LowE')[-4:]
	print 30*'#'
	
		
