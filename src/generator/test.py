from Utils import Utils

matrix = [[1,2,3],
          [4,5,6],
          [7,8,9]]

matrix = Utils.rotate(matrix)
for row in matrix:
    print("Row by row: ", row)
print("\n")
matrix = Utils.rotate(matrix)
for row in matrix:
    print("Row by row: ", row)