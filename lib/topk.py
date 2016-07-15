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
        feat_subset.append(max_feature)
            
    return (feat_subset)    


def find_max(score_data):
    ind = score_data.index(max(score_data))
    score_data[ind] = float("-inf")
    return (ind+1,score_data)