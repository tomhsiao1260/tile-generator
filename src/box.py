import numpy as np

class TriangleSoup:
    def __init__(self):
        self.verticeArray = [
            [
                np.array([-5., -5., -5.], dtype=np.float32),
                np.array([-5., 5., -5.], dtype=np.float32),
                np.array([5., -5., -5.], dtype=np.float32),
            ],
            [
                np.array([5., 5., -5.], dtype=np.float32),
                np.array([5., -5., -5.], dtype=np.float32),
                np.array([-5., 5., -5.], dtype=np.float32),
            ],
            [
                np.array([-5., -5., -5.], dtype=np.float32),
                np.array([-5., -5., 5.], dtype=np.float32),
                np.array([-5., 5., -5.], dtype=np.float32),
            ],
            [
                np.array([-5., 5., 5.], dtype=np.float32),
                np.array([-5., 5., -5.], dtype=np.float32),
                np.array([-5., -5., 5.], dtype=np.float32),
            ],
            [
                np.array([-5., 5., -5.], dtype=np.float32),
                np.array([-5., 5., 5.], dtype=np.float32),
                np.array([5., 5., -5.], dtype=np.float32),
            ],
            [
                np.array([5., 5., -5.], dtype=np.float32),
                np.array([-5., 5., 5.], dtype=np.float32),
                np.array([5., 5., 5.], dtype=np.float32),
            ], #
            [
                np.array([5., 5., 5.], dtype=np.float32),
                np.array([-5., 5., 5.], dtype=np.float32),
                np.array([5., -5., 5.], dtype=np.float32),
            ],
            [
                np.array([-5., -5., 5.], dtype=np.float32),
                np.array([5., -5., 5.], dtype=np.float32),
                np.array([-5., 5., 5.], dtype=np.float32),
            ],
            [
                np.array([5., 5., 5.], dtype=np.float32),
                np.array([5., -5., 5.], dtype=np.float32),
                np.array([5., 5., -5.], dtype=np.float32),
            ],
            [
                np.array([5., -5., -5.], dtype=np.float32),
                np.array([5., 5., -5.], dtype=np.float32),
                np.array([5., -5., 5.], dtype=np.float32),
            ],
            [
                np.array([5., -5., 5.], dtype=np.float32),
                np.array([-5., -5., 5.], dtype=np.float32),
                np.array([5., -5., -5.], dtype=np.float32),
            ],
            [
                np.array([-5., -5., 5.], dtype=np.float32),
                np.array([-5., -5., -5.], dtype=np.float32),
                np.array([5., -5., -5.], dtype=np.float32),
            ],
        ]

        self.uvArray = [
            [
                np.array([0., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
            ],
            [
                np.array([1., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
            ],
            [
                np.array([0., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
            ],
            [
                np.array([1., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
            ],
            [
                np.array([0., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
            ],
            [
                np.array([1., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
            ],#
            [
                np.array([0., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
            ],
            [
                np.array([1., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
            ],
            [
                np.array([0., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
            ],
            [
                np.array([1., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
            ],
            [
                np.array([0., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
            ],
            [
                np.array([1., 1.], dtype=np.float32),
                np.array([1., 0.], dtype=np.float32),
                np.array([0., 1.], dtype=np.float32),
            ],
        ]

    def getPositionArray(self):
        verticeTriangles = self.verticeArray
        verticeArray = vertexAttributeToArray(verticeTriangles)

        return b''.join(verticeArray)

    def getDataArray(self):
        verticeTriangles = self.uvArray
        verticeArray = vertexAttributeToArray(verticeTriangles)
        return b''.join(verticeArray)

    def getNormalArray(self):
        normals = []
        for t in self.verticeArray:
            U = t[1] - t[0]
            V = t[2] - t[0]
            N = np.cross(U, V)
            norm = np.linalg.norm(N)
            if norm == 0:
                normals.append(np.array([0, 0, 1], dtype=np.float32))
            else:
                normals.append(N / norm)

        verticeArray = faceAttributeToArray(normals)
        return b''.join(verticeArray)


def faceAttributeToArray(triangles):
    array = []
    for face in triangles:
        array += [face, face, face]
    return array


def vertexAttributeToArray(triangles):
    array = []
    for face in triangles:
        for vertex in face:
            array.append(vertex)
    return array
