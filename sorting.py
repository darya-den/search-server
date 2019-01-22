"""Module contains sorting method our_sort"""

def our_sort(mass):
    """Sort the elements of the array of arrays.

    Each array is sorted, then turned into an iterator.
    Take first element of each iterator, find the smallest,
    get next element in the iterator, repeat until all elements are yielded.
    
    :param mass:array of arrays
    """
    first_el = []
    iter_mass = []
    # turn each array into iterator
    for n, seq in enumerate(mass):
        seq = iter(seq)
        iter_mass.append(seq)
        first_el.append(next(seq)) # list of first element of the iterator
    while True:
        minim = min(first_el) # smallest element
        ind = first_el.index(minim) # index of the smallest element in the list
        yield minim
        try:
            first_el[ind] = next(iter_mass[ind]) # go to the next element in iterator
        # if there are no more elements
        except StopIteration:
            del first_el[ind]
            del iter_mass[ind]
            # if there are no more iterators
            if first_el == []:
                break

if __name__ == '__main__':
    mass = [[1, 4, 7, 9], [2, 3, 4, 5, 6], [8, 10, 16, 24]]
    for n in our_sort(mass):
        print(n)
