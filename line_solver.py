from fractions import Fraction
import matplotlib.pyplot as plt 
import itertools
import numpy as np

def rotate_matrix(mat):
    return list(zip(*mat[::-1]))

def frac(num):
    return Fraction(num).limit_denominator()

def linear_solve(mat,plot = False):
    m = len(mat[0])
    n = len(mat)
    if m != 2 and n != 2:
        raise Exception(f"Invalid matrix provided. Expect Nx2 or 2xM and got {m}x{n}")
    else:
        op = None
        op2 = None
        var_name = ""
        if m == 2:
            
            def op(a,b):
                return a <= b
            def op2(a,b):
                return a > b
            var_name = "q"
        else: # n == 2
            mat = [mat[1],mat[0]]
            mat = rotate_matrix(mat)
            def op(a,b):
                return a >= b
            def op2(a,b):
                return a < b
            var_name = "p"

        #q=(D-B)/(A-B-C+D)
        intercepts = []
        for combo_mat in itertools.combinations(mat, 2):
            a = combo_mat[0][0]
            b = combo_mat[0][1]
            c = combo_mat[1][0]
            d = combo_mat[1][1]
            q = frac((d-b)/(a-b-c+d))
            v = (a*q)+(b*(1-q))
            if q >= 0 and q <= 1:
                intercepts.append((q,v))

        passing_tuples = []
        for q,v in intercepts:
            passed = 0
            for line in mat:
                if op((line[0]*q)+(line[1]*(1-q)),v):
                    passed += 1
            if passed == len(mat):
                if len(passing_tuples) == 0:
                    passing_tuples.append((q,v))
                elif op2(passing_tuples[0][1],v):
                    passing_tuples = []
                    passing_tuples.append
                elif passing_tuples[0][1] == v:
                    passing_tuples.append((q,v))
        
        print(f"{var_name},v values:")
        for q,v in passing_tuples:
            print(f"{var_name} =",q,"v =",v)

        if plot:
            with plt.ion():
                for index,line in enumerate(mat):
                    #Aq+B(1-q)
                    #(A-B)q+B
                    a = line[0]
                    b = line[1]
                    slope = a-b
                    intercept = b
                    axes = plt.gca()
                    x_vals = np.array(axes.get_xlim())
                    y_vals = intercept + slope * x_vals
                    plt.plot(x_vals, y_vals,label=f"line {index+1}")
                    plt.plot(0, intercept, marker="o")
                
                for q,v in intercepts:
                    plt.plot(q, v, marker="o")
                
                plt.xlabel(var_name)
                plt.ylabel("v")
                plt.legend(loc="upper left")
        
            plt.show()

#EXAMPLE

if __name__ == '__main__':
    mat = eval(input('Enter the game matrix: '))
    graph = False
    if (input("Graph the output lines? [y/N]: ").lower()[:1] == 'y'):
        graph = True
    linear_solve(mat,graph)
