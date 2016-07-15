import numpy as np
import os

def var_rel(ranking_scores_directory, feature_numbers, query_ids):
    var_list = []
    avg_list = []
    for j in sorted(feature_numbers):
        fname = os.path.join( ranking_scores_directory, "F{}.txt".format(j) )
        scorefile = open(fname,'r')
        score_list = []
        for line in scorefile:
            a=line.split()
            score_list.append(float(a[2]))
            
        b=[]
        for i in range(len(query_ids)):
            b.append(score_list[i])
        imp = score_list[len(query_ids)]
        s = np.std(b, ddof=1)  
        v=s*s
        var_list.append(v)
        avg_list.append(imp)
    return ( avg_list, var_list)

  
    
    
