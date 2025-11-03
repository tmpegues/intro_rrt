import pytest
import numpy as np
import distance as dt

def test_eu_dist():
    """Ensure Euclidian distances are correct"""
    d1 = dt.eu_dist([0,0], [0,1])
    d2 = dt.eu_dist([0,0], [1,1])
    d3 = dt.eu_dist([0,1], [0,0])
    d4 = dt.eu_dist([1,1], [0,0])
    d5 = dt.eu_dist([-1,-1], [1,-1])

    assert d1 - 1 < 0.00001
    assert d2 - np.sqrt(2) < 0.00001
    assert d1 - d3 < 0.00001
    assert d2 - d4 < 0.00001
    assert d5 - 2 < 0.00001

def test_point_in_seg():
    """Ensure point in segment calculations are correct"""
    buffer = 0

    point = [0,0]
    end1 = [-1, 0]
    end2 = [1, 0]
    c1 = dt.point_in_seg(point, end1, end2, buffer)

    point = [0,0]
    end1 = [0, 0]
    end2 = [1, 0]
    c2 = dt.point_in_seg(point, end1, end2, buffer)

    point = [0,0]
    end1 = [.01, 0]
    end2 = [1, 0]
    c3 = dt.point_in_seg(point, end1, end2, buffer)

    point = [0,.01]
    end1 = [-1, 0]
    end2 = [1, 0]
    c4 = dt.point_in_seg(point, end1, end2, buffer)

    assert c1 == True
    assert c2 == True
    assert c3 == False
    assert c4 == False