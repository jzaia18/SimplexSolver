# Find all Nash equilibria in a given matrix
def find_nash(mat):
    for r in range(len(mat)):
        for c in range(len(mat[r])):
            # Checking position (r, c)
            state1 = mat[r][c]
            failed = False

            # See if any elem is prefered for P1
            for r2 in range(len(mat)):
                state2 = mat[r2][c]
                # If this player prefers another state, state1 is not a Nash equilibrium
                if state2[0] > state1[0]:
                    failed = True
                    break

            # See if any elem is prefered for P2
            for c2 in range(len(mat[r])):
                state2 = mat[r][c2]
                # If this player prefers another state, state1 is not a Nash equilibrium
                if state2[1] > state1[1]:
                    failed = True
                    break

            if not failed:
                print("Nash equilibrium found at r{} c{}: ".format(r + 1, c + 1), mat[r][c])

# Find all Pareto optimal states in a given matrix
def pareto_optimal(mat):
    for r in range(len(mat)):
        for c in range(len(mat[r])):
            # Checking position (r, c)
            state1 = mat[r][c]

            failed = False

            for r2 in range(len(mat)):
                for c2 in range(len(mat[r2])):
                    if r == r2 and c == c2: continue
                    state2 = mat[r2][c2]

                    # If both players prefer state 2, then state 1 cannot be pareto optimal
                    if state2[0] >= state1[0] and state2[1] >= state1[1]:
                        failed = True
                        break

                if failed: break

            if not failed:
                print("Pareto optimal outcome found at r{} c{}: ".format(r + 1, c + 1), mat[r][c])

if __name__ == '__main__':
    mat = eval(input("Enter the matrix: "))

    find_nash(mat)
    print()
    pareto_optimal(mat)
