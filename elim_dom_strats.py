def elim_dom_strats(mat, verbose=False):
    # Loop until there are no more domm'd rows/cols to find
    more_to_find = True
    while more_to_find:
        more_to_find = False

        # Loop through every row
        for r in range(len(mat)):
            dommed = False

            # Check all other rows find dom row
            for r2 in range(len(mat)):
                if r == r2:
                    continue

                dommed = True
                # Check that every col in this row dom's
                for c in range(len(mat[r])):
                    # if row r is not domm'd at this col, exit early
                    if mat[r][c] > mat[r2][c]:
                        dommed = False
                        break

                # If a row is dominated, we can exit this loop early
                if dommed: break

            # If the entire row is domm'd remove it
            if dommed:
                mat = mat[:r] + mat[r+1:]
                more_to_find = True # There may be more stuff to find
                if verbose:
                    print('Remove dom\'d r{}, mat:'.format(r+1), mat)
                break

        # Loop through every column
        for c in range(len(mat[0])):
            dommed = False

            # Check all other columns to find dom column
            for c2 in range(len(mat[0])):
                if c == c2:
                    continue

                dommed = True
                # Check that every row in this column dom's
                for r in range(len(mat)):
                    # If col c is not domm'd at this row, exit early
                    if mat[r][c] < mat[r][c2]:
                        dommed = False
                        break

                # If a col is dominated, we can exit this loop early
                if dommed: break

            if dommed:
                for r in range(len(mat)):
                    mat[r] = mat[r][:c] + mat[r][c+1:]
                more_to_find = True
                if verbose:
                    print('Remove dom\'d c{}, mat:'.format(c+1), mat)
                break

    return mat

if __name__ == '__main__':
    mat = eval(input("Enter the game matrix:\n"))

    mat = elim_dom_strats(mat, verbose=True)

    print()
    print('Result:')
    print(*mat, sep='\n')
