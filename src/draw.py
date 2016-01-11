import itertools
from time import process_time

import noise
import numpy as np
from vispy import app
from vispy import gloo

import cellular_automata as ca
from tiles import resource, fort

start = process_time()
events = [start]
c = app.Canvas(keys='interactive')

vertex_shader = """
attribute vec2 a_position;
attribute vec4 a_colour;
out vec4 colour;
void main (void)
{
    gl_Position = vec4(a_position, 0.0, 1.0);
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
print("Gloo Setup {}s, {}s total".format(str(events[-1]-events[-2]), str(events[-1]-start)))
start = process_time()
program = gloo.Program(vertex_shader, fragment_shader)
map_vertices = []
map_colours = []

events.append(process_time())
print("Start Map {}s, {}s total".format(str(events[-1]-events[-2]), str(events[-1]-start)))
m = ca.CAMap(100, 100).init(0.45).mutate(5, 0, True, 4).mutate(5, -1, True, 2)
m = resource.add_resources(m)
m = fort.add_forts(m)
events.append(process_time())
print("End Map {}s, {}s total".format(str(events[-1]-events[-2]), str(events[-1]-start)))

offset = max(m.width, m.height) / 2.0
step = 1.0 / offset

events.append(process_time())
print("Start Vertex Construction {}s, {}s total".format(str(events[-1]-events[-2]), str(events[-1]-start)))
for x, y in itertools.product(range(m.width), range(m.height)):
    if m.get(x, y).draw_me:
        colour = m.get(x, y).colour
        map_vertices.append(tuple((x, y)))
        map_colours.append(colour)
        map_vertices.append(tuple((x, y + 1)))
        map_colours.append(colour)
        map_vertices.append(tuple((x + 1, y)))
        map_colours.append(colour)

        map_vertices.append(tuple((x + 1, y + 1)))
        map_colours.append(colour)
        map_vertices.append(tuple((x, y + 1)))
        map_colours.append(colour)
        map_vertices.append(tuple((x + 1, y)))
        map_colours.append(colour)

events.append(process_time())
print("End Vertex Construction {}s, {}s total".format(str(events[-1]-events[-2]), str(events[-1]-start)))

program['a_position'] = np.array(
        [tuple(((v[0] - offset) * step, (v[1] - offset) * step)) for v in map_vertices]).astype(np.float32)

program['a_colour'] = np.array(map_colours).astype(np.float32)


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
print("Run All The Things {}s, {}s total".format(str(events[-1]-events[-2]), str(events[-1]-start)))

def make_noise():
    vertices_data = []
    colours_data = []
    size = 200
    seed = 5
    octaves = 5
    for x, y in itertools.product(range(size * 2), range(size * 2)):
        vertices_data.append(tuple((x, y)))
        colours_data.append(noise.snoise3(seed, x, y, octaves))
        vertices_data.append(tuple((x, y + 1)))
        colours_data.append(noise.snoise3(seed, x, y + 1, octaves))
        vertices_data.append(tuple((x + 1, y)))
        colours_data.append(noise.snoise3(seed, x + 1, y, octaves))

        vertices_data.append(tuple((x + 1, y + 1)))
        colours_data.append(noise.snoise3(seed, x + 1, y + 1, octaves))
        vertices_data.append(tuple((x + 1, y)))
        colours_data.append(noise.snoise3(seed, x + 1, y, octaves))
        vertices_data.append(tuple((x, y + 1)))
        colours_data.append(noise.snoise3(seed, x, y + 1, octaves))

    vertices = np.array([tuple(((v[0] - size) / size, (v[1] - size) / size)) for v in vertices_data]).astype(np.float32)
    colours = np.array(colours_data).astype(np.float32)
