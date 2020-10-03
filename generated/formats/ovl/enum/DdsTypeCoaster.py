from generated.enum import UbyteEnum


class DdsTypeCoaster(UbyteEnum):

	"""
	maps the OVL's dds type to name of compression format
	"""
	DXGI_FORMAT_BC1_UNORM = 97
	DXGI_FORMAT_BC1_UNORM_SRGB = 98
	DXGI_FORMAT_BC2_UNORM = 99
	DXGI_FORMAT_BC2_UNORM_SRGB = 100
	# PZ wolf baldnessscars texture
	DXGI_FORMAT_BC3_UNORM = 101
	DXGI_FORMAT_BC3_UNORM_SRGB = 102
	DXGI_FORMAT_BC4_UNORM = 103
	DXGI_FORMAT_BC4_SNORM = 104
	DXGI_FORMAT_BC5_UNORM = 105
	DXGI_FORMAT_BC5_SNORM = 106
	DXGI_FORMAT_BC7_UNORM = 126
	# PZ titan beetle
	DXGI_FORMAT_BC7_UNORM_SRGB = 127