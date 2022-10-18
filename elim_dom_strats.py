def elim_dom_strats(mat, verbose=False):
    # Loop until there are no more domm'd rows/cols to find
    more_to_find = True
    while more_to_find:
        more_to_find = False

        # Loop through every row
        for r in range(len(mat)):
            whole_row_dommed = True

            # Check that every col in this row is domm'd
            for c in range(len(mat[r])):
                col_dommed = False

                # Check all other rows at same col to find dom
                for r2 in range(len(mat)):
                    if r == r2:
                        continue

                    # row r is domm'd at this col
                    if mat[r][c] <= mat[r2][c]:
                        col_dommed = True
                        break
                # If row r is not domm'd at 1 col, it is not domm'd
                if not col_dommed:
                    whole_row_dommed = False
                    break

            # If the entire row is domm'd remove it
            if whole_row_dommed:
                mat = mat[:r] + mat[r+1:]
                more_to_find = True # There may be more stuff to find
                if verbose:
                    print('Remove dom\'d r{}:'.format(r+1), mat)
                break

        for c in range(len(mat[0])):
            whole_col_dommed = True
            for r in range(len(mat)):
                row_dommed = False
                for c2 in range(len(mat[0])):
                    if c == c2:
                        continue
                    if mat[r][c] >= mat[r][c2]:
                        row_dommed = True
                        break
                if not row_dommed:
                    whole_col_dommed = False
                    break

            if whole_col_dommed:
                for r in range(len(mat)):
                    mat[r] = mat[r][:c] + mat[r][c+1:]
                more_to_find = True
                if verbose:
                    print('Remove dom\'d c{}:'.format(c+1), mat)
                break

    return mat

if __name__ == '__main__':
    mat = eval(input("Enter the game matrix:\n"), verbose=True)

    mat = elim_dom_strats(mat)

    print()
    print('Result:')
    print(*mat, sep='\n')
