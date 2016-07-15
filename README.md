# Feature Selection Methods for Learning to Rank

> Open sourced implementation of [this paper](http://www.ceng.metu.edu.tr/~altingovde/pubs/n.pdf):
**Exploiting Result Diversification Methods
for Feature Selection in Learning to Rank** 



Following 5 methods of feature selection for LTR have been implemented:

 * MMR (**M**aximal **M**arginal **R**elevance)
 * MSD (**M**aximum **S**um **D**ispersion)
 * MPT (**M**odern **P**ortfolio **T**heory)
 * GAS (**G**reedy **S**earch **A**lgorithm)
 * TopK 


### Installation

I will assume that you have python 2.7 installed. Remaining requirements are written in `requirements.txt`
```
pip install -r requirements.txt
```
You will also need appropriate binary of `trec_eval` available in your `PATH` variable. The following steps might be helpful:
```
git clone https://github.com/usnistgov/trec_eval.git
cd trec_eval
make # this should generate binary of trec_eval
sudo chmod +x trec_eval
sudo cp trec_eval /bin/ 
```

Finally, just clone this repo and check next section to see how to use it.
```
git clone https://github.com/HarshTrivedi/feature-selection-for-learning-to-rank.git
```

---


### Usage

I will assume that you have your training and testing data in `svm_light` format. You can get the details [here](http://svmlight.joachims.org/). In home directory of this repo, there are `trainingset.txt` and `testset.txt` for sample purpose. 
So you will need to have following files of yours which need to be replaced for your usage:

* trainingset.txt
* testset.txt
* qrels.qrel 

Once the input files are replaced, you need to set some configurations for the run. They can be set in `config.py` file. Following parameters are tunable:

```python
# example configurations
total_number_of_features = 45
n = [10, 15, 20, 25, 30]
methods = ["msd", "mpt", "mmr", "gas", "topk" ]
balancing_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
measure = "ndcg" # ndcg or map
```
Config Details:
* `total_number_of_features`: total number of features in your dataset.
* `n`: list of number of features to be selected
* `methods`: list of methods you want to use in this run
* `balancing_factors`: each of the first 4 methods use a balancing factor [0, 1] which is essentially a balance between importance of selected features and diversity among this set. So its a list of balancing_factors to be used.
* `measure`: quantity that will be used for measuring importance of feature. 

With this configuration, you will have list of selected features for each method from `methods` using each of the balancing facotr from `balancing_factors` and for each k in n.

Once this is done, following scripts need to be run sequentially:

* `1.preprocess.py`
* `2.select_features.py`
* `3.generate_examples_from_generated_features.py`

As a result, you will have following 5 additional directories now:

* features_selected
* rankings
* query_wise_rankings
* ranking_scores
* feature_selected_example_files

You would mainly be interested in 2 directories: `features_selected` and `feature_selected_example_files`. The former has the list of features selcted for each combination configuration from `config.py`. The later has the various versions of `trainingset.txt` and `testset.txt` (containing only the selected features) - each correspond to one of the combination configuration.


---

<br><br>
In case you plan to use it in your research, please cite the above paper using:

```
@inproceedings{naini2014exploiting,
  title={Exploiting result diversification methods for feature selection in learning to rank},
  author={Naini, Kaweh Djafari and Altingovde, Ismail Sengor},
  booktitle={European Conference on Information Retrieval},
  pages={455--461},
  year={2014},
  organization={Springer}
}
```


Please Note: I am NOT any of the authors of of the paper. So, if you want you can consider to verify the implementation yourself!

In case of any problem, please contact me at: harshjtrivedi94@gmail.com

Hope you find it useful : )