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

def translate_example_file_with_selected_features(source_examples_file_path, target_examples_file_path, feature_numbers):
	target_examples_file = open(target_examples_file_path, "w")
	with open(source_examples_file_path) as source_example_file:
		for source_line in source_example_file:
			array = source_line.strip().split(" ")
			final_array = []
			relevance_and_query_id_text = array[0:2] 
			featured_items = filter( lambda element: ((":" in element) and ("qid" not in element)), array[2:])
			selected_features_text = filter(lambda element: int(element.split(":")[0]) in feature_numbers, featured_items)
			document_id = array[-1]
			final_array.extend(relevance_and_query_id_text)
			final_array.extend(selected_features_text)
			final_array.extend(["#docid =", document_id])
			updated_line = " ".join(final_array)
			target_examples_file.write(updated_line + "\n")
	target_examples_file.close()

#### --------------------------------------------------- ####
#### --------------------------------------------------- ####

	
root_directory = os.path.join(os.getcwd(), fold )
feature_selection_directory = os.path.join( root_directory, "features_selected")
for k in n:
	for balancing_factor in balancing_factors:		
		for method in methods:
			
			lines = open( os.path.join(feature_selection_directory, "{}_{}.ranking".format(method, balancing_factor) )).readlines()[:k]
			feature_numbers = map(lambda line: int(line.strip()), lines)
			### Translate Training Examples - Start ###
			source_examples_file_path = os.path.join( root_directory, "trainingset.txt")
			target_examples_file_path = os.path.join( root_directory, "feature_selected_example_files", "{}_{}_{}_training_examples.dat".format(method, k, balancing_factor))
			translate_example_file_with_selected_features(source_examples_file_path, target_examples_file_path, feature_numbers)
			### Translate Training Examples - Complete ###			
			### Translate Testing Examples - Start ###
			source_examples_file_path = os.path.join( root_directory, "testset.txt")
			target_examples_file_path = os.path.join( root_directory, "feature_selected_example_files", "{}_{}_{}_testing_examples.dat".format(method, k, balancing_factor))			
			translate_example_file_with_selected_features(source_examples_file_path, target_examples_file_path, feature_numbers)
			### Translate Testing Examples - Complete ###
