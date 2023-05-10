#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Michael ORTEGA LIG/CNRS - 02/Apr/2021

import math, time
import numpy as np

def vector(a, b):
    return [b[0] - a[0], b[1] - a[1]]

def norm(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def normalize(v):
    n =norm(v)
    if n != 0:
        return [v[0]/n, v[1]/n]
    return [0, 0]

def distance(a, b):
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

def bouding_box_size(points):
    return np.max(points, axis=0) - np.min(points, axis=0)

def angle_btw_u_vectors(v1, v2):
    ''' Gives acute angle between unit vectors
        from (0,0) to v1, and (0,0) to v2'''
    n = v1[0]*v2[0] + v1[1]*v2[1]
    return math.acos(max(-1.0, min(1.0, n))) #ensure [-1,+1]

def deg_2_rad(d):
    return d * math.pi / 180.0

def heap_permute(n, order, orders):
    if n == 1:
        orders.append(order.copy())
        return orders
    else:
        for i in range(n):
            orders = heap_permute(n-1, order, orders)
            if n%2 == 1: # swap 0, n-1
                tmp = order[0]
                order[0] = order[n - 1]
                order[n - 1] = tmp
            else: # swap i, n-1
                tmp = order[i]
                order[i] = order[n - 1]
                order[n - 1] = tmp
        return orders

def indicative_angle(points):
    ''' find and save the indicative angle from the points' centroid to the
        first point. Then rotate to set this angle to 0.'''
    c = np.mean(points, axis=0)
    return math.atan2(c[1]-points[0][1], c[0] - points[0][0])

def resample(points, n):
    ''' resample a points path into n evenly spaced points'''
    I = path_length(points)/(n-1)
    D = 0.0
    pts = points.copy()
    new_points = [pts[0]]
    i = 1
    while i < len(pts):
        d = distance(pts[i-1], pts[i])
        if (D+d) >= I:
            q = [   pts[i-1][0] + ((I-D)/d)*(pts[i][0] - pts[i-1][0]),
                    pts[i-1][1] + ((I-D)/d)*(pts[i][1] - pts[i-1][1]) ]
            new_points.append(q)
            pts = np.insert(pts, i, q, axis=0)
            D = 0.0
        else:
            D += d
        i+=1

    if len(new_points) == n-1:
        new_points.append(pts[-1])
    return np.array(new_points)

def path_length(A):
    return np.sqrt(((A[1:]-A[:-1])**2).sum(axis=1)).sum()

def path_distance(A, B):
    '''average distance between corresponding points in two paths'''
    return np.sqrt(((A-B)**2).sum(axis=1)).sum() / len(A)

def distance_at_best_angle(points, S, teta_a, teta_b, d_teta):
    x1 = self.phi*teta_a +(1 -self.phi)*teta_b
    f1 = self.distance_at_angle(points, S, x1)
    x2 = (1 -self.phi)*teta_a +self.phi*teta_b
    f2 = self.distance_at_angle(points, S, x2)
    while math.fabs(teta_b - teta_a) > d_teta:
        if f1 < f2:
            teta_b  = x2
            x2      = x1
            f2      = f1
            x1 = self.phi*teta_a + (1 -self.phi)*teta_b
            f1 = self.distance_at_angle(points, S, x1)
        else:
            teta_a  = x1
            x1      = x2
            f1      = f2
            x2 = (1 -self.phi)*teta_a + self.phi*teta_b
            f2 = self.distance_at_angle(points, S, x2)
    return min(f1, f2)

def distance_at_angle(points, S, radians):
    new_points = self.rotate_by(points, radians)
    d = self.path_distance(newPoints, S)

def combine_strokes(strokes):
    '''combine strokes into one unistroke: points'''
    points = []
    for s in strokes:
        for p in s:
            points.append(p)
    return np.array(points)

def rotate_by(points, angle):
    new_points = []
    c = np.mean(points, axis=0)
    for p in points:
        qx = (p[0]-c[0])*math.cos(angle) -(p[1]-c[1])*math.sin(angle) +c[0]
        qy = (p[0]-c[0])*math.sin(angle) +(p[1]-c[1])*math.cos(angle) +c[1]
        new_points.append([qx, qy])
    return np.array(new_points)

def make_unistrokes(strokes, orders):
    unistrokes = []
    for r in range(len(orders)):
        for b in range(len(orders[r])**2):
            unistroke = [[0,0]]
            for i in range(len(orders[r])):
                pts = []
                if ((b >> i) & 1) == 1: #is b's bit at index i on?
                    pts = np.flip(strokes[orders[r][i]], axis=0)
                else:
                    pts = strokes[orders[r][i]].copy()
                unistroke = np.concatenate((unistroke,  pts))
            unistrokes.append(unistroke[1:])
    return unistrokes

def scale_dim_to(points, size, ratio1D):
    ''' Scale dimensionnally-sensitive based on threshold ratio1D.
        Next, if using rotation_inveriance, restore drawn orientation by
        rotating +angle. Then translate to the origin (0,0)'''
    b = bouding_box_size(points)
    new_points = []
    for p in points:
        if b[0] == 0 or b[1] == 0:
            q = [   p[0]*size/max(b[0],b[1]),
                    p[1]*size/max(b[0],b[1])]
        elif min(b[0]/b[1], b[1]/b[0]) <= ratio1D:
            q = [   p[0]*size/max(b[0],b[1]),
                    p[1]*size/max(b[0],b[1])]
        else:
            q = [   p[0]*size/b[0],
                    p[1]*size/b[1] ]
        new_points.append(q)
    return np.array(new_points)

def calc_start_u_vector(points, i):
    '''Calculates the start units vector v for points using index i'''
    return normalize(vector(points[0], points[i]))

def check_restore_orientation(points, angle):
    if self.rotation_invariance:
        return self.rotate_by(points, angle)

def translate_to(points, pt):
    return points + pt - np.mean(points, axis=0)

#--PROTRACTOR----------------------------------------
def optimal_cos_distance(v1, v2):
    '''for Protractor option'''
    a, b = 0.0, 0.0
    for _i in range(int(len(v1)/2)):
        i = _i*2
        if i+1 < len(v1) and i+1 < len(v2):
            a += v1[i]*v2[i] + v1[i+1]*v2[i+1]
            b += v1[i]*v2[i+1] - v1[i+1]*v2[i]
    angle = math.atan(b / a)
    return math.acos(a * math.cos(angle) + b * math.sin(angle))

def vectorize(points, rotation_invariance):
    '''for Protractor option'''
    cos = 1.0
    sin = 0.0
    if rotation_invariance:
        iAngle = math.atan2(points[0][1], points[0][0])
        #print((iAngle + math.pi / 8.0) / (math.pi / 4.0))
        baseOrientation = (math.pi / 4.0) * math.floor((iAngle + math.pi / 8.0) / (math.pi / 4.0))
        cos = math.cos(baseOrientation - iAngle)
        sin = math.sin(baseOrientation - iAngle)

    vector = []
    sum = 0.0
    for p in points:
        new_v = [   p[0]*cos -p[1]*sin,
                    p[1]*cos -p[0]*sin ]
        vector.append(new_v[0])
        vector.append(new_v[1])
        sum += new_v[0] * new_v[0] + new_v[1] * new_v[1]
    vector = np.array(vector)
    vector /= math.sqrt(sum)
    return vector
#--PROTRACTOR----------------------------------------

class globals():
    def __init__(self):
        self.nb_resamp = 96
        self.square_size = 250.0
        self._1D_threshold = 0.25
        self.origin = [0, 0]
        self.phi_M = 30
        self.phi = .5*(-1+math.sqrt(5))
        self.teta = 45
        self.d_teta = 2
        self.angle_sim_threshold = deg_2_rad(30.0)
        self.angle_range = deg_2_rad(45.0);
        self.angle_precision = deg_2_rad(2.0);

        self.start_angle_index = int(self.nb_resamp/8)
        self.diagonal = math.sqrt(  self.square_size * self.square_size +
                                    self.square_size * self.square_size);
        self.half_diagonal = 0.5 * self.diagonal

GBLS = globals()

class unistroke():
    def __init__(self,  name, rotation_invariance, points):
        self.name = name
        self.points = resample(points, GBLS.nb_resamp)
        radians = indicative_angle(self.points)

        self.points = rotate_by(self.points, -radians)
        self.points = scale_dim_to( self.points,
                                    GBLS.square_size,
                                    GBLS._1D_threshold);
        if rotation_invariance:
            self.points = rotate_by(self.points, radians) #restore
        self.points = translate_to(self.points, GBLS.origin)
        self.start_u_vector = calc_start_u_vector(  self.points,
                                                    GBLS.start_angle_index)
        self.vector = vectorize(self.points, rotation_invariance) #Protractor

class multistroke():
    def __init__(self, name, rotation_invariance, strokes):
        ''' srokes should be an array of strokes'''
        self.name = name;
        self.nb_strokes = len(strokes) # number of individual strokes

        order = np.arange(len(strokes))
        orders = heap_permute(len(strokes), order, []);
        unistrokes = make_unistrokes(strokes, orders)
        self.unistrokes = [] # unistrokes for this multistroke
        for u in unistrokes:
            self.unistrokes.append(unistroke(name, rotation_invariance, u))

class recognizer():
    def __init__(self):
        self.rotation_invariance = True
        self.same_nb_strokes = True
        self.use_protractor = True
        self.multistrokes = []

    def set_rotation_invariance(self, b):
        self.rotation_invariance = b

    def set_same_nb_strokes(self, b):
        self.same_nb_strokes = b

    def get_rotation_invariance(self):
        return self.rotation_invariance

    def get_same_nb_strokes(self):
        return self.same_nb_strokes

    def add_gesture(self, name, strokes):
        m = multistroke(name, self.rotation_invariance, strokes)
        self.multistrokes.append(m)

    def recognize(self, strokes):
        t0 = time.time()
        points = combine_strokes(strokes) # make one connected unistroke from the given strokes
        candidate = unistroke("", self.rotation_invariance, points)
        scores = np.full(len(self.multistrokes), np.inf)
        for _m in range(len(self.multistrokes)):
            m = self.multistrokes[_m]
            if not self.same_nb_strokes or len(strokes) == m.nb_strokes: # optional -- only attempt match when same nb of component strokes
                for _u in range(len(m.unistrokes)):
                    u = m.unistrokes[_u]
                    # strokes start in the same direction)
                    abuv = angle_btw_u_vectors( candidate.start_u_vector,
                                                u.start_u_vector)
                    if abuv <= GBLS.angle_sim_threshold:
                        d = None
                        if (self.use_protractor):
                            d = optimal_cos_distance(u.vector, candidate.vector)
                        else:
                            d = distance_at_best_angle( candidate.points,
                                                        u,
                                                        -GBLS.angle_range,
                                                        GBLS.angle_range,
                                                        GBLS.angle_precision)
                        if d < scores[_m]:
                            scores [_m] = d # best (least) distance
        found = np.argmin(scores)

        t1 = time.time()
        if scores[found] >= 1:
            return {'name': '', 'value':0.0, 'time': t1-t0}
        else:
            result = {'name': self.multistrokes[found].name}
            if self.use_protractor:
                result['value'] = 1.0 - scores[found]
            else:
                result['value'] = 1.0 - scores[found] / GBLS.half_diagonal
            result['time'] = t1-t0
        return result
