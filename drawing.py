#! usr/bin/env python

'''The purpose of this program is to generate a drawing using Pycairo'''

#Import neccessary modules
import cairo

width = 1000 
height = 2000

#create the coordinates to display your graphic, designate output
surface = cairo.PDFSurface("Pycairo.pdf",width, height)
#create the coordinates you will be drawing on
context = cairo.Context(surface)

#Need to tell cairo where to put the brush, the color and width, and the shape you want it to draw
#draw a line
context.set_line_width(3)
context.move_to(50,25) 
context.line_to(450,25)
context.stroke()

#draw a rectangle
context.rectangle(100,100,150,350)        #(x0,y0,x1,y1)
context.fill()

#write out drawing
surface.finish()