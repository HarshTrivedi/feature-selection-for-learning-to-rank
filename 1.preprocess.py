import os
import sys
from config import *

def pluck_feature_and_generate_ranking_file(input_example_file, target_directory,  feature_number):

	line_count = sum(1 for line in open(input_example_file))

	with open("Q0", "w") as q0_file:
		for _ in xrange(line_count): q0_file.write("Q0\n")

	with open("rank", "w") as rank_file:
		for i in xrange(line_count): rank_file.write(str(i+1) + "\n")

	with open("label", "w") as label_file:
		for _ in xrange(line_count): label_file.write("Feature{}\n".format(feature_number))

	os.system(" cut -d' ' -f2 {} | cut -d':' -f2 > query_ids ".format(input_example_file))
	os.system(" rev {} | cut -d' ' -f1 | rev | tr -d '\r'> document_ids".format(input_example_file))
	os.system(" cut -d' ' -f{} {} | cut -d':' -f2 > feature_values".format(feature_number + 2, input_example_file) )

	output_file_path = os.path.join(target_directory, "Feature{}".format(feature_number) )
	os.system("paste -d' ' query_ids Q0 document_ids rank feature_values label | sort -k1,1n -k5,5gr > {}".format(output_file_path))
	os.remove("query_ids")
	os.remove("Q0")
	os.remove("document_ids")
	os.remove("rank")
	os.remove("feature_values")
	os.remove("label")


def split_ranking_file_feature_wise(source_directory, target_directory, feature_number):
	ranking_file = os.path.join(source_directory, "Feature{}".format(feature_number) )

	query_ids = set(map(lambda x: int((x.split(" ")[0]) ), open( ranking_file,'r').readlines()  ) )
	for query_id in query_ids:
		lines = filter( lambda x: x.startswith("{} ".format(query_id)), open(ranking_file, "r").readlines())
		file = open( os.path.join(target_directory, "f{}q{}".format(feature_number, query_id)), "w")
		file.writelines(lines)
		file.close()


def evaluate_ranking_file(source_directory, target_directory, feature_number, qrel_file_path):
	ranking_file = os.path.join(source_directory, "Feature{}".format(feature_number) )
	output_file_path = os.path.join(target_directory, "F{}.txt".format(feature_number) )
	command = "trec_eval -q -m '{}' {} {} > {}".format(measure, qrel_file_path, ranking_file, output_file_path)
	os.system(command)



root_directory = os.getcwd()
paths = [] # clean paths required in root directory for preprocessing
paths.append( os.path.join( root_directory, "rankings" ))
paths.append((os.path.join( root_directory, "query_wise_rankings" ) ))
paths.append(os.path.join( root_directory, "ranking_scores" ))
paths.append(os.path.join( root_directory, "feature_selected_example_files" ))
paths.append(os.path.join( root_directory, "features_selected" ))

for path in paths:
	if os.path.exists(path): os.system("rm -rf {}".format(path))
	os.makedirs(path)

for feature_number in range(1, total_number_of_features + 1):
	print "About to process Feature {}".format(feature_number)
	
	input_example_file = os.path.join( root_directory, "trainingset.txt" )
	target_directory = os.path.join( root_directory, "rankings" )
	pluck_feature_and_generate_ranking_file(input_example_file, target_directory, feature_number)
	source_directory = os.path.join( root_directory, "rankings" )
	target_directory = os.path.join( root_directory, "query_wise_rankings" ) 
	split_ranking_file_feature_wise( source_directory, target_directory, feature_number, )
	qrel_file_path = "qrels.qrel"
	source_directory = os.path.join( root_directory, "rankings" )
	target_directory = os.path.join( root_directory, "ranking_scores" )
	evaluate_ranking_file(source_directory, target_directory, feature_number, qrel_file_path)		
	print "---------"
