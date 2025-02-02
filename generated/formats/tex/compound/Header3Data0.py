from generated.formats.tex.enum.DdsType import DdsType


class Header3Data0:

	"""
	Data struct for headers of type 3, read by data 0 of 3,7 frag.
	16 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 32 bytes, all 0
		self.zeros = 0

		# flag, not direct index into DDS enum
		self.compression_type = DdsType()

		# 0 or 1
		self.one_0 = 0

		# 1 or 2
		self.one_1 = 0

		# 1 or 2
		self.one_2 = 0

		# 0
		self.pad = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros = stream.read_uint64()
		self.compression_type = DdsType(stream.read_ubyte())
		self.one_0 = stream.read_ubyte()
		self.one_1 = stream.read_ubyte()
		self.one_2 = stream.read_ubyte()
		self.pad = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.zeros)
		stream.write_ubyte(self.compression_type.value)
		stream.write_ubyte(self.one_0)
		stream.write_ubyte(self.one_1)
		stream.write_ubyte(self.one_2)
		stream.write_uint(self.pad)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header3Data0 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* compression_type = {self.compression_type.__repr__()}'
		s += f'\n	* one_0 = {self.one_0.__repr__()}'
		s += f'\n	* one_1 = {self.one_1.__repr__()}'
		s += f'\n	* one_2 = {self.one_2.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
