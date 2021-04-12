#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Michael ORTEGA LIG/CNRS - 02/Apr/2021

import dollarN as dN

r = dN.recognizer()

r.add_gesture('X', [   [[0.,0.], [5.,5.]], [[0.,5.], [5.,0.]]      ])
r.add_gesture('T', [   [[0.,5.], [5.,5.]], [[2.5,0.], [2.5,5.]]    ])

test = [[[0, 5.2], [5.,5.]], [[2.5, 0.], [2.5,5.]]]
print( r.recognize(test) )
