input_matrix = eval(input("Enter your matrix:\n"))

matrix_rows = len(input_matrix)
matrix_cols = len(input_matrix[0])

# First, normalize matrix
smallest = min([min(row) for row in input_matrix])
increment = 0

if smallest <= 0:
    increment = -smallest + 1

# Apply normalization onto matrix
input_matrix = [[elem + increment for elem in row] for row in input_matrix]

# Extend rows and cols to make tableau shape
tab = [row + [0]*(matrix_rows) + [1] for row in input_matrix]
tab.append([-1]*matrix_cols + [0]*(matrix_rows+1))


def print_tableau(tab):
    print(*tab, sep='\n')

print_tableau(tab)
