# coding: utf-8
# -----------------------------------------------------------------------------
# Copyright (c) 2015 Tiago Baptista
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Game of Life example using the simcx framework.

"""

from __future__ import division

__docformat__ = 'restructuredtext'
__author__ = 'Paulo Pereira'

# Allow the import of the framework from one directory down the hierarchy
import sys

sys.path.insert(1, '..')

import simcx
import numpy as np
import pyglet
from copy import deepcopy
from Area import Area


class WildFires(simcx.Simulator):
    QUAD_BLACK = (0, 0, 0) * 4
    QUAD_WHITE = (255, 255, 255) * 4
    QUAD_GREEN = (0, 204, 0) * 4
    QUAD_BROWN = (160, 82, 45) * 4
    QUAD_RED   = (255, 0, 0) * 4

    def __init__(self, width=50, height=50, cell_size=20, prob_inflame=0.8, prob_reborn=0.1, prob_decrease=0.8,
                 gene_burn=5, gene_burned=25, wind=0, repeat=False):
        super(WildFires, self).__init__(width * cell_size, height * cell_size, use_mpl=False)

        self.grid_width = width
        self.grid_height = height
        self.values = []
        self.prob_inflame = prob_inflame
        self.prob_reborn = prob_reborn
        self.prob_decrease = prob_decrease
        self.gene_burn = gene_burn
        self.gene_burned = gene_burned
        self.wind = wind
        self.repeat = repeat

        # create graphics objects
        self.batch = pyglet.graphics.Batch()
        self.grid = []
        for y in range(height):
            self.grid.append([])
            for x in range(width):
                vertex_list = self.batch.add(4, pyglet.gl.GL_QUADS, None,
                                             ('v2i', (x * cell_size, y * cell_size,
                                                      x * cell_size + cell_size, y * cell_size,
                                                      x * cell_size + cell_size, y * cell_size + cell_size,
                                                      x * cell_size, y * cell_size + cell_size)),
                                             ('c3B', WildFires.QUAD_BROWN))
                self.grid[y].append(vertex_list)


    def random(self, prob):
        self.values = []
        for y in range(self.grid_height):
            temp = []
            for x in range(self.grid_width):
                temp.append(Area(np.random.choice((0, 1), p=(1 - prob, prob)), self.prob_inflame))
            self.values.append(temp)

        y = np.random.randint(0, self.grid_height)
        x = np.random.randint(0, self.grid_width)
        self.values[y][x].kind = 2

        self._update_graphics()


    def add_block(self, block, pos_x, pos_y):
        height, width = block.shape

        for y in range(height):
            for x in range(width):
                self.values[pos_y + y, pos_x + x] = block[y, x]

        self._update_graphics()

    def step(self):
        temp = 0
        temp_values = deepcopy(self.values)

        for y in range(self.grid_height):
            for x in range(self.grid_width):

                if self.values[y][x].kind >= 2:
                    prob_inflame = self.values[y][x].prob_inflame

                    if self.wind == 0:
                        if y+1 < self.grid_height:
                            if self.values[y+1][x].kind == 1 and np.random.random() < prob_inflame:
                                temp_values[y+1][x].kind = 2
                                temp_values[y+1][x].prob_inflame = prob_inflame
                            '''if x+1 < self.grid_width and self.values[y+1][x+1] >= 2:
                                cont += 1
                            if x-1 >= 0 and self.values[y+1][x-1] >= 2:
                                cont += 1'''
                        if y-1 >= 0:
                            if self.values[y-1][x].kind == 1 and np.random.random() < prob_inflame:
                                temp_values[y-1][x].kind = 2
                                temp_values[y-1][x].prob_inflame = prob_inflame
                            '''if x+1 < self.grid_width and self.values[y-1][x+1] >= 2:
                                cont += 1
                            if x-1 >= 0 and self.values[y-1][x-1] >= 2:
                                cont += 1'''
                        if x+1 < self.grid_width and self.values[y][x+1].kind == 1 and np.random.random() < prob_inflame:
                            temp_values[y][x+1].kind = 2
                            temp_values[y][x+1].prob_inflame = prob_inflame
                        if x-1 >= 0 and self.values[y][x-1].kind == 1 and np.random.random() < prob_inflame:
                            temp_values[y][x-1].kind = 2
                            temp_values[y][x-1].prob_inflame = prob_inflame

                    else:
                        if y+1 < self.grid_height:
                            if self.values[y+1][x].kind == 1 and np.random.random() < prob_inflame:
                                # high probability
                                temp_values[y+1][x].kind = 2
                                temp_values[y+1][x].prob_inflame = prob_inflame
                        if y-1 >= 0:
                            if self.values[y-1][x].kind == 1 and np.random.random() < prob_inflame:
                                # low probability
                                temp_values[y-1][x].kind = 2
                                temp_values[y-1][x].prob_inflame = prob_inflame*self.prob_decrease
                        if x+1 < self.grid_width and self.values[y][x+1].kind == 1 and np.random.random() < prob_inflame:
                            # high probability
                            temp_values[y][x+1].kind = 2
                            temp_values[y][x+1].prob_inflame = prob_inflame
                        if x-1 >= 0 and self.values[y][x-1].kind == 1 and np.random.random() < prob_inflame:
                            # low probability
                            temp_values[y][x-1].kind = 2
                            temp_values[y][x-1].prob_inflame = prob_inflame*self.prob_decrease
                        if self.wind == 2:
                            if y+1 < self.grid_height:
                                if x+1 < self.grid_width:
                                    if self.values[y+1][x+1].kind == 1 and np.random.random() < prob_inflame:
                                        temp_values[y+1][x+1].kind = 2
                                        temp_values[y+1][x+1].prob_inflame = prob_inflame
                                    if x+2 < self.grid_width and self.values[y+1][x+2].kind == 1 and np.random.random() < prob_inflame:
                                        temp_values[y+1][x+2].kind = 2
                                        temp_values[y+1][x+2].prob_inflame = prob_inflame
                            if x+1 < self.grid_width:
                                if y+2 < self.grid_height and self.values[y+2][x+1].kind == 1 and np.random.random() < prob_inflame:
                                    temp_values[y+2][x+1].kind = 2
                                    temp_values[y+2][x+1].prob_inflame = prob_inflame

                    temp_values[y][x].kind += 1
                    if temp_values[y][x].kind >= 2 + self.gene_burn:
                        temp_values[y][x].kind = -self.gene_burned
                    temp = 1

                if self.prob_reborn > 0:
                    if self.values[y][x].kind < 0:
                        temp_values[y][x].kind += 1

                    elif self.values[y][x].kind == 0:
                        if np.random.random() < self.prob_reborn:
                            temp_values[y][x].kind = 1

        self.values = temp_values
        if self.repeat and temp == 0:
            y = np.random.randint(0, self.grid_height)
            x = np.random.randint(0, self.grid_width)
            self.values[y][x].kind = 2
            self.values[y][x].prob_inflame = self.prob_inflame

        self._update_graphics()

    def draw(self):
        self.batch.draw()

    def _update_graphics(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.values[y][x].kind == 1:
                    self.grid[y][x].colors[:] = WildFires.QUAD_GREEN
                elif self.values[y][x].kind == 0:
                    self.grid[y][x].colors[:] = WildFires.QUAD_BROWN
                elif self.values[y][x].kind >= 2:
                    self.grid[y][x].colors[:] = WildFires.QUAD_RED
                else:
                    self.grid[y][x].colors[:] = WildFires.QUAD_BLACK


if __name__ == '__main__':
    np.random.seed(911+112)

    #gol = WildFires(150, 75, 10, 0.8, 0.01, 5, 25, True, False)
    gol = WildFires(150, 75, 10, 0.8, 0.01, 0.8, 5, 50, 2, False)
    gol.random(0.8)

    display = simcx.Display(interval=0.2)
    display.add_simulator(gol)
    simcx.run()
