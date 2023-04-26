import math
import json
import numpy as np

from gltf import GlTF
from b3dm import B3dm
from box import TriangleSoup
from batch_table import BatchTable

def shift_partial(num):
    if num == '0': return [ 1,  1,  1]
    if num == '1': return [ 1,  1, -1]
    if num == '2': return [ 1, -1,  1]
    if num == '3': return [ 1, -1, -1]
    if num == '4': return [-1,  1,  1]
    if num == '5': return [-1,  1, -1]
    if num == '6': return [-1, -1,  1]
    if num == '7': return [-1, -1, -1]

    return [0, 0, 0]

def shift_total(name):
    shift = [0, 0, 0]

    for i, v in enumerate(name):
        if (i == 0): continue

        factor = 10 / 2 * math.pow(2, -i)
        shift[0] += shift_partial(v)[0] * factor
        shift[1] += shift_partial(v)[1] * factor
        shift[2] += shift_partial(v)[2] * factor

    return shift

def trans_build(name):
    level = len(name) - 1
    scale = math.pow(2, -level)
    shift = shift_total(name)

    transform = np.array([
        [   scale,        0,        0,     0],
        [       0,    scale,        0,     0],
        [       0,        0,    scale,     0],
        [shift[0], shift[1], shift[2], scale]], dtype=float)

    return transform

def build_tile(name):
    level = len(name) - 1

    data = {}
    data['refine'] = "REPLACE"
    data['geometricError'] = 0.2 * math.pow(1.41421, -level)
    data['content'] = { "uri": f"{name}.b3dm" }

    size = 10.0 * math.pow(2, -level)
    shift = shift_total(name)

    data['boundingVolume'] = {
      "box": [
        shift[0], shift[1], shift[2],
        size/2,        0.0,      0.0,
        0.0,        size/2,      0.0,
        0.0,           0.0,    size/2
      ]
    }
    data['children'] = []

    return data

class TexturedTileBuilder():

    def b3dm_build(name, arrays, value):
        transform = trans_build(name)
        transform = transform.transpose()
        transform = transform.flatten('F')

        bt = BatchTable()
        bt.add_property_from_array("color", value)

        glTF = GlTF.from_binary_arrays(arrays, transform, textureUri='squaretexture.jpg')
        t = B3dm.from_glTF(glTF, bt)

        t.to_array()
        t.save_as(f"../output/{name}.b3dm")

    def test_build(self):
        ts = TriangleSoup()
        positions = ts.getPositionArray()
        normals = ts.getNormalArray()
        uvs = ts.getDataArray()
        box = [[0, 0, 0],
               [10, 10, 10]]

        arrays = [{
            'position': positions,
            'normal': normals,
            'uv': uvs,
            'bbox': box
        }]

        data = np.zeros((2, 2, 2))

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                for k in range(data.shape[2]):
                    data[i][j][k] = (i + j + k) / 3

        tileset = {}
        tileset['asset'] = { 'version': "0.0" }
        tileset['transform'] = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]

        depth = int(math.log(data.shape[0], 2)) + 1
        depth = 4
    
        for i in range(depth):
            if (i == 0):
                tileset['root'] = build_tile('0')
            if (i == 1):
                for j in range(8):
                    tileset['root']['children'].append(build_tile(f'0{j}'))
            if (i == 2):
                for j in range(8):
                    for k in range(8):
                        tileset['root']['children'][j]['children'].append(build_tile(f'0{j}{k}'))
            if (i == 3):
                for j in range(8):
                    for k in range(8):
                        for l in range(8):
                            tileset['root']['children'][j]['children'][k]['children'].append(build_tile(f'0{j}{k}{l}'))

        json_data = json.dumps(tileset, indent=4, ensure_ascii=False)

        with open('../output/tileset.json', 'w') as f:
            f.write(json_data)

        for i in range(depth):
            if ((depth-i) == 1):
                TexturedTileBuilder.b3dm_build('0', arrays, 0.5)
            if ((depth-i) == 2):
                for j in range(8):
                    TexturedTileBuilder.b3dm_build(f'0{j}', arrays, j / 7)
            if ((depth-i) == 3):
                for j in range(8):
                    for k in range(8):
                        TexturedTileBuilder.b3dm_build(f'0{j}{k}', arrays, k / 7)
            if ((depth-i) == 4):
                for j in range(8):
                    for k in range(8):
                        for l in range(8):
                            TexturedTileBuilder.b3dm_build(f'0{j}{k}{l}', arrays, l / 7)

if __name__ == '__main__':
    builder = TexturedTileBuilder()
    builder.test_build()
