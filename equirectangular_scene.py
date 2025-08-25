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
    gl_version = (4, 1)
    window_size = (2000, 1000)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ctx = moderngl.create_context()

        self.screenshot_active = True

        self.program = self.ctx.program(
            vertex_shader='''
                #version 330 core

                uniform vec3 position;
                uniform float scale;

                layout (location = 0) in vec3 in_vertex;
                layout (location = 1) in vec3 in_normal;
                layout (location = 2) in vec2 in_uv;

                out vec3 v_vertex;
                out vec3 v_normal;
                out vec2 v_uv;

                void main() {
                    v_vertex = in_vertex;
                    v_normal = in_normal;
                    v_uv = in_uv;

                    gl_Position = vec4(v_vertex, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330 core

                uniform vec3 color;

                in vec3 v_vertex;
                in vec3 v_normal;
                in vec2 v_uv;

                layout (location = 0) out vec4 out_color;

                void main() {
                    out_color = vec4(color, 1.0);
                }
            ''',
        )

        colours = []

        for _index in range(6):
            currentColourShiftR = random.random();
            currentColourShiftG = random.random();
            currentColourShiftB = random.random();

            colours.append((currentColourShiftR, currentColourShiftG, currentColourShiftB))

        my_cube = Cube(colours=colours)
        self.meshes = [Mesh(self.program, panel) for panel in my_cube.panels]

    def on_render(self, time: float, frametime: float):
        self.ctx.clear()
        self.ctx.enable(self.ctx.DEPTH_TEST)

        [mesh.render() for mesh in self.meshes]

        if self.screenshot_active:
            screenshot.create(self.ctx.fbo)
            self.screenshot_active = False

Scene.run()
