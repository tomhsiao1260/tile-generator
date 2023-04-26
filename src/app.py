import math
import sys
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

class TexturedTileBuilder():

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

        name = sys.argv[1]
        value = sys.argv[2]

        transform = trans_build(name)
        transform = transform.transpose()
        transform = transform.flatten('F')

        bt = BatchTable()
        bt.add_property_from_array("color", value)

        glTF = GlTF.from_binary_arrays(arrays, transform, textureUri='squaretexture.jpg')
        t = B3dm.from_glTF(glTF, bt)

        t.to_array()
        t.save_as(f"../output/{name}.b3dm")

if __name__ == '__main__':
    builder = TexturedTileBuilder()
    builder.test_build()
