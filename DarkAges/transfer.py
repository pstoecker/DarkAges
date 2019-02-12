u"""
.. module:: transfer
   :synopsis: Definition of the transfer-class and the laod and dump function
.. moduleauthor:: Patrick Stoecker <stoecker@physik.rwth-aachen.de>

Contains the definition of the transfer class :class:`transfer <DarkAgees.transfer.transfer>`
to store the 3D-array of the discretized transfer functions :math:`T_{klm}` and the
1D-array with the values of :math:`z_\\mathrm{dep}`, :math:`\\log_{10} E`, and :math:`z_\\mathrm{inj}`

Also contains methods to store (dump) an instance of this class in a file and
to load them from this.
"""

import numpy as np
import dill

class transfer(object):
	u"""
	Container of the discretized transfer functions :math:`T_{klm}` and the
	arrays with the values at which they are defined.

	Reads the transfer functions and pojts at which they are defined and stores them
	as numpy-arrays.
	"""

	def __init__(self, infile):
		u"""
		Parameters
		----------
		infile : :obj:`str`
			Path to the table z_deposited, log10E, z_injected, transfer_elec and transfer_phot
			in increasing order.
		"""

		#print 'Initializing the transfer functions'
		data = np.genfromtxt(infile, unpack=True, usecols=(0,1,2,3,4), dtype=np.float64 )
		self.z_injected = np.unique(data[2]).astype(np.float64)
		self.z_deposited = np.unique(data[0]).astype(np.float64)
		self.log10E = np.unique(data[1]).astype(np.float64)
		l1 = len(self.z_deposited)
		l2 = len(self.log10E)
		l3 = len(self.z_injected)
		self.transfer_phot = data[4].reshape(l1,l2,l3).astype(np.float64)
		self.transfer_elec = data[3].reshape(l1,l2,l3).astype(np.float64)

	def __neg__(self):
		import copy
		negself = copy.deepcopy(self)
		negself.transfer_phot = -self.transfer_phot
		negself.transfer_elec = -self.transfer_elec
		return negself

def transfer_dump(transfer_instance, outfile):
	u"""Stores a initialized instance of the :class:`transfer <DarkAges.transfer.transfer>`
	-class in file using the dump method of :class:`dill`.

	Parameters
	----------
	transfer_instance : :obj:`class`
		Initialized instance of the :class:`transfer <DarkAges.transfer.transfer>`-class
	outfile : :obj:`str`
		Filename (absolute or relative) under which the transfer instance should be stored
	"""

	if not isinstance(transfer_instance, transfer):
		from .__init__ import DarkAgesError
		raise DarkAgesError('You did not include a proper instance of the class "transfer"')
	with open(outfile, 'wb') as f_dump:
		dill.dump(transfer_instance, f_dump)
	return

def transfer_load(infile):
	u"""Reloads an instance of the :class:`transfer <DarkAges.transfer.transfer>`
	-class dumped with :meth:`transfer_dump <DarkAges.transfer.transfer_dump>`

	Parameters
	----------
	infile : :obj:`str`
		Filename (absolute or relative) under which the transfer instance is stored

	Returns
	-------
	:obj:`class`
		Restored instance of the :class:`transfer <DarkAges.transfer.transfer>`-class
	"""

	loaded_transfer = dill.load(open(infile, 'rb'))
	if not isinstance(loaded_transfer, transfer):
		from .__init__ import DarkAgesError
		raise DarkAgesError('The file {0} does not provide a proper instance of the class "transfer"'.format(infile))
	else:
		return loaded_transfer

def transfer_combine(*transfer_instances):
	if transfer_instances is None:
		raise DarkAgesError('The method "transfer_combine" expects at least one positional argument')
	first_time_in_loop = True
	for single_transfer in transfer_instances:
		if not isinstance(single_transfer,transfer):
			raise DarkAgesError('You did not include a proper instance of the class "transfer"')
		if first_time_in_loop:
			import copy
			first_time_in_loop = False
			transfer_to_return = copy.deepcopy(single_transfer)
		else:
			transfer_to_return.transfer_phot += single_transfer.transfer_phot
			transfer_to_return.transfer_elec += single_transfer.transfer_elec
	return transfer_to_return
