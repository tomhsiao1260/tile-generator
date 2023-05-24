import os
import shutil
import math
import json
import numpy as np

from cube import Cube
from gltf import GlTF
from b3dm import B3dm
from batch_table import BatchTable

depth = 2
cube_size = 10

OUTPUT_DIR = '../output/'
CLIENT_DIR = '../client/static/'

JSON_DIR = os.path.join(OUTPUT_DIR, 'tileset.json')

class TileBuilder():

    def __init__(self):
        self.cube_arrays = self.get_cube_arrays()
        self.tileset = self.get_init_tileset()

    @staticmethod
    def get_cube_arrays():
        cube = Cube()

        positions = cube.getPositionArray()
        normals = cube.getNormalArray()
        uvs = cube.getUVArray()
        box = cube.getBoxArray()

        return [{
            'position': positions,
            'normal': normals,
            'uv': uvs,
            'bbox': box
        }]
    
    @staticmethod
    def get_init_tileset():
        tileset = {}
        tileset['asset'] = { 'version': '0.0' }
        tileset['transform'] = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]
        tileset['root'] = {}

        return tileset
    
    @staticmethod
    def shift_table(index):
        if (index == 0): return [ 1,  1,  1]
        if (index == 1): return [ 1,  1, -1]
        if (index == 2): return [ 1, -1,  1]
        if (index == 3): return [ 1, -1, -1]
        if (index == 4): return [-1,  1,  1]
        if (index == 5): return [-1,  1, -1]
        if (index == 6): return [-1, -1,  1]
        if (index == 7): return [-1, -1, -1]

        return [0, 0, 0]

    def build_single_b3dm(self, id, shift, scale, value):
        arrays = self.cube_arrays
    
        transform = np.array([
            [    scale,        0,        0,     0 ],
            [        0,    scale,        0,     0 ],
            [        0,        0,    scale,     0 ],
            [ shift[0], shift[1], shift[2], scale ]], dtype=float).transpose().flatten('F')

        bt = BatchTable()
        bt.add_property_from_array("intensity", value)

        glTF = GlTF.from_binary_arrays(arrays, transform)
        t = B3dm.from_glTF(glTF, bt)

        t.to_array()
        t.save_as(f"{OUTPUT_DIR}{id}.b3dm")

    @staticmethod
    def build_single_tile(id, shift, half_size, parent):
        child = {}
        child['refine'] = 'REPLACE'
        child['content'] = { 'uri': f'{id}.b3dm' }
    
        if (id == '0'): child['geometricError'] = 0.3
        if (id != '0'): child['geometricError'] = parent['geometricError'] / 1.41421

        child['boundingVolume'] = {
            'box': [
                shift[0],    shift[1],   shift[2],
                half_size,        0.0,        0.0,
                0.0,        half_size,        0.0,
                0.0,              0.0,   half_size
            ]
        }
        child['children'] = []

        if (id == '0'): parent['root'] = child
        if (id != '0'): parent['children'].append(child)          

    def build_b3dm_and_tile(self, tile_endpoint, data, depth):
        if (depth > 0):
            st = int(math.pow(2, depth - 1))
            parent_id = tile_endpoint['content']['uri'].replace('.b3dm', '')
            parent_shift = tile_endpoint['boundingVolume']['box'][0:3]
            parent_half_size = tile_endpoint['boundingVolume']['box'][3]
            current_half_size = parent_half_size / 2

            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        ind = 4 * x + 2 * y + 1 * z
                        delta = [ v * current_half_size for v in self.shift_table(ind) ]
                        data_slice = data[st*x:st*(x+1), st*y:st*(y+1), st*z:st*(z+1)]

                        current_id = f'{parent_id}{ind}'
                        current_shift = [ p_sh + delta[i] for i, p_sh in enumerate(parent_shift)]
                        current_value = np.mean(data_slice)

                        self.build_single_b3dm(current_id, current_shift, current_half_size * 0.9, current_value)
                        self.build_single_tile(current_id, current_shift, current_half_size * 1.0, tile_endpoint)

                        self.build_b3dm_and_tile(tile_endpoint['children'][ind], data_slice, depth - 1)

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    h = cube_size / 2
    size = int(math.pow(2, depth))
    data = np.zeros((size, size, size))

    for i in range(size):
        for j in range(size):
            for k in range(size):
                data[i][j][k] = (i + j + k) / (3 * size)

    tile = TileBuilder()

    tile.build_single_b3dm('0', [0, 0, 0], h, 0.5)
    tile.build_single_tile('0', [0, 0, 0], h, tile.tileset)

    tile.build_b3dm_and_tile(tile.tileset['root'], data, depth)

    # tile.tileset
    # tile.tileset['root']
    # tile.tileset['root']['children'][i]
    # tile.tileset['root']['children'][i]['children'][j]
    # and so on ...

    json_data = json.dumps(tile.tileset, indent=4, ensure_ascii=False)
    with open(JSON_DIR, 'w') as f:
        f.write(json_data)

    for file in os.listdir(OUTPUT_DIR):
        origin = os.path.join(OUTPUT_DIR, file)
        copy = os.path.join(CLIENT_DIR, file)
        shutil.copy(origin, copy)


