import binascii, struct, json

def read_vox(file):
    """Parses a .vox file into a dictionary.
    
    Currently can only read SIZE, XYZI, and RGBA.
    TODO: implement parsing of nTRN, nGRP, nSHP, LAYR, MATL, rOBJ

    Keyword arguments:
    file -- name of the .vox file
    """
    if file is None or "":
        raise ValueError('Invalid file input.')

    f = open(file, 'rb')
    # reads a 32 bit int from the file
    def read_int():
        """Reads a 32 bit int from the file"""
        return struct.unpack('i', f.read(4))[0]

    # reads a 4 byte string from the file
    #  def read_str():
    #      """Reads a 4 byte string from the file"""
    #      return struct.unpack('4s', f.read(4))[0]

    def read_str(num_bytes = 4):
        return struct.unpack(str(num_bytes) + 's', f.read(num_bytes))[0]

    # reads a byte from the file
    def read_byte():
        """Reads a single byte from the file"""
        return struct.unpack('b', f.read(1))[0]
    
    def read_ubyte():
        """Reads an unsigned byte from the file"""
        return struct.unpack('B', f.read(1))[0]

    def read_dict():
        dictionary = {}
        for _ in range(read_int()):
            key = read_str(read_int())
            val = read_str(read_int())
            dictionary[key] = val                                   
        return dictionary

    def read_rotation():
        rotation = {}
        rotation['arr'] = read_int()
        rotation['arr'] = bin(rotation['arr'])[2:].rjust(8, '0')
        return rotation
    # read a single chunk from the file
    def read_main():
        """Reads the contents of the MAIN chunk
        into a dictionary along with its content and children
        byte count."""
        chunk = {}
        chunk_id = read_str()
        chunk_content = read_int()
        chunk_children = read_int()

        chunk[chunk_id] = {}
        chunk[chunk_id]['content'] = chunk_content
        chunk[chunk_id]['children'] = chunk_children

        return chunk

    def read_chunk():
        """Reads a single chunk into a dictionary.
        
        currently can only read SIZE, XYZI, and RGBA.
        TODO: implement parsing of nTRN, nGRP, nSHP, LAYR, MATL, rOBJ"""

        # skips the following chunks bcause they do not contain any
        # relevant information for the blueprint_reader
        _SKIP_CHUNKS = ['nSHP', 'LAYR', 'MATL', 'rOBJ']
        
        chunk = {}

        # read in chunk meta-data
        #  chunk['id'] = read_str()
        chunk_id = read_str()
        chunk_content = read_int()
        chunk_children = read_int()
        chunk[chunk_id] = {}
        
        # SIZE contains the dimensions of the model
        if chunk_id == 'SIZE':
            chunk[chunk_id]['dimensions'] = (read_int(), read_int(), read_int())
        # XYZI contains the number of voxels and the (X, Y, Z, colorIndex)
        # for each voxel.
        elif chunk_id == 'XYZI':
            chunk[chunk_id]['numVoxels'] = read_int()
            chunk[chunk_id]['voxels'] = \
                    [(read_byte(), read_byte(), read_byte(), read_byte()) 
                    for _ 
                    in range(chunk[chunk_id]['numVoxels'])]
        # RGBA contains the palette used by the model where each
        # color index is defined by (R, G, B, A). Palette and color
        # index use 1 based indexing (1-255).
        elif chunk_id == 'RGBA':
            chunk[chunk_id]['paletteId'] = \
                    [(read_ubyte(), read_ubyte(), read_ubyte(), read_ubyte()) 
                    for _ 
                    in range(256)]
        elif chunk_id == 'nTRN':
            transform_node = decoded_vox['MAIN'][chunk_id] \
                    if chunk_id in decoded_vox['MAIN'] else {}

            node_id = read_int()
            transform_node[node_id] = {}
            transform_node[node_id]['nodeAttributes'] = read_dict()
            transform_node[node_id]['childNodeId'] = read_int()
            transform_node[node_id]['reservedId'] = read_int()
            transform_node[node_id]['layerId'] = read_int()
            transform_node[node_id]['num_frames'] = read_int()
            transform_node[node_id]['frames'] = []

            for _ in range(transform_node[node_id]['num_frames']):
                transform_node[node_id]['frames'].append(read_dict())
            chunk[chunk_id] = transform_node
        
        elif chunk_id == 'nGRP':
            group_node = decoded_vox['MAIN'][chunk_id] \
                    if chunk_id in decoded_vox['MAIN'] else {}
            
            node_id = read_int()
            group_node[node_id] = {}
            group_node[node_id]['nodeAttributes'] = read_dict()
            group_node[node_id]['childIds'] = []
            for _ in range(read_int()):
                group_node[node_id]['childIds'].append(read_int())
            chunk[chunk_id] = group_node

        # Skip unimplemented chunks
        elif chunk_id in _SKIP_CHUNKS:
            f.read(chunk_content + chunk_children)
        return chunk

    
    decoded_vox = {}
    # read model meta-deta
    decoded_vox['Magica'] = read_str()
    decoded_vox['version'] = read_int()
    # read root chunk MAIN
    decoded_vox.update(read_main()) 
    # read child chunks
    while f.tell() <= decoded_vox['MAIN']['children']:
        decoded_vox['MAIN'].update(read_chunk())

    return decoded_vox

def convert_to_json(file_in, file_out):
    """Converts a .vox file to a .json file.

    Keyword Arguments:
    file_in -- Path of input file
    file_out -- Path of output file    
    """
    if file_in is None or "":
        raise ValueError('Invalid file input.')
    if file_out is None or "":
        raise ValueError('Invalid file output.')

    with open(file_out, 'w') as out:
        json.dump(read_vox(file_in), out, indent=4)

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    v1 = read_vox('../vox/3x3x3.vox')
    pp.pprint(v1)















