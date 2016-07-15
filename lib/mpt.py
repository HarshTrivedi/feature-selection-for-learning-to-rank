import sys
# sys.path.insert(0, 'lib')
import glob
import os
import math
import findvar
import kendals_tau


def select( query_wise_rankings_directory, ranking_scores_directory, k, balancing_factor):    
    
    """ List of the importance scores of each feature
    """
    feat_subset = []
    
    """To set the value of K (Number of features to be selected)
    """
    ranking_score_files = glob.glob(  os.path.join(ranking_scores_directory, "*")  )
    feature_numbers = map( lambda file_path: int(os.path.basename(file_path).replace("F", "").replace(".txt", "")) , ranking_score_files)

    query_wise_rankings_files = glob.glob( os.path.join(query_wise_rankings_directory, "*") )
    query_ids = list(set(map( lambda file_path: int(os.path.basename(file_path).split("q")[1]), query_wise_rankings_files)))
    
    FkDocs = []    
    
    fscores, vx = findvar.var_rel(ranking_scores_directory, feature_numbers, query_ids)
    max_feature, fscores = find_max(fscores)
    feat_subset.append(max_feature)
    
    for cnt in range(k): 
        
        
        FkDocs = find_doclist(max_feature, FkDocs, query_wise_rankings_directory, query_ids)
        max_feature, fscores = upd_rel_score(FkDocs,fscores, feat_subset, ranking_scores_directory, query_wise_rankings_directory, feature_numbers, query_ids, balancing_factor)
        feat_subset.append(max_feature)
    
    #print "The features selected for MPT method are"
    return (feat_subset)
    
    
    
    
""" To find top 10 documents of newly added feature and append it to the old list  since at every step the 
    importance score of the remaining features is calculated based on all the features selected so far
"""
def find_doclist(max_feaure, FkDocs, query_wise_rankings_directory, query_ids):
    fiList_doc = []    
        
    for q in query_ids:
        x = []        
        qryfile = os.path.join(query_wise_rankings_directory, "f{}q{}".format(max_feaure, q) )

        fi = open(qryfile,'r')
        start = str(q) + " "
        for i in range(10):
             line=fi.next().strip()
             if line.startswith(start):
                 a = line.split()
                 x.append(int(a[2]))
        fiList_doc.append(x)  
    FkDocs.append(fiList_doc)     
    return FkDocs        
        
"""To find feature with maximum importance score
    Input: List of importance scores
    Output: feature with highest score
"""
def find_max(score_data):
    ind = score_data.index(max(score_data))
    score_data[ind] = float("-inf")
    return (ind+1,score_data)
   
"""This function is used to update the importance scores of the remaining features based on the last selected feature
   Input : Top 10 documents of all features selected so far,List of importance scores
   Output : Updated importance scores
"""   

def upd_rel_score(feat_subset, scores, feat_subset1, ranking_scores_directory, query_wise_rankings_directory, feature_numbers, query_ids, balancing_factor):
    """ Variances of each feature based on all queries"""
    scores_copy = scores
    a, fvar = findvar.var_rel(ranking_scores_directory, feature_numbers, query_ids)
       
    Fk = len(feat_subset)
        
    for j in feature_numbers:
        b=0.0000001
        fjList_doc = []
        if scores[j-1] != float("-inf"):        
            y = []          
                   
            for q in query_ids:
                y = []
                qryfile = os.path.join(query_wise_rankings_directory, "f{}q{}".format(j, q) )
                fj = open(qryfile,'r')
                start = str(q) + " "
                for k in range(10):
                    line=fj.next().strip()
                    if line.startswith(start):
                        a = line.split()
                        y.append(int(a[2]))
                fjList_doc.append(y)  
            
            """ To calculate sum of s.d of f(j) * sim(fi,fj) over all features selected so far"""
            Sim_sum = 0
            for d in range(0,Fk): 
                fiList_doc = feat_subset[d]
                tauSum = 0
                for avg in range(0,len(query_ids)):                
                    t = kendals_tau.tau_distance(fiList_doc[avg], fjList_doc[avg])
                    
                    tauSum = tauSum + t
                    
                tauAvg = tauSum / len(query_ids)
                prev_feature = feat_subset1[d]
                Sim_sum = Sim_sum + (math.sqrt(fvar[prev_feature - 1])*tauAvg)
            
            """ Update score based on formula for MPT"""
            scores[j-1] = scores[j-1] - ((balancing_factor*fvar[j-1]) + (2 * balancing_factor * math.sqrt(fvar[j-1]) * Sim_sum))
    
    t = scores.index(max(scores))
    scores_copy[t] = float("-inf")
    
    return (t+1, scores_copy)        
    

# select("query_wise_rankings", "ranking_scores", 4, 0.5)