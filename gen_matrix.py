def buildmatrix(rows, cols, args):
    if len(args) != rows*cols:
        raise Exception(f"Incorrect number of args provided! Expected {rows*cols} and got {len(args)}")

    mat = []
    for i in range(rows):
        row = []
        for ii in range(cols):
            row.append(args[i*cols+ii])

        mat.append(row)
    return mat

def buildmatrix_nzs(rows, cols, args):
    if len(args) != rows*cols*2:
        raise Exception(f"Incorrect number of args provided! Expected {rows*cols*2} and got {len(args)}")
    mat = []

    for i in range(rows):
        row = []
        for ii in range(0,cols*2,2):
            row.append((args[(i*cols*2)+ii],args[(i*cols*2)+ii+1]))

        mat.append(row)
    return mat

if __name__ == '__main__':
    non_zero_sum = input('Should this matrix be zero-sum? [Y/n]')[:1].lower() == 'n'

    mat_rows = int(input('Enter the number of rows: '))
    mat_cols = int(input('Enter the number of cols: '))

    vals = []

    loop = mat_rows * mat_cols
    if non_zero_sum:
        loop *= 2

    for i in range(loop):
        vals.append(int(input("Enter a value: ")))

    if non_zero_sum:
        print(buildmatrix_nzs(mat_rows, mat_cols, vals))
    else:
        print(buildmatrix(mat_rows, mat_cols, vals))
