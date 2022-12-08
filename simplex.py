from elim_dom_strats import elim_dom_strats
from fractions import Fraction

# Options for making the output more friendly
VERBOSE = True
LATEX = False

# Print the tableau in whichever format is currently globally selected
def print_tableau(tab):
    if LATEX:
        print_tableau_latex(tab)
    else:
        print_tableau_text(tab)

# Print a tableau in a neat text format
def print_tableau_text(tab):
    # Print tableau header
    print('    ', end='')
    for c in range(matrix_cols):
        print('x{}      '.format(c+1), end='')
    for c in range(matrix_rows):
        print('s{}      '.format(c+1), end='')
    print()
    print('──┼─', end='')
    print('─'*8*(matrix_cols+matrix_rows), end='')
    print('┼───────')

    # Print main rows of tableau
    r = 0
    for row in tab[:-1]:
        # Print row label
        if r in used_rows:
            print('x{}│ '.format(used_rows.index(r) + 1), end='')
        else:
            print('s{}│ '.format(r + 1), end='')
        r += 1

        # Print main row contents
        for elem in row[:-1]:
            print('{:8s}'.format(str(elem)), end='')

        # Print far right column
        print('│{:8s}'.format(str(row[-1])))

    # Print bottom row
    print('──┼─', end='')
    print('─'*(tableau_cols-1)*8, end='')
    print('┼', end='')
    print('─'*7)
    print('  │ ', end='')
    for elem in tab[-1][:-1]:
        print('{:8s}'.format(str(elem)), end='')
    print('│{:8s}'.format(str(tab[-1][-1])))

# Print a tableau in a neat format for latex
def print_tableau_latex(tab):
    # Print necessary LaTeX setup
    print('\\begin{table}[!h]')
    print('  \\centering')
    print('  \\begin{tabular}{r |' + 'c '*(tableau_cols-1) +  '| c}')

    # Print the tableau heading
    print('    \\textbf{B}', end='')
    for i in range(matrix_cols):
        print(' & $X_{}$'.format(i+1), end='')
    for i in range(matrix_rows):
        print(' & $S_{}$'.format(i+1), end='')
    print(' & \\\\')
    print('    \\hline')

    # Print the main rows of the tableau
    r = 0
    for row in tab[:-1]:
        # Print the column labels
        if r in used_rows:
            print('    $X_{}$'.format(used_rows.index(r) + 1), end='')
        else:
            print('    $S_{}$'.format(r + 1), end='')
        r += 1

        # Print the main row body
        for elem in row:
            if elem.denominator == 1:
                print(' & ${}$'.format(elem.numerator), end='')
            else:
                print(' & $\\frac{{{}}}{{{}}}$'.format(elem.numerator, elem.denominator), end='')
        print('\\\\')

    # Print the final row
    print('    \\hline')
    print('         ', end='')
    for elem in tab[-1]:
        if elem.denominator == 1:
            print(' & ${}$'.format(elem.numerator), end='')
        else:
            print(' & $\\frac{{{}}}{{{}}}$'.format(elem.numerator, elem.denominator), end='')

    # More LaTeX cleanup
    print()
    print('  \\end{tabular}')
    print('\\end{table}')

# Compute the next tableau given the current one
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

        # Only use a row if it is the smallest positive one found that is in a row that hasn't already been used
        if curr_pivot_val < 0 or pivot_row in used_rows or (curr_row_val > 0 and curr_row_val < curr_pivot_val and r not in used_rows):
            pivot_row = r

    # Mark this row as used (needed for labeling)
    if pivot_col < matrix_cols:
        used_rows[pivot_col] = pivot_row
    if VERBOSE: print('\nPivot chosen: ({}, {})\n'.format(pivot_row + 1, pivot_col + 1))

    # Find new value for pivot row
    for c in range(tableau_cols):
        next_tab[pivot_row][c] /= prev_tab[pivot_row][pivot_col]

    # Compute all other rows based on pivot value
    for r in range(tableau_rows):
        if r == pivot_row:
            continue

        # Compute the new row values by subtracting the multiple of the pivot row
        for c in range(tableau_cols):
            next_tab[r][c] -= prev_tab[r][pivot_col] * next_tab[pivot_row][c]

    return next_tab

if __name__ == '__main__':
    # Prompt the user for a matrix
    matrix = eval(input("Enter your matrix:\n"))

    # Ask the user if they want to eliminate dominated strategies
    if (input("Use elimination of dominated strategies [y/N]:").lower()[:1] == 'y'):
        matrix = elim_dom_strats(matrix, verbose=VERBOSE)

    # Determine the number of rows/cols in the input
    matrix_rows = len(matrix)
    matrix_cols = len(matrix[0])

    # Initialized used rows list
    used_rows = [-1]*matrix_cols

    # Determine the number of tableau rows/cols
    tableau_rows = matrix_rows + 1
    tableau_cols = matrix_rows + matrix_cols + 1

    # Normalize matrix
    smallest = min([min(row) for row in matrix])
    increment = 0
    if smallest <= 0:
        increment = -smallest + 1

        # Apply normalization onto matrix
        matrix = [[elem + increment for elem in row] for row in matrix]

    # Extend rows and cols to make tableau shape
    tab = [row + [0]*(matrix_rows) + [1] for row in matrix]
    tab.append([-1]*matrix_cols + [0]*(matrix_rows+1))

    # Fill in identity matrix
    for offset in range(matrix_rows):
        tab[offset][matrix_cols+offset] = 1

    # Convert all numbers to fractions for ease of computation
    tab = [[Fraction(elem) for elem in row] for row in tab]

    # Keep generating tableaus until no more can be created
    last_tab = tab
    num_tabs = 0
    while tab is not None:
        print_tableau(tab)

        # Stop going when there are no more rows with which to solve
        #if num_tabs >= matrix_rows:
        #    break

        tab = compute_next_tableau(tab)
        if tab is not None:
            last_tab = tab.copy()
        num_tabs += 1

    # Print out game value
    print()
    print("Normalization increment = ", increment)
    print("Value of the game: ", 1/(last_tab[-1][-1]) - increment)

    # Determine optimal player strategies
    player1_strat = last_tab[-1][matrix_cols:-1]
    player1_strat = [x/last_tab[-1][-1] for x in player1_strat]
    player2_strat = [0]*matrix_cols

    # Calculate player 2 strategies based on used rows (ignore unused)
    for i in range(len(used_rows)):
        r = used_rows[i]
        if r != -1:
            player2_strat[i] = last_tab[r][-1]/last_tab[-1][-1]

    # Display optimal strategies
    player1_strat = [str(frac) for frac in player1_strat]
    player2_strat = [str(frac) for frac in player2_strat]
    print("Player 1 optimal strategy: ", player1_strat)
    print("player 2 optimal strategy: ", player2_strat)
