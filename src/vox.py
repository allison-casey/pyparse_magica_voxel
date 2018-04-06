import vox_parser, os
import numpy as np

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
        self.__voxels = np.array(vox_dict['MAIN']['XYZI']['voxels'])
        self.__palette = np.array(vox_dict['MAIN']['RGBA']['paletteId'])
    
    def get_rgb(self, vox_index):
        return self.__palette[self.__voxels[vox_index][3] - 1]

    def get_palette_id(self, index):
        return self.__voxels[index][3]

    def voxel(self, index):
        return self.__voxels[index]

    @property
    def get_voxels(self):
        return self.__voxels

    @property
    def coords(self):
        return self.__voxels[:,0:3]

    @property
    def xs(self):
        return self.__voxels[:,0]

    @property
    def ys(self):
        return self.__voxels[:,1]

    @property
    def zs(self):
        return self.__voxels[:,2]
    
    @property
    def color_indices(self):
        return self.__voxels[:,3]
    
    @property
    def count(self):
        return self.__voxels.shape[0]

    @property
    def size(self):
        return self.__dimensions[0] * self.__dimensions[1] * self.__dimensions[2]


if __name__ == '__main__':
    pass
