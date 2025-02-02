# START_GLOBALS
from generated.io import BinaryStream
from modules.formats.shared import get_padding

ZERO = b"\x00"


# END_GLOBALS

class ZStringBuffer:
	"""Holds a buffer of zero-terminated strings"""

# START_CLASS

	def __init__(self, arg=None, template=None):
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""
		self.strings = []

	def read(self, stream):
		self.data = stream.read(self.arg)
		self.strings = self.data.split(ZERO)

	def write(self, stream):
		stream.write(self.data)

	def get_str_at(self, pos):
		end = self.data.find(ZERO, pos)
		return self.data[pos:end].decode()

	def update_with(self, list_of_arrays):
		"""Updates this name buffer with a list of (array, attrib) whose elements have
		offset: bytes relative to the start of the name block
		[attrib]: string"""
		print("Updating name buffer")
		self.strings = []
		offset_dic = {}
		with BinaryStream() as stream:
			# for name in self.names:
			for array, attrib in list_of_arrays:
				for item in sorted(array, key=lambda i: getattr(i, attrib)):
					name = getattr(item, attrib)
					if name in offset_dic:
						# known string, just get offset
						address = offset_dic[name]
					else:
						# new string, store offset and write zstring
						address = stream.tell()
						self.strings.append(name)
						offset_dic[name] = address
						stream.write_zstring(name)
					# store offset on item
					item.offset = address
			# get the actual result buffer
			buffer_bytes = stream.getvalue()

		self.data = buffer_bytes + get_padding(len(buffer_bytes), alignment=8)

	def __repr__(self):
		return str(self.strings)
