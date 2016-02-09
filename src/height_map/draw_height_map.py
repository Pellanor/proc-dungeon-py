import itertools
from time import process_time

import math
import numpy as np
from vispy import app
from vispy import gloo
from vispy.util.transforms import perspective, ortho

import height_map.terrain as terrain


def look_at(camera_pos, target_pos, up_vector):
    forward_ved = normalized(target_pos - camera_pos)
    right_vec = normalized(np.cross(up_vector, forward_ved))
    up_vec = np.cross(forward_ved, right_vec)

    M = np.matrix([
        [right_vec[0], up_vec[0], forward_ved[0], 0],
        [right_vec[1], up_vec[1], forward_ved[1], 0],
        [right_vec[2], up_vec[2], forward_ved[2], 0],
        [-np.dot(right_vec, camera_pos), -np.dot(up_vec, camera_pos), -np.dot(forward_ved, camera_pos), 1]
    ], dtype=np.float32)
    return M


def normalized(a):
    return a / math.sqrt(np.square(a).sum())


start = process_time()
events = [start]
c = app.Canvas(keys='interactive')

vertex_shader = """
attribute vec3 a_position;
attribute vec4 a_colour;
uniform mat4 a_transform;
out vec4 colour;
void main (void)
{
    gl_Position = vec4(a_position, 1.0) * a_transform;
    colour = a_colour;
}
"""

fragment_shader = """
in vec4 colour;
out vec4 frag_colour;
void main()
{
    frag_colour = colour;
}
"""

events.append(process_time())
print("Gloo Setup {}s, {}s total".format(str(events[-1] - events[-2]), str(events[-1] - start)))
start = process_time()
program = gloo.Program(vertex_shader, fragment_shader)
map_vertices = []
map_colours = []

events.append(process_time())
print("Start Map {}s, {}s total".format(str(events[-1] - events[-2]), str(events[-1] - start)))
hm = terrain.make_noise_height_map(500, 500, 0, 7)
events.append(process_time())
print("End Map {}s, {}s total".format(str(events[-1] - events[-2]), str(events[-1] - start)))

offset = max(hm.width, hm.height) / 2.0
step = 1.0 / offset

events.append(process_time())
print("Start Vertex Construction {}s, {}s total".format(str(events[-1] - events[-2]), str(events[-1] - start)))
for x, y in itertools.product(range(hm.width - 1), range(hm.height - 1)):
    colour = [0.0, 1 - hm.get(x, y), hm.get(x, y), 0.0]
    map_vertices.append(tuple((x, y, hm.get(x, y))))
    map_colours.append(colour)
    map_vertices.append(tuple((x, y + 1, hm.get(x, y + 1))))
    map_colours.append(colour)
    map_vertices.append(tuple((x + 1, y, hm.get(x + 1, y))))
    map_colours.append(colour)

    map_vertices.append(tuple((x + 1, y + 1, hm.get(x + 1, y + 1))))
    map_colours.append(colour)
    map_vertices.append(tuple((x, y + 1, hm.get(x, y + 1))))
    map_colours.append(colour)
    map_vertices.append(tuple((x + 1, y, hm.get(x + 1, y))))
    map_colours.append(colour)

events.append(process_time())
print("End Vertex Construction {}s, {}s total".format(str(events[-1] - events[-2]), str(events[-1] - start)))

program['a_position'] = np.array(
    [tuple(((v[0] - offset) * step, (v[1] - offset) * step, v[2] * 0.2)) for v in map_vertices]).astype(np.float32)

program['a_colour'] = np.array(map_colours).astype(np.float32)

m_look_at = look_at(np.array([0, 2, 1]).astype(np.float32),
                    np.array([0, 0, 0]).astype(np.float32),
                    np.array([1, 0, 0]).astype(np.float32))

m_projection = perspective(45.0, hm.width / float(hm.height), -1.0, 100.0)

program['a_transform'] = m_look_at
# program['a_transform'] = ortho(offset/10, -offset/10, -offset/10, offset/10, 1.0, -1.0)


print(program.variables)


@c.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)


@c.connect
def on_draw(event):
    gloo.clear((1, 1, 1, 1))
    program.draw('triangles')


c.show()
app.run()

events.append(process_time())
print("Run All The Things {}s, {}s total".format(str(events[-1] - events[-2]), str(events[-1] - start)))
