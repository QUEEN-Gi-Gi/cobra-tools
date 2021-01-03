import time
import numpy as np
import os
from generated.array import Array
from generated.formats.ovl.versions import *
from generated.formats.voxelskirt.compound.Data import Data
from generated.formats.voxelskirt.compound.Header import Header
# from generated.formats.ovl import *
from generated.formats.voxelskirt.compound.Material import Material
from generated.formats.voxelskirt.compound.PosInfo import PosInfo
from generated.formats.voxelskirt.compound.Size import Size
from generated.io import IoFile, BinaryStream
from modules.formats.shared import get_padding_size, get_padding


class VoxelskirtFile(Header, IoFile):

	def __init__(self, ):
		super().__init__()

	def name_items(self, array):
		for item in array:
			item.name = self.names[item.id]

	def load(self, filepath):
		start_time = time.time()
		self.filepath = filepath
		self.basename = os.path.basename(self.filepath)
		print(f"Loading {self.basename}...")

		with self.reader(filepath) as stream:
			self.read(stream)
			self.eoh = stream.tell()
			print(self)
			# print(self.eoh)

			stream.seek(self.eoh + self.info.name_buffer_offset)
			name_offsets = stream.read_uint64s((self.info.name_count,))
			self.names = []
			for offset in name_offsets:
				stream.seek(int(self.eoh + offset))
				self.names.append(stream.read_zstring())

			stream.seek(self.eoh + self.info.data_offset)
			self.datas = stream.read_types(Data, (), (self.info.data_count,))

			stream.seek(self.eoh + self.info.size_offset)
			self.sizes = stream.read_types(Size, (), (self.info.size_count,))

			stream.seek(self.eoh + self.info.position_offset)
			self.positions = stream.read_types(PosInfo, (), (self.info.position_count,))

			stream.seek(self.eoh + self.info.mat_offset)
			self.materials = stream.read_types(Material, (), (self.info.mat_count,))

			# assign names...
			for s in (self.datas, self.sizes, self.positions, self.materials):
				self.name_items(s)
			print(self.sizes)

			for data in self.datas:
				stream.seek(self.eoh + data.offset)
				if data.type == 0:
					data.im = stream.read_ubytes((self.info.x, self.info.y))
				elif data.type == 2:
					data.im = stream.read_floats((self.info.x, self.info.y))

			for pos in self.positions:
				stream.seek(self.eoh + pos.offset)
				# X, Z, Y, Euler Z rot
				pos.locs = stream.read_floats((pos.count, 4))

			for mat in self.materials:
				stream.seek(self.eoh + mat.offset)
				# 4 floats, could be a bounding sphere
				mat.locs = stream.read_floats((mat.count, 4))

			# read PC style height map and masks
			if self.info.height_array_size_pc:
				stream.seek(self.eoh)
				# same as the other games
				self.heightmap = stream.read_floats((self.info.x, self.info.y))
				# the same pixel of each layer is stored in 4 consecutive bytes
				self.weights = stream.read_ubytes((self.info.x, self.info.y, 4))

		print(f"Loaded {self.basename} in {time.time()-start_time:.2f} seconds!")

	def extract(self, ):
		"""Stores the embedded height map and masks as separate images, lossless."""
		start_time = time.time()
		import imageio
		bare_name = os.path.splitext(self.filepath)[0]
		if is_pc(self):
			imageio.imwrite(f"{bare_name}_height.tiff", self.heightmap)
			for i in range(4):
				imageio.imwrite(f"{bare_name}_mask{i}.png", self.weights[:, :, i], compress_level=2)
		else:
			for data in self.datas:
				if data.type == 0:
					imageio.imwrite(f"{bare_name}_{data.name}.png", data.im, compress_level=2)
				elif data.type == 2:
					imageio.imwrite(f"{bare_name}_{data.name}.tiff", data.im)
		print(f"Extracted maps from {self.basename} in {time.time()-start_time:.2f} seconds!")

	def update_names(self, list_of_arrays):
		self.names = []
		for s in list_of_arrays:
			for item in s:
				if item.name not in self.names:
					self.names.append(item.name)
				item.id = self.names.index(item.name)

	def save(self, filepath):
		start_time = time.time()
		self.basename = os.path.basename(self.filepath)
		print(f"Saving {self.basename}...")

		# update data
		self.update_names((self.datas, self.sizes, self.positions, self.materials))
		if is_pc(self):
			self.info.height_array_size_pc = self.info.x * self.info.y * 4

		# write the buffer data to a temporary stream
		with BinaryStream() as stream:
			# write the images
			if is_pc(self):
				stream.write_floats(self.heightmap)
				stream.write_ubytes(self.weights)
			else:
				# PC and JWE store the images attached to data infos
				for data in self.datas:
					data.offset = stream.tell()
					if data.type == 0:
						stream.write_ubytes(data.im)
					elif data.type == 2:
						stream.write_floats(data.im)

			self.info.data_offset = stream.tell()
			self.info.data_count = len(self.datas)
			stream.write_types(self.datas)

			self.info.size_offset = stream.tell()
			self.info.size_count = len(self.sizes)
			# todo - need to update this??
			stream.write_types(self.sizes)

			# write object positions
			for pos in self.positions:
				pos.offset = stream.tell()
				stream.write_floats(pos.locs)
			self.info.position_offset = stream.tell()
			self.info.position_count = len(self.positions)
			stream.write_types(self.positions)

			# write 'materials' / bbox / whatever
			for mat in self.materials:
				mat.offset = stream.tell()
				stream.write_floats(mat.locs)
			self.info.material_offset = stream.tell()
			self.info.material_count = len(self.materials)
			stream.write_types(self.materials)

			# write names
			name_addresses = []
			name_start = stream.tell()
			for name in self.names:
				name_addresses.append(stream.tell())
				stream.write_zstring(name)
			# pad name section
			stream.write(get_padding(stream.tell() - name_start, alignment=8))
			stream.write_uint64s(name_addresses)
			# get the actual result buffer
			buffer_bytes = stream.getvalue()

		# write the actual file
		with self.writer(filepath) as stream:
			self.write(stream)
			stream.write(buffer_bytes)
		print(f"Saved {self.basename} in {time.time()-start_time:.2f} seconds!")


