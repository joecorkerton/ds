import MapReduce
import sys

"""
Unique Trims in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: sequence id
    # value: nucleotides
    key = record[0]
    value = record[1]
    #Remove last 10 characters
    value = value[:-10]
    mr.emit_intermediate(0, value)

def reducer(key, list_of_values):
    # key: dummy
    # value: trimmed nucleotide strings
    total = []
    for v in list_of_values:
        if v not in total:
            total.append(v)
    for string in total:
        mr.emit(string)


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
