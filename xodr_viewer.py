#!/usr/bin/env python
# coding: utf-8


import xodr_parser
from lxml import etree
import matplotlib.pyplot as plt
import elements
from math import cos, sin, radians
import numpy as np
from viewer.draw_lane import DrawLaneSection


class XodrViewer:
    def __init__(self, fpath: str):
        tree = etree.parse(fpath)
        root = tree.getroot()
        self.xodr = xodr_parser.parse_opendrive(root)
        self.ax = plt.figure().add_subplot(111)
        
    def show_geometry(self):
        self.draw_geometry()
        self.show()
        
    def draw_lane(self):
        for road in self.xodr.roads:
            for lanesection in road.lanes.lane_sections: 
                DrawLaneSection(lanesection).Draw()

                    
    def draw_geometry_color(self):
        for road in self.xodr.roads:
            for geometry in road.planView.get_geometries:
                if isinstance(geometry, elements.geometry.Line):
                    self._draw_line(geometry)
                elif isinstance(geometry, elements.geometry.Arc):
                    self._draw_arc(geometry)
                elif isinstance(geometry, elements.geometry.Spiral):
                    self._draw_spiral(geometry)
                elif isinstance(geometry, elements.geometry.ParamPoly3):
                    self._draw_param_poly3(geometry)
                elif isinstance(geometry, elements.geometry.Poly3):
                    self._draw_poly3(geometry)

    def draw_geometry(self):
        for road in self.xodr.roads:
            _x = []
            _y = []
            for s in np.linspace(0,road.planView.length,100):
                pos,_ = road.planView.calc(s)
                _x.append(pos[0])
                _y.append(pos[1])
            self.ax.plot(_x, _y, color="#98b574")
                
        
    def _draw_line(self, line: elements.geometry.Line):
        x, y = line.start_position
        length = line.length
        [end_x, end_y],hdg = line.calc_position(length)
        self.ax.plot([x, end_x], [y, end_y], color='#677d90')

    def _draw_arc(self,arc:elements.geometry.Arc):
        x = []
        y = []
        for s in np.linspace(0,arc.length,100):
            [_x,_y],_ = arc.calc_position(s)
            x.append(_x)
            y.append(_y)
        self.ax.plot(x, y, color="#98b574")

    def _draw_spiral(self,spiral:elements.geometry.Spiral):
        x = []
        y = []
        for s in np.linspace(0,spiral.length,100):
            [_x,_y],_ = spiral.calc_position(s)
            x.append(_x)
            y.append(_y)
        self.ax.plot(x, y, color='#ebc44c')
        
    def _draw_param_poly3(self,poly:elements.geometry.ParamPoly3):
        x = []
        y = []
        for s in np.linspace(poly.start_position,poly.length,100):
            [_x,_y],_ = poly.calc_position(s)
            x.append(_x)
            y.append(_y)
        self.ax.plot(x, y, color='#faf0e6')
    
    def _draw_poly3(self,poly:elements.geometry.Poly3):
        x = []
        y = []
        for s in np.linspace(0,poly.length,100):
            [_x,_y],_ = poly.calc_position(s)
            x.append(_x)
            y.append(_y)
        self.ax.plot(x, y, color='#b1754c')
        
    
    def show(self):
        self.ax.axis('equal')
        plt.show()
        


if __name__ == "__main__":
    viewer1 = XodrViewer("./xodr/examples/Ex_Lane-Width/Ex_Lane-Width.xodr")
    #viewer1 = XodrViewer("./xodr/curve_r100.xodr")
    #viewer1 = XodrViewer("./xodr/multi_intersections.xodr")
    #viewer1 = XodrViewer("./xodr/jolengatan.xodr")
    viewer1.draw_lane()

