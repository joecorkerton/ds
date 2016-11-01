import MapReduce
import sys

"""
Join in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: order_id
    # value: rest of the attributes
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: order_id
    # value: list of instances with this order_id
    #Find inner product
    for v in list_of_values:
        current_table = v[0]
        if current_table == "order":
            for instance in list_of_values:
                if instance[0] != current_table:
                    mr.emit(v + instance)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
