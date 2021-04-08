#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Michael ORTEGA LIG/CNRS - 02/Apr/2021

import numpy as np
from dollarN import dollarN

dN = dollarN()

dN.add_gesture('X', [   [[0.,0.], [5.,5.]], [[0.,5.], [5.,0.]]      ])
dN.add_gesture('T', [   [[0.,5.], [5.,5.]], [[2.5,0.], [2.5,5.]]    ])

w = np.array([[0, 5.2], [5.,5.]])
x = np.array([[2.5, 0.], [2.5,5.]])
res = dN.recognize([w, x])
print(res)
