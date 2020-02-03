#!/usr/bin/env python
import sys
from sys import argv

from PIL import Image
from PIL import ImageDraw

# Parse Command Line Arguments
if len(argv) < 3:
    sys.exit("Usage is render.py <input file> <output file> [cutoff]")

input_file = argv[1]
output_file = argv[2]
cutoff = None if len(argv) <= 3 else float(argv[3])


# Helper Functions
def circle_as_4_tuple(center, size):
    return (center[0] - size, center[1] - size, center[0] + size, center[1] + size)


frames = []


def new_frame():
    img = Image.new('L', (1024, 1024), 'white')
    frames.append(img)
    return ImageDraw.Draw(img)


with open(input_file, 'r') as f:
    num_parts, box_size = next(f).split()
    num_parts, box_size = int(num_parts), float(box_size)

    # Parse input file
    drawer = new_frame()
    for line in f:
        if line.isspace():
            drawer = new_frame()
            continue

        line_split = line.split()
        center_x = int(1024 * (float(line_split[0]) / box_size))
        center_y = int(1024 * (float(line_split[1]) / box_size))
        center = (center_x, center_y)

        if cutoff:
            cutuff_radius = int(1024 * (cutoff / box_size))
            drawer.ellipse(circle_as_4_tuple(center, cutuff_radius), 'yellow')
        drawer.ellipse(circle_as_4_tuple(center, 1), 'black')

    frames[0].save(output_file, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)
