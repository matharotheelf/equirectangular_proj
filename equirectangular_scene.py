import math
import os
import sys
import random

import glm
import moderngl
import numpy as np
import pygame
import moderngl_window as mglw
from moderngl_window import screenshot


from src.panel import Panel
from src.cube import Cube
from src.octohedron import Octohedron
from src.mesh import Mesh

class TriangleGeometry:
    def __init__(self):
        self.ctx = moderngl.get_context()
        vertices = np.array([
            0.0, 0.4, 0.0,
            -0.4, -0.3, 0.0,
            0.4, -0.3, 0.0,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())

    def vertex_array(self, program):
        return self.ctx.vertex_array(program, [(self.vbo, '3f', 'in_vertex')])

class Scene(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (2000, 1000)
    aspect_ratio = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ctx = moderngl.create_context()
        self.ctx.gc_mode = 'context_gc'

        self.screenshot_active = True

        self.program = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;
                
                uniform float time = 0.0;

                in vec4 in_color;
                out vec4 v_color;    // Goes to the fragment shader

                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);

                    float red = mod((in_color[0] + time*2), 1);
                    float green = mod((in_color[1] + time*2), 1); 
                    float blue = mod((in_color[2] + time*2), 1);

                    v_color = vec4(red, green, blue, in_color[3]);
                }
            ''',
            fragment_shader='''
                #version 330

                in vec4 v_color;
                out vec4 f_color;

                void main() {
                    f_color = vec4(v_color);
                }
            ''',        )

        colours = []

        for _index in range(8):
            currentColourShiftR = random.random();
            currentColourShiftG = random.random();
            currentColourShiftB = random.random();

            colours.append((currentColourShiftR, currentColourShiftG, currentColourShiftB))

        # my_cube = Cube(colours=colours)
        # self.meshes = [Mesh(self.program, panel) for panel in my_cube.panels]

        self.my_oct = Octohedron(colours=colours)
        self.meshes = [Mesh(self.program, panel) for panel in self.my_oct.panels]

    def on_render(self, time: float, frametime: float):
        self.ctx.clear()
        self.ctx.clear_samplers()
        self.ctx.gc()
        self.ctx.enable(self.ctx.DEPTH_TEST)

        print(f"Time: {time}, Frame Time: {frametime}")

        # for mesh in self.meshes:
        #     mesh.render(time)

        self.meshes[3].render(time)

        if self.screenshot_active:
            screenshot.create(self.ctx.fbo)
            self.screenshot_active = False

Scene.run()