if __name__ == "__main__":
	import matplotlib
	import matplotlib.pyplot as plt
	m = VoxelskirtFile()
	# files = ("C:/Users/arnfi/Desktop/deciduousskirt.voxelskirt",
	# 		  "C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",
	# 		  "C:/Users/arnfi/Desktop/nublar.voxelskirt",
	# 		   "C:/Users/arnfi/Desktop/savannahskirt.voxelskirt")
	# files = ("C:/Users/arnfi/Desktop/savannahskirt.voxelskirt",)
	# files = ("C:/Users/arnfi/Desktop/nublar.voxelskirt",)
	files = ("C:/Users/arnfi/Desktop/alpineskirt.voxelskirt",)
	for f in files:
		# print(f)
		m.load(f)
		m.extract()
		m.positions[0].name = "TestObject"
		m.save(f+"2")
		#
		# fig, ax = plt.subplots()
		# # ax.imshow(m.rest)
		# # ax.imshow(m.weights.reshape((m.info.x, m.info.y, 4))[:,:,1])
		# # ax.plot(m.rest[:,:1], "o")
		# # ax.scatter(m.rest[:,:1], m.rest[:,2])
		# ax.scatter(m.positions[:,0], m.positions[:,2], m.positions[:,3]*20)
		# # x, z, y,
		#
		# # ax.set(xlabel='time (s)', ylabel='voltage (mV)',
		# # 	   title='About as simple as it gets, folks')
		# # ax.grid()
		#
		# fig.savefig("test.png")
		# plt.show()