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
import matplotlib.pyplot as plt


class WildFires(simcx.Simulator):
    QUAD_BLACK = (0, 0, 0) * 4
    QUAD_WHITE = (255, 255, 255) * 4
    QUAD_GREEN = (0, 204, 0) * 4
    QUAD_BROWN = (160, 82, 45) * 4
    QUAD_RED = (255, 0, 0) * 4

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
        self.first = True
        self.burned_area = 0
        self.survived_area = 0
        self.count_iteration = 0
        self.number_obstacles = 0

        self.burned_area_list = list()
        self.survived_area_list = list()
        self.number_obstacles_list = list()
        self.display = None

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
                kind = np.random.choice((0, 1), p=(1 - prob, prob))
                temp.append(Area(kind, self.prob_inflame))
                if kind:
                    self.survived_area += 1
                else:
                    self.number_obstacles += 1
            self.values.append(temp)

        self.burned_area_list.append(self.burned_area)
        self.survived_area_list.append(self.survived_area)
        self.number_obstacles_list.append(self.number_obstacles)

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

    def step(self, dt=None):
        temp = 0
        temp_values = deepcopy(self.values)

        for y in range(self.grid_height):
            for x in range(self.grid_width):

                if self.values[y][x].kind >= 2:
                    prob_inflame = self.values[y][x].prob_inflame

                    if self.wind == 0:
                        if y + 1 < self.grid_height:
                            if self.values[y + 1][x].kind == 1 and np.random.random() < prob_inflame:
                                temp_values[y + 1][x].kind = 2
                                temp_values[y + 1][x].prob_inflame = prob_inflame
                            '''if x+1 < self.grid_width and self.values[y+1][x+1] >= 2:
                                cont += 1
                            if x-1 >= 0 and self.values[y+1][x-1] >= 2:
                                cont += 1'''
                        if y - 1 >= 0:
                            if self.values[y - 1][x].kind == 1 and np.random.random() < prob_inflame:
                                temp_values[y - 1][x].kind = 2
                                temp_values[y - 1][x].prob_inflame = prob_inflame
                            '''if x+1 < self.grid_width and self.values[y-1][x+1] >= 2:
                                cont += 1
                            if x-1 >= 0 and self.values[y-1][x-1] >= 2:
                                cont += 1'''
                        if x + 1 < self.grid_width and self.values[y][
                                    x + 1].kind == 1 and np.random.random() < prob_inflame:
                            temp_values[y][x + 1].kind = 2
                            temp_values[y][x + 1].prob_inflame = prob_inflame
                        if x - 1 >= 0 and self.values[y][x - 1].kind == 1 and np.random.random() < prob_inflame:
                            temp_values[y][x - 1].kind = 2
                            temp_values[y][x - 1].prob_inflame = prob_inflame

                    else:
                        if y + 1 < self.grid_height:
                            if self.values[y + 1][x].kind == 1 and np.random.random() < prob_inflame:
                                # high probability
                                temp_values[y + 1][x].kind = 2
                                temp_values[y + 1][x].prob_inflame = prob_inflame
                        if y - 1 >= 0:
                            if self.values[y - 1][x].kind == 1 and np.random.random() < prob_inflame:
                                # low probability
                                temp_values[y - 1][x].kind = 2
                                temp_values[y - 1][x].prob_inflame = prob_inflame * self.prob_decrease
                        if x + 1 < self.grid_width and self.values[y][
                                    x + 1].kind == 1 and np.random.random() < prob_inflame:
                            # high probability
                            temp_values[y][x + 1].kind = 2
                            temp_values[y][x + 1].prob_inflame = prob_inflame
                        if x - 1 >= 0 and self.values[y][x - 1].kind == 1 and np.random.random() < prob_inflame:
                            # low probability
                            temp_values[y][x - 1].kind = 2
                            temp_values[y][x - 1].prob_inflame = prob_inflame * self.prob_decrease
                        if self.wind == 2:
                            if y + 1 < self.grid_height:
                                if x + 1 < self.grid_width:
                                    if self.values[y + 1][x + 1].kind == 1 and np.random.random() < prob_inflame:
                                        temp_values[y + 1][x + 1].kind = 2
                                        temp_values[y + 1][x + 1].prob_inflame = prob_inflame
                                    if x + 2 < self.grid_width and self.values[y + 1][
                                                x + 2].kind == 1 and np.random.random() < prob_inflame:
                                        temp_values[y + 1][x + 2].kind = 2
                                        temp_values[y + 1][x + 2].prob_inflame = prob_inflame
                            if x + 1 < self.grid_width:
                                if y + 2 < self.grid_height and self.values[y + 2][
                                            x + 1].kind == 1 and np.random.random() < prob_inflame:
                                    temp_values[y + 2][x + 1].kind = 2
                                    temp_values[y + 2][x + 1].prob_inflame = prob_inflame

                    temp_values[y][x].kind += 1
                    if temp_values[y][x].kind >= 2 + self.gene_burn:
                        if self.first:
                            temp_values[y][x].kind = -999
                            self.first = False
                        else:
                            temp_values[y][x].kind = -self.gene_burned
                        self.burned_area += 1
                        self.survived_area -= 1
                    temp = 1

                if self.prob_reborn > 0 and self.values[y][x].kind != -999:
                    if self.values[y][x].kind < 0:
                        temp_values[y][x].kind += 1
                        if temp_values[y][x].kind == 0:
                            self.burned_area -= 1
                            self.number_obstacles += 1
                    elif self.values[y][x].kind == 0:
                        if np.random.random() < self.prob_reborn:
                            temp_values[y][x].kind = 1
                            self.survived_area += 1

        self.values = temp_values
        self.count_iteration += 1
        self.burned_area_list.append(self.burned_area)
        self.survived_area_list.append(self.survived_area)
        self.number_obstacles_list.append(self.number_obstacles)

        if self.repeat and temp == 0:
            y = np.random.randint(0, self.grid_height)
            x = np.random.randint(0, self.grid_width)
            self.values[y][x].kind = 2
            self.values[y][x].prob_inflame = self.prob_inflame

        if temp == 0 and not self.repeat and (self.burned_area == 1 or self.prob_reborn == 0):
            self.burned_area_list.append(self.burned_area)
            self.survived_area_list.append(self.survived_area)
            self.number_obstacles_list.append(self.number_obstacles)
            self.display.close()

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
                elif self.values[y][x].kind == -999:
                    self.grid[y][x].colors[:] = WildFires.QUAD_WHITE
                else:
                    self.grid[y][x].colors[:] = WildFires.QUAD_BLACK


