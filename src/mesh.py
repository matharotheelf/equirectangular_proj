import moderngl

class Mesh:
    def __init__(self, program, panel):
        self.colour = panel.colour
        self.ctx = moderngl.get_context()
        vertices = panel.vertices

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.vertex_array(program, [(self.vbo, '3f 12x 8x', 'in_vertex')])

    def render(self):
        self.vao.program['color'] = self.colour
        self.vao.render()
