# dollarN
**_Python implementation of $N, the 2D multistrokes recognizer_** 

http://depts.washington.edu/acelab/proj/dollar/ndollar.html

> The $N Multistroke Recognizer is a 2-D multistroke recognizer designed 
> for rapid prototyping of gesture-based user interfaces. $N is built upon 
> the $1 Unistroke Recognizer. $N automatically generalizes examples of 
> multistrokes to encompass all possible stroke orders and directions, 
> meaning you can make and define multistrokes using any stroke order and 
> direction you wish, provided you begin at either endpoint of each 
> component stroke, and $N will generalize so as to recognize other ways 
> to articulate that same multistroke. A version of $N utilizing 
> Protractor, optional here, improves $N's speed. 

## Features
- [Python 3](https://www.python.org/)
- [Numpy](https://numpy.org/)

## Example of use (simple.py):
```
import dollarN as dN

r = dN.recognizer()

#Adding gestures: multistrokes with names
r.add_gesture('X', [   [[0.,0.], [5.,5.]], [[0.,5.], [5.,0.]]      ])
r.add_gesture('T', [   [[0.,5.], [5.,5.]], [[2.5,0.], [2.5,5.]]    ])

#Launching a recognition
test = [[[0, 5.2], [5.,5.]], [[2.5, 0.], [2.5,5.]]]
print( r.recognize(test) )
```
```
{'name': 'T', 'value': 0.9484976300936439, 'time': 0.006083965301513672}
```
## Demo
A demo is available with tkDollarN.py
