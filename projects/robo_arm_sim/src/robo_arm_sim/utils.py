from itertools import islice, tee

def pairwise(iterable):
    """Gives back pairs of elements

    example: 
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, islice(b, None))

def get_angle(index, angle):
    return angle * 2 if index == 0 else angle + 90
