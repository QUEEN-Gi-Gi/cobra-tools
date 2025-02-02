import numpy
import typing
from generated.array import Array
from generated.formats.ms2.compound.Ms2BufferInfoZTHeader import Ms2BufferInfoZTHeader


class Ms2Buffer0:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.name_hashes = numpy.zeros((), dtype='uint')
		self.names = Array()
		self.zt_streams_header = Ms2BufferInfoZTHeader()

	def read(self, stream):

		self.io_start = stream.tell()
		self.name_hashes = stream.read_uints((self.arg.name_count))
		self.names = stream.read_zstrings((self.arg.name_count))
		if stream.version == 17:
			self.zt_streams_header = stream.read_type(Ms2BufferInfoZTHeader, (self.arg,))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uints(self.name_hashes)
		stream.write_zstrings(self.names)
		if stream.version == 17:
			stream.write_type(self.zt_streams_header)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Ms2Buffer0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_hashes = {self.name_hashes.__repr__()}'
		s += f'\n	* names = {self.names.__repr__()}'
		s += f'\n	* zt_streams_header = {self.zt_streams_header.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
