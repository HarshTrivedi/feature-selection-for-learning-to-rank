import sys
sys.path.insert(0, 'lib')
import kendals_tau
import findvar
import mmr
import mpt
import msd
import gas
import topk
import glob
import os
from config import *


root_directory = os.path.join(os.getcwd()  )
output_directory = os.path.join( root_directory, "features_selected")

for balancing_factor in balancing_factors:
	print "About to start with balancing factor: {}".format(balancing_factor)
	if "gas" in methods:
		print "starting method: gas"
		ranked_features = gas.select( os.path.join(root_directory, "query_wise_rankings"), os.path.join(root_directory, "ranking_scores"), total_number_of_features, balancing_factor)
		print ranked_features
		with open(os.path.join(output_directory, "gas_{}.ranking".format(balancing_factor) ), "w") as gas_feature_selection_file:
			gas_feature_selection_file.write(  "\n".join(map( str, ranked_features))  )
	if "mmr" in methods:
		print "starting method: mmr"
		ranked_features = mmr.select( os.path.join(root_directory, "query_wise_rankings"), os.path.join(root_directory, "ranking_scores"), total_number_of_features, balancing_factor)
		print ranked_features
		with open(os.path.join(output_directory, "mmr_{}.ranking".format(balancing_factor) ), "w") as mmr_feature_selection_file:
			mmr_feature_selection_file.write(  "\n".join(map( str, ranked_features))  )
	if "mpt" in methods:
		print "starting method: mpt"
		ranked_features = mpt.select( os.path.join(root_directory, "query_wise_rankings"), os.path.join(root_directory, "ranking_scores"), total_number_of_features, balancing_factor)
		print ranked_features
		with open(os.path.join(output_directory, "mpt_{}.ranking".format(balancing_factor) ), "w") as mpt_feature_selection_file:
			mpt_feature_selection_file.write(  "\n".join(map( str, ranked_features))  )
	if "msd" in methods:
		print "starting method: msd"
		ranked_features = msd.select( os.path.join(root_directory, "query_wise_rankings"), os.path.join(root_directory, "ranking_scores"), total_number_of_features, balancing_factor)
		print ranked_features
		with open(os.path.join(output_directory, "msd_{}.ranking".format(balancing_factor) ), "w") as msd_feature_selection_file:
			msd_feature_selection_file.write(  "\n".join(map( str, ranked_features))  )
	if "topk" in methods:
		print "starting method: topk"
		ranked_features = topk.select( os.path.join(root_directory, "query_wise_rankings"), os.path.join(root_directory, "ranking_scores"), total_number_of_features, balancing_factor)
		print ranked_features
		with open(os.path.join(output_directory, "topk_{}.ranking".format(balancing_factor) ), "w") as topk_feature_selection_file:
			topk_feature_selection_file.write(  "\n".join(map( str, ranked_features))  )