if __name__ == '__main__':
    # np.random.seed(911+112)
    # gol = WildFires(150, 75, 10, 0.8, 0.01, 0.8, 5, 50, 2, False)
    # gol = WildFires(150, 75, 10, 0.8, 0, 0.8, 5, 50, 2, False)
    # gol.random(0.8)

    list_of_kinds = [0, 1, 2]
    list_of_regenerate = [0, 0.01]

    for kind in list_of_kinds:
        for regenerate in list_of_regenerate:
            np.random.seed(911 + 112)
            gol = WildFires(250, 150, 5, 0.8, regenerate, 0.8, 5, 50, kind, False)
            gol.random(0.7)

            display = simcx.Display(interval=0.01)
            display.add_simulator(gol)
            display.paused = False
            gol.display = display

            simcx.run()

            print("NUMBER OF INTERACTIONS: ", gol.count_iteration)
            print("NUMBER OF OBSTACLES: ", gol.number_obstacles)
            print("SURVIVED FOREST: ", gol.survived_area)
            print("BURNED FOREST: ", gol.burned_area)

            plt.figure()
            plt.plot(gol.burned_area_list, label="Burned area", color="r")
            plt.plot(gol.survived_area_list, label="Forest", color="g")
            plt.plot(gol.number_obstacles_list, label="Obstacles", color="#A52A2A")
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            plt.savefig("graphic_" + str(kind) + "_" + str(regenerate) + ".png", bbox_inches='tight')
            plt.close()



