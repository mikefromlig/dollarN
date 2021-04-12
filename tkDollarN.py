#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Michael ORTEGA LIG/CNRS - 02/Apr/2021

import os
import numpy as np
import dollarN as dN
import tkinter as tk

#_______________________________________________________________________________
#Globals
dNr              = dN.recognizer()
m_window        = tk.Tk()
m_canvas        = None
result_txt      = None
drawn_strokes   = []
cb_var_1        = tk.IntVar()
cb_var_2        = tk.IntVar()

#_______________________________________________________________________________
#$N management
dNr.add_gesture('X', [   [[0.,0.], [5.,5.]], [[0.,5.], [5.,0.]]      ])
dNr.add_gesture('T', [   [[0.,5.], [5.,5.]], [[2.5,5.], [2.5,0.]]    ])
dNr.add_gesture('U', [   [[0.,5.], [0.,0.], [5.,0.], [5.,5.]]        ])

def recognize():
    if len(drawn_strokes):
        res = dNr.recognize(drawn_strokes)
        txt = res['name']+' ('+str(res['value'])+')'
        result_txt.configure(text=txt)

#_______________________________________________________________________________
#Tkinter management
def c_boxes():
    dNr.set_rotation_invariance(cb_var_1.get())
    dNr.set_same_nb_strokes(cb_var_2.get())

def drawing(event):
    h = m_canvas.winfo_height()
    drawn_strokes[-1].append([  float(event.x),
                                float(h - event.y)])
    m_canvas.create_line(   drawn_strokes[-1][-2][0],
                            h - drawn_strokes[-1][-2][1],
                            drawn_strokes[-1][-1][0],
                            h - drawn_strokes[-1][-1][1])

def start_drawing(event):
    drawn_strokes.append([[ float(event.x),
                            float(m_canvas.winfo_height() - event.y)]])

def stop_drawing(event):
    #print(drawn_strokes)
    pass

def clean():
    global drawn_strokes
    m_canvas.delete("all")
    drawn_strokes = []

def close(event):
    os._exit(os.EX_OK)

#Interactive window
m_window.title('$N example')
m_window.bind('<Escape>', close)
frame_cb = tk.Frame(m_window, borderwidth=2, relief=tk.FLAT)
frame_cb.pack()
cb1 = tk.Checkbutton(frame_cb,  text="rotation invariance",
                                command=c_boxes,
                                variable=cb_var_1,
                                onvalue=1, offvalue=0)
cb2 = tk.Checkbutton(frame_cb,  text="same number of strokes",
                                command=c_boxes,
                                variable=cb_var_2,
                                onvalue=1, offvalue=0)

m_canvas = tk.Canvas(m_window, width=400, height=400, background='lightgrey')
m_canvas.pack()
m_canvas.bind("<ButtonPress-1>", start_drawing)
m_canvas.bind("<ButtonRelease-1>", stop_drawing)
m_canvas.bind("<B1-Motion>", drawing)

cb1.pack(side=tk.LEFT)
cb2.pack(side=tk.RIGHT)
if dNr.get_rotation_invariance():    cb1.select()
if dNr.get_same_nb_strokes():        cb2.select()

frame_bt = tk.Frame(m_window, borderwidth=2, relief=tk.FLAT)
frame_bt.pack()
tk.Button(frame_bt, text="Recognize", command=recognize).pack(side=tk.RIGHT)
tk.Button(frame_bt, text="Clean", command=clean).pack(side=tk.LEFT)

result_txt = tk.Label(m_window, text="")
result_txt.pack()

m_window.mainloop()
