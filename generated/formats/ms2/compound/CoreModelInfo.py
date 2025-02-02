import numpy
import typing
from generated.array import Array
from generated.formats.ms2.compound.Vector3 import Vector3


class CoreModelInfo:

	"""
	Used by ms2 or in Mdl2ModelInfo
	In load order it always defines the variable fragments for the next mdl2
	The mdl2's fragment informs the first mdl2
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3()

		# not sure
		self.unk_float_a = 0

		# the biggest coordinates across all axes
		self.bounds_max = Vector3()

		# scale: pack_offset / 512, also added as offset
		self.pack_offset = 0

		# cog? medium of bounds?
		self.center = Vector3()

		# probably from center to max
		self.radius = 0

		# PZ only, zero-ish
		self.unknowns = numpy.zeros((4), dtype='float')

		# verbatim repeat
		self.bounds_min_repeat = Vector3()

		# verbatim repeat
		self.bounds_max_repeat = Vector3()
		self.num_materials = 0
		self.num_lods = 0
		self.num_objects = 0

		# count of modeldata fragments for the mdl2 this struct refers to
		self.num_models = 0

		# ?
		self.last_count = 0

		# nonzero in PZ flamingo, ZT african ele female
		self.another_count = 0

		# ?
		self.unks = numpy.zeros((7), dtype='ushort')
		self.pad = numpy.zeros((3), dtype='ushort')

	def read(self, stream):

		self.io_start = stream.tell()
		self.bounds_min = stream.read_type(Vector3)
		if not (stream.version < 19):
			self.unk_float_a = stream.read_float()
		self.bounds_max = stream.read_type(Vector3)
		if not (stream.version < 19):
			self.pack_offset = stream.read_float()
		self.center = stream.read_type(Vector3)
		self.radius = stream.read_float()
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			self.unknowns = stream.read_floats((4))
		if not (stream.version == 17):
			self.bounds_min_repeat = stream.read_type(Vector3)
			self.bounds_max_repeat = stream.read_type(Vector3)
		self.num_materials = stream.read_ushort()
		self.num_lods = stream.read_ushort()
		self.num_objects = stream.read_ushort()
		self.num_models = stream.read_ushort()
		self.last_count = stream.read_ushort()
		self.another_count = stream.read_ushort()
		self.unks = stream.read_ushorts((7))
		self.pad = stream.read_ushorts((3))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.bounds_min)
		if not (stream.version < 19):
			stream.write_float(self.unk_float_a)
		stream.write_type(self.bounds_max)
		if not (stream.version < 19):
			stream.write_float(self.pack_offset)
		stream.write_type(self.center)
		stream.write_float(self.radius)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version == 19):
			stream.write_floats(self.unknowns)
		if not (stream.version == 17):
			stream.write_type(self.bounds_min_repeat)
			stream.write_type(self.bounds_max_repeat)
		stream.write_ushort(self.num_materials)
		stream.write_ushort(self.num_lods)
		stream.write_ushort(self.num_objects)
		stream.write_ushort(self.num_models)
		stream.write_ushort(self.last_count)
		stream.write_ushort(self.another_count)
		stream.write_ushorts(self.unks)
		stream.write_ushorts(self.pad)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'CoreModelInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* bounds_min = {self.bounds_min.__repr__()}'
		s += f'\n	* unk_float_a = {self.unk_float_a.__repr__()}'
		s += f'\n	* bounds_max = {self.bounds_max.__repr__()}'
		s += f'\n	* pack_offset = {self.pack_offset.__repr__()}'
		s += f'\n	* center = {self.center.__repr__()}'
		s += f'\n	* radius = {self.radius.__repr__()}'
		s += f'\n	* unknowns = {self.unknowns.__repr__()}'
		s += f'\n	* bounds_min_repeat = {self.bounds_min_repeat.__repr__()}'
		s += f'\n	* bounds_max_repeat = {self.bounds_max_repeat.__repr__()}'
		s += f'\n	* num_materials = {self.num_materials.__repr__()}'
		s += f'\n	* num_lods = {self.num_lods.__repr__()}'
		s += f'\n	* num_objects = {self.num_objects.__repr__()}'
		s += f'\n	* num_models = {self.num_models.__repr__()}'
		s += f'\n	* last_count = {self.last_count.__repr__()}'
		s += f'\n	* another_count = {self.another_count.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
