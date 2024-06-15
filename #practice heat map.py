#practice Gooey

import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2


tk.Tk().withdraw() # part of the import if you are not using other tkinter functions

fn = askopenfilename()
print("user chose", fn)
#from typing import Mapping, Any, Optional
#from gooey.types import PublicGooeyState

'''
# Gooey Documentation: https://github.com/chriskiehl/Gooey?tab=readme-ov-file#installation-instructions

args = []

@Gooey  (program_name='Example App', header_bg_color='blue') # GUI python decorator


def main():

    global args
    parser = GooeyParser()

    parser.add_argument('num_1', action='store', help='description 1', metavar='metavar desc')
    parser.add_argument('num_2', action='store', help='description 2', metavar='metavar desc 2')
    parser.add_argument('--num_2', action='store', help='description 2', metavar='metavar desc 2')



    parser.add_argument('filename', widget='FileChooser')


    args = parser.parse_args() # passes arguements; comes at the end

    while True:

        image = cv2.imread(args.filename)
        cv2.namedWindow('test')
        cv2.imshow('test', image)

        if cv2.waitKey(1) & 0xFF == 27:  # Exit on pressing 'ESC'
            break



    print(int(args.num_1) + int(args.num_2))

#ef on_success

main()

while True:

    image = cv2.imread(args.filename)
    cv2.namedWindow('test222')
    cv2.imshow('test222', image)

    if cv2.waitKey(0):  # Exit on pressing 'ESC'
        break
'''