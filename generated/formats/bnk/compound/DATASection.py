import numpy
import typing
from generated.array import Array


class DATASection:

	"""
	second Section of a soundback aux
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of following data
		self.length = 0
		self.wem_files_datas = numpy.zeros((self.length), dtype='byte')

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.wem_files_datas = stream.read_bytes((self.length))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_bytes(self.wem_files_datas)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'DATASection [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* length = {self.length.__repr__()}'
		s += f'\n	* wem_files_datas = {self.wem_files_datas.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
