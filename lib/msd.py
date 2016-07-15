import sys
# sys.path.insert(0, 'lib')
import kendals_tau
import findvar
import numpy
import glob
import os
from awesome_print import ap
numpy.set_printoptions(threshold=numpy.nan)
def select( query_wise_rankings_directory, ranking_scores_directory, k, balancing_factor):
    feat_subset = []
    
    """To set the value of K (Number of features to be selected)
    """
    ranking_score_files = glob.glob(  os.path.join(ranking_scores_directory, "*")  )
    feature_numbers = map( lambda file_path: int(os.path.basename(file_path).replace("F", "").replace(".txt", "")) , ranking_score_files)

    query_wise_rankings_files = glob.glob( os.path.join(query_wise_rankings_directory, "*") )
    query_ids = list(set(map( lambda file_path: int(os.path.basename(file_path).split("q")[1]), query_wise_rankings_files)))

    cnt=0

    fscores, fvar = findvar.var_rel(ranking_scores_directory, feature_numbers, query_ids)

    No_of_features = len(feature_numbers)    
    scorematrix = numpy.zeros((No_of_features,No_of_features))
    
    for i in range(1, No_of_features+1):
        for j in range(i+1, No_of_features+1):
            val = calcmsdVal(i,j,fscores[i-1],fscores[j-1], query_wise_rankings_directory, feature_numbers, query_ids, balancing_factor)
            scorematrix[i-1][j-1] = val
            scorematrix[j-1][i-1] = val

    # print scorematrix

    while cnt<=k:
        """ Find max pair"""
        row,column = numpy.unravel_index(scorematrix.argmax(), scorematrix.shape)
        
        for i in range(0,No_of_features):
            scorematrix[i][row] = float("-inf")
            scorematrix[row][i] = float("-inf")
        for j in range(0,No_of_features):
            scorematrix[j][column] = float("-inf")
            scorematrix[column][j] = float("-inf")
            
        feat_subset.append(row+1)
        feat_subset.append(column+1)    
        cnt=cnt+2

        
    return (feat_subset[0:k])    
           
          
def calcmsdVal(k, l, relk, rell, query_wise_rankings_directory, feature_numbers, query_ids, balancing_factor):
    """To find the top 10 documents when retrieving using feature k
    """
    fkList_doc = []
    
    for q in query_ids:
        x = []
        qryfile = os.path.join(query_wise_rankings_directory, "f{}q{}".format(k, q) )
        fk = open(qryfile, 'r')
        start = str(q) + " "
        for i in range(10):
             line = fk.next().strip()
             if line.startswith(start):
                 a = line.split()
                 x.append(int(a[2]))
        fkList_doc.append(x)
      
    """ Fetching the top documents for the feature f(l)
    """
    flList_doc = []
    for q in query_ids:
        x = []
        qryfile = os.path.join(query_wise_rankings_directory, "f{}q{}".format(l, q) )
        fl = open(qryfile, 'r')
        start = str(q) + " "
        for i in range(10):
             line = fl.next().strip()
             if line.startswith(start):
                 a = line.split()
                 x.append(int(a[2]))
        flList_doc.append(x)
    
                
    tauSum = 0
    for avg in range(0, len(query_ids)):
        t = kendals_tau.tau_distance(fkList_doc[avg], flList_doc[avg])
        tauSum = tauSum + t
    tauAvg = float(tauSum) / len(query_ids)
    msdval = ((1-balancing_factor)*(relk+rell)) + (2*balancing_factor*(1-tauAvg))
    return msdval
