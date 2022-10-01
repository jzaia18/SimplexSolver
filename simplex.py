from fractions import Fraction

VERBOSE = True

# Print a tableau in a neat format
def print_tableau(tab):
    #print(*[[str(x) for x in row] for row in tab], sep='\n')

    for row in tab[:-1]:
        for elem in row[:-1]:
            print('{:8s}'.format(str(elem)), end='')
        print('│{:8s}'.format(str(row[-1])))

    print('─'*(tableau_cols-1)*8, end='')
    print('┼', end='')
    print('─'*7)
    for elem in tab[-1][:-1]:
        print('{:8s}'.format(str(elem)), end='')
    print('│{:8s}'.format(str(tab[-1][-1])))


def compute_next_tableau(prev_tab):
    # Copy previous tableau
    next_tab = [[elem for elem in row] for row in prev_tab]

    # Find minimum in bottom row
    minval = min(prev_tab[-1])
    if minval >= 0:
        return None

    # Assign pivot column
    pivot_col = prev_tab[-1].index(minval)
    pivot_row = 0

    # Determine pivot row
    for r in range(matrix_rows):
        curr_row_val = prev_tab[r][-1]/prev_tab[r][pivot_col]
        curr_pivot_val = prev_tab[pivot_row][-1]/prev_tab[pivot_row][pivot_col]

        if curr_pivot_val < 0 or (curr_row_val > 0 and curr_row_val < curr_pivot_val):
            pivot_row = r

    if VERBOSE: print('Pivot chosen: ({}, {})\n'.format(pivot_row + 1, pivot_col + 1))

    # Find new value for pivot row
    for c in range(tableau_cols):
        next_tab[pivot_row][c] /= prev_tab[pivot_row][pivot_col]

    # Compute all other rows based on pivot value
    for r in range(tableau_rows):
        if r == pivot_row:
            continue

        for c in range(tableau_cols):
            next_tab[r][c] -= prev_tab[r][pivot_col] * next_tab[pivot_row][c]

    return next_tab

if __name__ == '__main__':
    input_matrix = eval(input("Enter your matrix:\n"))

    matrix_rows = len(input_matrix)
    matrix_cols = len(input_matrix[0])

    tableau_rows = matrix_rows + 1
    tableau_cols = matrix_rows + matrix_cols + 1

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
    tab = [[Fraction(elem) for elem in row] for row in tab]

    # Keep generating tableaus until no more can be created
    while tab is not None:
        print_tableau(tab)

        tab = compute_next_tableau(tab)
