from sampler_general_ex import *
import time
import pickle
import numpy
import networkx as nx
import sampling_utils as su
import matplotlib.pyplot as plt
import OBDsearch

graph_file_name = "/home/irma/workspace/dblp_graphs_proba/DATA/Dblp/Dblp.gpickle"
short_graph_file_name = "patt7"
pattern_file_name = "/home/irma/workspace/dblp_graphs_proba/PATTERNS/patterns_size_4/batch1/patt7/patt7.gml" # BEWARE: change below ALSO the Plist, OBdecomp and root-target AND fdict_ex pickle file !!!
D = nx.read_gpickle(graph_file_name)
P = nx.read_gml(pattern_file_name)
root_nodes = [x for x in D.nodes() if D.node[x]['predicate']=='coauthored']


OBdecomp = OBDsearch.get_heuristic4_OBD(P, startNode = 2)
Plist = [item for sublist in OBdecomp for item in sublist]

print "Using OBD: %s" % str(OBdecomp)
print "and Plist: %s" % str(Plist)
## Plist = [0,1,2,7,3,4,5,6,8,9]
## OBdecomp = [ [0], [1] , [2], [7, 3, 4], [5] , [6], [8], [9]]


start=time.time()
fdict_exhaustive_inf = sampling_exhaustive_general_inf(D,  P,  Plist,  root_nodes)
stop=time.time()
fdict_exhaustive = fdict_exhaustive_inf[0]

infofile = open('_info.txt',  'w')
infofile.write("Exhaustive procedure took %d seconds.\n" % int(stop-start))
infofile.write("Total number of observations: %d \n"  % fdict_exhaustive_inf[1])
infofile.write("Number of combinations: %d \n" % len(fdict_exhaustive))

sum = 0
for k in fdict_exhaustive.keys():
    sum = sum + fdict_exhaustive[k]

infofile.write("Number of embeddings: %d \n" % sum)
infofile.write("Frequencies in combinations:\n")

flist = []
for k in fdict_exhaustive.keys():
    flist.append(fdict_exhaustive[k])

infofile.write("minimum: %d \n" % min(flist))
infofile.write("maximum: %d \n" % max(flist))
infofile.write("mean: %d \n" % numpy.mean(flist))
infofile.write("median: %d \n" % numpy.median(flist))

print "Info done, now pickling..."              #-#########--PICKLING

D = nx.read_gpickle(graph_file_name)
P = nx.read_gml(pattern_file_name)

start=time.time()
fdict_exhaustive = sampling_exhaustive_general2(D,  P,  Plist,  root_nodes)
stop=time.time()

picklename = "fdict_exhaustive_%s.pickle" % short_graph_file_name

pickout = open(picklename, 'wb')
pickle.dump(fdict_exhaustive, pickout)
pickout.close()

timepickout = open("extime.pickle", 'wb')
extime= []
extime.append(stop-start)
pickle.dump(extime, timepickout)
timepickout.close()


print "Finished: infoed and pickled %s" % short_graph_file_name

