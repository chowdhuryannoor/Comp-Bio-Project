import numpy as np
from pydivsufsort import divsufsort, kasai

class Node:
    def __init__(self, ):
        return


def suffix_tree(sa, lcp):
    return


if __name__ == "__main__":
    string_inp = "banana$"
    suffix_array = divsufsort(string_inp)
    lcp_array = kasai(string_inp, suffix_array)
    print(suffix_array, lcp_array)
    for i in suffix_array:
        print(string_inp[i:])