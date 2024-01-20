from numpy import dot
from numpy.linalg import norm


def cos_sim(a, b):
    """
    This function calculates the cosine similarity between two input vectors
    'a' and 'b'. Cosine similarity is a measure of similarity between two
    non-zero vectors of an inner product space that measures the cosine
    of the angle between them.

    INPUT:
    a: 1-D array object
    b: 1-D array object
    OUTPUT:
    A scalar value representing the cosine similarity between the input
    vectors 'a' and 'b'.

    Example input:
    a = [0.3, 0.2, 0.5]
    b = [0.2, 0.2, 0.5]
    """
    return dot(a, b)/(norm(a)*norm(b))


def top_highest_x_values(d, x):
    """
    This function takes a dictionary 'd' and an integer 'x' as input, and
    returns a new dictionary containing the top 'x' key-value pairs from the
    input dictionary 'd' with the highest values.

    INPUT:
      d: Dictionary. The input dictionary from which the top 'x' key-value pairs
         with the highest values are to be extracted.
      x: Integer. The number of top key-value pairs with the highest values to
         be extracted from the input dictionary.
    OUTPUT:
      A new dictionary containing the top 'x' key-value pairs from the input
      dictionary 'd' with the highest values.

    Example input:
      d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}
      x = 3
    """
    top_v = dict(sorted(d.items(),
                        key=lambda item: item[1],
                        reverse=True)[:x])
    return top_v
