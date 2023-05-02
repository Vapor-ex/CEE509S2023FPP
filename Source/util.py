import numpy as np
import math
import pandas as pd
import ast

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return int(math.ceil(n))

def decomp(n):
    # n is integer greater than 1
    ans = []
    if n == 1:
        ans.append([n])
    else:
        ans.append([n])
        for i in np.arange(1,n):
            ans_i = decomp(i)
            ans_ni = decomp(n-i)
            for j in np.arange(len(ans_i)):
                for k in np.arange(len(ans_ni)):
                    ans_jk = ans_i[j]+ans_ni[k]
                    ans.append(ans_jk)
        res = []
        [res.append(x) for x in ans if x not in res]
        ans = res
    return ans

def save_data(filename, data, shape=1):
    with open(filename, 'w') as f:

        if shape == 1:
            for row in data:
                f.write(str(row) + '\n')
        elif shape == 2:
            for row in data:
                f.write(' '.join([str(val) for val in row]) + '\n')

def read_result_csv(filename):
    read_result = pd.read_csv(filename)

    hL_star = read_result['Optimal Height']
    v_star = read_result['Optimal Value']
    scenario = read_result['Scenario']

    result = {
    'Optimal Height': [],
    'Optimal Value': [],
    'Scenario': []
    }
    result = pd.DataFrame(result)

    for i in np.arange(len(hL_star)):
        hLi = hL_star[i]
        hLi = hLi.replace('.',',')
        hLi = ast.literal_eval(hLi)
        vi = v_star[i]
        si = scenario[i]
        result_i = [hLi,vi,si]
        result.loc[i] = result_i

    return result
