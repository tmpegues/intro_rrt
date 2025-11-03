import numpy as np

def eu_dist(veca, vecb):
    dist = np.linalg.norm([a-b for  a,b in zip(veca, vecb)])
    return dist

def point_in_seg(point, end_near, end_far, buffer):
    line_dist = eu_dist(end_far, end_near)
    point_near = eu_dist(point, end_near)
    point_far = eu_dist(point, end_far)

    on_line = True
    diff =  (point_near + point_far) - line_dist

    if diff >.00001:
        on_line = False
    return on_line

buffer = 0
point = [0,.1]
end1 = [-1, 0]
end2 = [1, 0]
c4 = point_in_seg(point, end1, end2, buffer)