import sys
# sys.path.insert(0, 'lib')
import scipy.stats as stats
import findvar
import glob
import os


def select( query_wise_rankings_directory, ranking_scores_directory, k, balancing_factor):
    """ List of the importance scores of each feature
    """
    feat_subset = []
    
    """To set the value of k (Number of features to be selected)
    """
    
    ranking_score_files = glob.glob(  os.path.join(ranking_scores_directory, "*")  )
    feature_numbers = map( lambda file_path: int(os.path.basename(file_path).replace("F", "").replace(".txt", "")) , ranking_score_files)

    query_wise_rankings_files = glob.glob( os.path.join(query_wise_rankings_directory, "*") )
    query_ids = list(set(map( lambda file_path: int(os.path.basename(file_path).split("q")[1]), query_wise_rankings_files)))

    fscores, fvar = findvar.var_rel(ranking_scores_directory, feature_numbers, query_ids)
    
    for cnt in range(k): 
        
        max_feature, fscores = find_max(fscores)

        """Add feature with highest importance score in the subset of selected features
        """
        feat_subset.append(max_feature)
        
        fscores = upd_rel_score(max_feature,fscores, query_wise_rankings_directory, feature_numbers, query_ids, balancing_factor)
    
    return (feat_subset)
    #print sorted(feat_subset)
    
"""To find feature with maximum importance score
    Input: List of importance scores
    Output: feature with highest score
"""
def find_max(score_data):
    ind = score_data.index(max(score_data))
    score_data[ind] = float("-inf")
    return (ind+1,score_data)
   
"""This function is used to update the importance scores of the remaining features based on the last selected feature
   Input : Last selected feature, List of importance scores
   Output : Updated importance scores
"""   
def upd_rel_score(maxf, scores, query_wise_rankings_directory, feature_numbers, query_ids, balancing_factor):
    
    """To find the top 10 documents when retrieving using feature x
    """
    fiList_doc = []
     
    
    """ Fetching the top documents for the feature f(i)
    """
        
    for q in query_ids:
        x = []
        qryfile = os.path.join(query_wise_rankings_directory, "f{}q{}".format(maxf, q) )
        fi = open(qryfile, 'r')
        start = str(q) + " "
        for i in range(10):
             line = fi.next().strip()
             if line.startswith(start):
                 a = line.split()
                 x.append(int(a[2]))
        fiList_doc.append(x)
        
    for j in feature_numbers:
        fjList_doc = []
        if( scores[j-1] != float("-inf")):
            y = []
        
            for q in query_ids:
                y = []
                qryfile = os.path.join(query_wise_rankings_directory, "f{}q{}".format(maxf, q) )
                fj = open(qryfile,'r')
                start = str(q) + " "
                for k in range(10):
                    line=fj.next().strip()
                    if line.startswith(start):
                        a = line.split()
                        y.append(int(a[2]))
                fjList_doc.append(y)  
                
            tauSum = 0
            for avg in range(0, len(query_ids)):
                #t = kendals_tau.tau_distance(fiList_doc[avg], fjList_doc[avg])
                t, p_value = stats.kendalltau(fiList_doc[avg], fjList_doc[avg])
                tauSum = tauSum + t
            tauAvg = float(tauSum) / len(query_ids)
            
            scores[j-1] = scores[j-1] - (tauAvg*2*balancing_factor)
    return scores


# select("query_wise_rankings", "ranking_scores", 4, 0.5)