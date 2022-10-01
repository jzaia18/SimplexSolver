from fractions import Fraction

# Print a tableau in a neat format
def print_tableau(tab):
    print(*tab, sep='\n')



if __name__ == '__main__':
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

    # Fill in identity matrix
    for offset in range(matrix_rows):
        tab[offset][matrix_cols+offset] = 1

    # Convert all numbers to fractions for ease of computation
    tab = [[Fraction(elem) for elem in row] for row in input_matrix]

    print_tableau(tab)
