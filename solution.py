from Pyro4 import expose
from heapq import merge

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        processed_arr = self.read_input()
        step = len(processed_arr) / len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(processed_arr[i*step:i*step+step]))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(array):
        n = len(array)
        curr_size = n
        while curr_size > 1:
            mi = findMax(array, curr_size)
            if mi != curr_size-1:
                flip(array, mi)
                flip(array, curr_size-1)
            curr_size -= 1
        return array

    @staticmethod
    @expose
    def myreduce(mapped):
        arr_num = len(mapped)
        res = mapped[0].value
        for i in range(1, arr_num):
            res = list(merge(res, list(mapped[i].value)))
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        array = []
        arr_line = f.readline().split(' ')
        for element in arr_line:
            if element != '':
                array.append(int(element))
        f.close()
        return array

    def write_output(self, output):
        f = open(self.output_file_name, 'a')
        f.write(str(output))
        f.write('\n')
        f.close()


# Reverses arr[0..i] */
def flip(arr, i):
    start = 0
    while start < i:
        temp = arr[start]
        arr[start] = arr[i]
        arr[i] = temp
        start += 1
        i -= 1

# Returns index of the maximum
# element in arr[0..n-1] */
def findMax(arr, n):
    mi = 0
    for i in range(0,n):
        if arr[i] > arr[mi]:
            mi = i
    return mi