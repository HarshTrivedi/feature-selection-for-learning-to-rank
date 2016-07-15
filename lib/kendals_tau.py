import itertools
#from  more_itertools import unique_everseen


def tau_distance(list1, list2):
	
	list1 = map(str, list1)
	list2 = map(str, list2)
	x = list( itertools.combinations( list1 ,2) )
	y = list( itertools.combinations( list2 ,2) )

	x = map(lambda e: list(e), x)
	y = map(lambda e: list(e), y)

	number_of_cordant_pairs = 0
	#print x
	#print y
	for item in x:
		if list(item) in y:
			number_of_cordant_pairs += 1

	for item in y:
		if list(item) in x:
			number_of_cordant_pairs += 1

	number_of_cordant_pairs = number_of_cordant_pairs/2

	total_list = []
	total_list.extend(x)
	total_list.extend(y)

	total_list = map( lambda x: ':'.join(sorted(x)), total_list)
	total_list = list(set(total_list))
	n = len(total_list)
	tau_distance = number_of_cordant_pairs/float(n)
	return tau_distance


#list1 = ['a', 'b']
#list2 = ['a', 'b']

# list1 = [1,2,3,4,5,6,7,8,9,10,11,12]
# list2 = [2,1,4,3,6,5,8,7,10,9,12,11]

#print tau_distance(list1, list2)


