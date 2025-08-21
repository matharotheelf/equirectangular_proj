import moderngl
import numpy as np
# from pyrr import Matrix44
import pygame
from pygame.locals import DOUBLEBUF, OPENGL

# Initialize Pygame and OpenGL context
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
pygame.display.set_mode((800, 600), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

ctx = moderngl.create_context()

# Generate a grid of vertices
grid_size = 50  # Number of points along one axis
vertices = []
indices = []

for y in range(grid_size):
    for x in range(grid_size):
        # Normalized coordinates in range [-1, 1]
        vertices.append(((x / (grid_size - 1)) * 2 - 1, (y / (grid_size - 1)) * 2 - 1))

        # Create indices for two triangles forming a square
        if x < grid_size - 1 and y < grid_size - 1:
            i = y * grid_size + x
            indices.extend([i, i + 1, i + grid_size, i + 1, i + grid_size, i + grid_size + 1])

vertices = np.array(vertices, dtype='f4')  # Convert to NumPy array
indices = np.array(indices, dtype='i4')   # Convert to NumPy array

# Create shaders
vertex_shader = ctx.program(
    vertex_shader='''
    #version 330

    in vec2 in_position;

    uniform float time;

    void main() {
        float distortion = sin(in_position.x * 10.0 + time) * 0.1;
        vec2 distorted_position = in_position + vec2(0.0, distortion);
        gl_Position = vec4(distorted_position, 0.0, 1.0);
    }
    ''',
    fragment_shader='''
    #version 330

    out vec4 frag_color;

    void main() {
        frag_color = vec4(1.0, 0.0, 0.0, 1.0); // Red color
    }
    '''
)

# Create buffers and VAO
vbo = ctx.buffer(vertices.tobytes())
ibo = ctx.buffer(indices.tobytes())

vao = ctx.simple_vertex_array(vertex_shader, vbo, 'in_position', index_buffer=ibo)

# Animation loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.1, 0.1, 0.1)  # Clear screen with a dark gray background
    vertex_shader['time'].value = pygame.time.get_ticks() / 1000.0  # Pass time to shader
    vao.render(moderngl.TRIANGLES)  # Render the mesh
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
