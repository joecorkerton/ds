import MapReduce
import sys

"""
Matrix multiplication in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: the indice that isn't summed over
    #Mij = A_ik B_kj
    # value: [matrix, i, j, value]
    #We have to assume a size of the matrix. I assume n = 20
    value = record
    if record[0] == "a":
        for i in range(20):
            key = (record[1], i)
            mr.emit_intermediate(key, value)
    else:
        for i in range(20):
            key = (i, record[2])
            mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: [i, j] of output matrix
    # value: Data from relevant cells of input matrix
    total = 0
    for v in list_of_values:
        if v[0] == "b":
            continue
        else:
            for w in list_of_values:
                if w[0] == "b" and w[1] == v[2]:
                    total += (v[3] * w[3])
        
    mr.emit((key[0], key[1], total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
