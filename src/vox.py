import vox_parser, os

class Vox(object):

    """Container for a MagicaVoxel object."""

    def __init__(self, file_path):
        """Constructs a voxel object from a .vox file.
        
        Keyword Arguments:
        file_path -- path to the .vox file
        """

        if file_path is None or \
                os.path.splitext(file_path)[1] != ".vox" or \
                os.path.splitext(file_path)[0] == "":
            raise ValueError('Invalid file path.')
        vox_dict = vox_parser.read_vox(file_path)
        self.__dimensions = vox_dict['MAIN']['SIZE']['dimensions']
        self.__voxels = vox_dict['MAIN']['XYZI']['voxels']
        self.__palette = vox_dict['MAIN']['RGBA']['paletteId']
    
    def get_rgba(self, vox_index):
        return self.__palette[self.__voxels[vox_index][3] - 1]
    
    def get_palette_id(self, index):
        return self.__voxels[index][3]
    
    def voxel(self, index):
        return self.__voxels[index]
    
    @property
    def voxels(self):
        return self.__voxels
    
    @property
    def coords(self):
        return [(c[0], c[1], c[2]) for c in self.__voxels]
    
    @property
    def xs(self):
        return [c[0] for c in self.__voxels]
    
    @property
    def ys(self):
        return [c[1] for c in self.__voxels]
    
    @property
    def zs(self):
        return [c[2] for c in self.__voxels]
    
    @property
    def color_indices(self):
        return [c[3] for c in self.__voxels]
    
    @property
    def count(self):
        return len(self.__voxels)
    
    @property
    def size(self):
        return self.__dimensions[0] * self.__dimensions[1] * self.__dimensions[2]


if __name__ == '__main__':
    pass





