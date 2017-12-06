
from sampler_general_ex import *
import OBDsearch
import time
import os
import pickle
import numpy
import networkx as nx
import sampling_utils as su
import matplotlib.pyplot as plt

start = time.time()



graph_file_name = "/home/irma/workspace/dblp_graphs_proba/DATA/Dblp/Dblp.gpickle"
short_graph_file_name = "patt7"
pattern_file_name = "patt7.gml" # BEWARE: change below ALSO the Plist, OBdecomp and root-target AND fdict_ex pickle file !!!
pattern_path="/home/irma/workspace/dblp_graphs_proba/PATTERNS/patterns_size_4/batch1/patt7/patt7.gml"
repetitions = 10

latex_file_name = "experiments_ICDM__" + short_graph_file_name + pattern_file_name+".x"+str(repetitions)+".latex"
latexfile = open(latex_file_name,  'a')
latexfile.write("\n\\begin{table}\n")
latexfile.write("\\centering\n")
latexfile.write("\\begin{tabular}{|l|l|r|c|c|c|r} \\hline \n")
latexfile.write("graph		& algorithm     & observed	& KLD   				& BHT   				& HLD 				& s/run  \\\\ \\hline \n")
latexfile.close()

plot_result_dict = {}

# Total number of observations: 13,927,119
NLIMIT_values = [1, 1000000, 2000000, 3000000, 4000000,  5000000,  6000000,  7000000,  8000000, 10000000,20000000,25000000]


exhaustive_times = []
all_randnode_times = []
all_furer_times = []    
all_falsefurer_times = []    

rndicts = []
fudicts = []
falsefudicts = []
for i in range(repetitions):
    print "starting iteration %d" % i
    ##D = nx.read_gml(graph_file_name)
    
    D = nx.read_gpickle(graph_file_name)
    
    P = nx.read_gml(pattern_path)
    # --------------------------------------------############### ---------- HERE CHANGE ALL THOSE ALWAYS

    OBdecomp = OBDsearch.get_heuristic4_OBD(P, startNode = 2)
    OBdecomp_false = [[item] for sublist in OBdecomp for item in sublist]
    Plist = [item for sublist in OBdecomp for item in sublist]
    root_nodes = [x for x in D.nodes() if D.node[x]['predicate']=='coauthored']
    print OBdecomp_false
    print OBdecomp
   
    # --------------------------------------------############### ----------------------------------------------------------------------
    print "Running random ..."
    limited_result = sampling_randomnode_general(D,  P,  Plist,  root_nodes,  NLIMIT_values)
    fdictionaries_limited = limited_result[0]
    times_limited = limited_result[1][1:]       # all without first element, which is absolute time of start
    #fdict_limited = fdictionaries_limited[-1:][0]      # samo najvecjega ne rabimo vec - rabimo listo vseh
    all_randnode_times.append(times_limited)
    rndicts.append(fdictionaries_limited)
    print "finished random ..."
    print "Running furer ..."
    furer_result = Furer_run_general(D, P , OBdecomp, root_nodes, NLIMIT_values)
    fdictionaries_Furer = furer_result[0]
    times_Furer = furer_result[1][1:]       # all without first element, which is absolute time of start
    #fdict_Furer = fdictionaries_Furer[-1:][0]      # samo najvecjega ne rabimo vec - rabimo listo vseh
    all_furer_times.append(times_Furer)
    fudicts.append(fdictionaries_Furer)
    print "Finished furer ..."
    print "Running false furer ..."
    falsefurer_result = Furer_run_general(D, P , OBdecomp_false, root_nodes, NLIMIT_values)
    fdictionaries_falseFurer = falsefurer_result[0]
    times_falseFurer = falsefurer_result[1][1:]       # all without first element, which is absolute time of start
    #fdict_Furer = fdictionaries_Furer[-1:][0]      # samo najvecjega ne rabimo vec - rabimo listo vseh
    all_falsefurer_times.append(times_falseFurer)
    falsefudicts.append(fdictionaries_falseFurer)
    print "Finished false furer ..."





# zdej vse rezultate imamo - samo se obdelat je treba...
# najprej pa SPICKLAT!
pickout = open('rndicts.pickle', 'wb')
pickle.dump(rndicts, pickout)
pickout.close()
pickout = open('fudicts.pickle', 'wb')
pickle.dump(fudicts, pickout)
pickout.close()
pickout = open('falsefudicts.pickle', 'wb')
pickle.dump(falsefudicts, pickout)
pickout.close()
pickout = open('all_randnode_times.pickle', 'wb')
pickle.dump(all_randnode_times, pickout)
pickout.close()
pickout = open('all_furer_times.pickle', 'wb')
pickle.dump(all_furer_times, pickout)
pickout.close()
pickout = open('all_falsefurer_times.pickle', 'wb')
pickle.dump(all_falsefurer_times, pickout)
pickout.close()
# poberi kar je za sprintat - ostalo spicklaj in je
# kar posimuliram kot je bilo nastavljeno prej:
#---pred tem se priprava fdict_exhaustive:
complete_combinations(fdict_exhaustive, D,  P,  Plist)      # add zeros to all not present combinations
smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive


for nli in range(len(NLIMIT_values)):
    plot_result_dict[NLIMIT_values[nli]] = {}
    randnode_results_KLD = []
    randnode_results_bhatta = []
    randnode_results_hellinger = []
    furer_results_KLD = []
    furer_results_bhatta = []
    furer_results_hellinger = []
    falsefurer_results_KLD = []
    falsefurer_results_bhatta = []
    falsefurer_results_hellinger = []
    randnode_times = []
    furer_times = []
    falsefurer_times = []    
    for i in range(repetitions):
        randnode_times.append(all_randnode_times[i][nli])
        furer_times.append(all_furer_times[i][nli])
        falsefurer_times.append(all_falsefurer_times[i][nli])
        
        fdict_limited = rndicts[i][nli]
        smooth(fdict_limited,  fdict_exhaustive)    # smoothing to avoid zeros
        fdict_Furer = fudicts[i][nli]
        smooth(fdict_Furer,  fdict_exhaustive)      # smoothing to avoid zeros
        fdict_falseFurer = falsefudicts[i][nli]
        smooth(fdict_falseFurer,  fdict_exhaustive)      # smoothing to avoid zeros



        ##pde = make_pd_general(fdict_exhaustive)
        [pde,  trash_list,  default_key] = make_pd_general_kickout_default(fdict_exhaustive,  trash_factor=0.01)     # we remove rows where frequencies do not reach 1%

        if len(pde) < 1:
            print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
            break
        [pdl,  tl,  dk] = make_pd_general_kickout_default_limited(fdict_limited,  trash_list,  default_key)
        [pdf ,  tl,  dk]= make_pd_general_kickout_default_limited(fdict_Furer,  trash_list,  default_key)
        [pdfalsef ,  tl,  dk]= make_pd_general_kickout_default_limited(fdict_falseFurer,  trash_list,  default_key)
        # new function also for limited ones : make_pd_general_kickout_default_limited(fdict,  trash,  default_key)



        randnode_results_KLD.append(su.avg_kld(transform_to_ptable(pde), transform_to_ptable(pdl)))
        randnode_results_bhatta.append(su.avg_bhatta(transform_to_ptable(pde), transform_to_ptable(pdl)))
        randnode_results_hellinger.append(su.avg_hellinger(transform_to_ptable(pde), transform_to_ptable(pdl)))
        
        furer_results_KLD.append(su.avg_kld(transform_to_ptable(pde), transform_to_ptable(pdf)))
        furer_results_bhatta.append(su.avg_bhatta(transform_to_ptable(pde), transform_to_ptable(pdf)))
        furer_results_hellinger.append(su.avg_hellinger(transform_to_ptable(pde), transform_to_ptable(pdf)))

        falsefurer_results_KLD.append(su.avg_kld(transform_to_ptable(pde), transform_to_ptable(pdfalsef)))
        falsefurer_results_bhatta.append(su.avg_bhatta(transform_to_ptable(pde), transform_to_ptable(pdfalsef)))
        falsefurer_results_hellinger.append(su.avg_hellinger(transform_to_ptable(pde), transform_to_ptable(pdfalsef)))

    print "So far good? plotting might be a problem"
    plot_result_dict[NLIMIT_values[nli]]["randomnode_KLD"] = (numpy.mean(randnode_results_KLD),  numpy.std(randnode_results_KLD,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["randomnode_BHT"] = (numpy.mean(randnode_results_bhatta),  numpy.std(randnode_results_bhatta,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["randomnode_HEL"] = (numpy.mean(randnode_results_hellinger),  numpy.std(randnode_results_hellinger,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["furer_KLD"] = (numpy.mean(furer_results_KLD),  numpy.std(furer_results_KLD,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["furer_BHT"] = (numpy.mean(furer_results_bhatta),  numpy.std(furer_results_bhatta,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["furer_HEL"] = (numpy.mean(furer_results_hellinger),  numpy.std(furer_results_hellinger,  ddof=1))

    plot_result_dict[NLIMIT_values[nli]]["falsefurer_KLD"] = (numpy.mean(falsefurer_results_KLD),  numpy.std(falsefurer_results_KLD,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["falsefurer_BHT"] = (numpy.mean(falsefurer_results_bhatta),  numpy.std(falsefurer_results_bhatta,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["falsefurer_HEL"] = (numpy.mean(falsefurer_results_hellinger),  numpy.std(falsefurer_results_hellinger,  ddof=1))

    # added to store and plot the times
    plot_result_dict[NLIMIT_values[nli]]["randomnode_times"] = (numpy.mean(randnode_times),  numpy.std(randnode_times,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["furer_times"] = (numpy.mean(furer_times),  numpy.std(furer_times,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["falsefurer_times"] = (numpy.mean(falsefurer_times),  numpy.std(falsefurer_times,  ddof=1))

    result_file_name = "ultimex_ICDM_" + short_graph_file_name + pattern_file_name+"."+str(repetitions) +"x"+str(NLIMIT_values[nli])+".result"
    resultfile = open(result_file_name,  'w')
    resultfile.write('-----SUMMARY---NO FALSE FURER HERE!--\n')
    resultfile.write("experiment on graph: " + str(short_graph_file_name) +" and pattern: "+pattern_file_name+"\n")
    resultfile.write("NLIMIT: " + str(NLIMIT_values[nli]) +"\n")
    resultfile.write("repetitions: " + str(repetitions) +"\n")
    resultfile.write(" " +"\n")
    resultfile.write("average average KLD on randomnode: " + str(numpy.mean(randnode_results_KLD))  + " with SSTD: " + str(numpy.std(randnode_results_KLD,  ddof=1)) +"\n")
    resultfile.write("average average bhatta on randomnode: " + str(numpy.mean(randnode_results_bhatta))  + " with SSTD: " + str(numpy.std(randnode_results_bhatta,  ddof=1)) +"\n")
    resultfile.write("average average hellinger on randomnode: " + str(numpy.mean(randnode_results_hellinger))  + " with SSTD: " + str(numpy.std(randnode_results_hellinger,  ddof=1)) +"\n")
    resultfile.write(" " +"\n")
    resultfile.write("average average KLD on Furer: " + str(numpy.mean(furer_results_KLD))  + " with SSTD: " + str(numpy.std(furer_results_KLD,  ddof=1)) +"\n")
    resultfile.write("average average bhatta on Furer: " + str(numpy.mean(furer_results_bhatta))  + " with SSTD: " + str(numpy.std(furer_results_bhatta,  ddof=1)) +"\n")
    resultfile.write("average average hellinger on Furer: " + str(numpy.mean(furer_results_hellinger))  + " with SSTD: " + str(numpy.std(furer_results_hellinger,  ddof=1)) +"\n")
    resultfile.write(" " +"\n")
    #resultfile.write("Experiment took: " +str(stop-start) + " seconds." +"\n")
    resultfile.write(' ' +"\n")
    #resultfile.write("Exhaustive took per run on average: " +str(numpy.mean(exhaustive_times)) + " seconds." +"\n")
    resultfile.write("Random node took per run on average: " +str(numpy.mean(randnode_times)) + " seconds." +"\n")
    resultfile.write("Furer took per run on average: " +str(numpy.mean(furer_times)) + " seconds." +"\n")
    resultfile.write('-----DETAILED RESULTS-----' +"\n")
    resultfile.write('randnode_results_KLD :' + str(randnode_results_KLD) +"\n")
    resultfile.write('randnode_results_bhatta :' + str(randnode_results_bhatta) +"\n")
    resultfile.write('randnode_results_hellinger :' + str(randnode_results_hellinger) +"\n")
    resultfile.write('furer_results_KLD :' + str(furer_results_KLD) +"\n")
    resultfile.write('furer_results_bhatta :' + str(furer_results_bhatta) +"\n")
    resultfile.write('furer_results_hellinger :' + str(furer_results_hellinger) +"\n")
    #resultfile.write('exhaustive_times :' + str(exhaustive_times) +"\n")
    resultfile.write('randnode_times :' + str(randnode_times) +"\n")
    resultfile.write('furer_times :' + str(furer_times) +"\n")
    resultfile.close()
    
    latexfile = open(latex_file_name,  'a')
    line1 = '$%s$ 	& random vertex & %s	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.0f \\\\ \n' % (short_graph_file_name,  str(NLIMIT_values[nli]), numpy.mean(randnode_results_KLD),  numpy.std(randnode_results_KLD,  ddof=1), numpy.mean(randnode_results_bhatta) ,  numpy.std(randnode_results_bhatta,  ddof=1),  numpy.mean(randnode_results_hellinger),  numpy.std(randnode_results_hellinger,  ddof=1),  numpy.mean(randnode_times))
    latexfile.write(line1)
    line2 = '$%s$ 	& Furer-Kasiv.  & %s	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.0f \\\\ \\hline \n' % (short_graph_file_name,   str(NLIMIT_values[nli]), numpy.mean(furer_results_KLD), numpy.std(furer_results_KLD,  ddof=1),  numpy.mean(furer_results_bhatta),  numpy.std(furer_results_bhatta,  ddof=1),  numpy.mean(furer_results_hellinger),  numpy.std(furer_results_hellinger,  ddof=1),  numpy.mean(furer_times))
    latexfile.write(line2)
    
    line3 = '$%s$ 	& falseFurer-Kasiv.  & %s	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.0f \\\\ \\hline \n' % (short_graph_file_name,   str(NLIMIT_values[nli]), numpy.mean(falsefurer_results_KLD), numpy.std(falsefurer_results_KLD,  ddof=1),  numpy.mean(falsefurer_results_bhatta),  numpy.std(falsefurer_results_bhatta,  ddof=1),  numpy.mean(falsefurer_results_hellinger),  numpy.std(falsefurer_results_hellinger,  ddof=1),  numpy.mean(falsefurer_times))
    latexfile.write(line3)
    latexfile.close()

    print "So far good 1? plotting might be a problem"
    startEX = time.time()
##        fdict_exhaustive = sampling_exhaustive_general2(D,  P,  Plist,  root_nodes)
    picklename = "fdict_exhaustive_%s.pickle" % short_graph_file_name
    pickin = open(picklename, 'rb')

    fdict_exhaustive = pickle.load(pickin)
    pickin.close()
    stopEX = time.time()
# za vse tu spodaj je treba samo, da je "plot_result_dict" tak kot mora biti

# plotting is now done in a separate script which is automatically created below
# (all direct plotting commands are surpressed with such a comment: #-- )
plot=False
if plot==True:
    plotScriptName = "plot_%sx%s_results.py" % (short_graph_file_name,  str(repetitions))
    plotScriptFile = open(plotScriptName,  'w')
    plotScriptFile.write("import matplotlib.pyplot as plt\n\n")
    plotfile = open("latest_plot_info.txt",  'w')
    
    
    #--plt.figure(1)
    plotScriptFile.write("plt.figure(1)\n")
    name = 'KLDof'+str(short_graph_file_name)+'x'+str(repetitions)
    PLTname = 'KLD \/ '+str(short_graph_file_name)+'x'+str(repetitions)     # name for plotting contains LaTeX math spacing command
    #--plt.ylabel(r'$\mathrm{%s}$' % PLTname)
    plotScriptFile.write("plt.ylabel(r'$\mathrm{%s}$')\n" % PLTname)
    #--plt.xlabel(r'$\mathrm{number of observations}$')
    plotScriptFile.write("plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotfile.write('name:' + str(name) +"\n")
    # gathering random vertex points
    rv_values = [plot_result_dict[k]["randomnode_KLD"][0] for k in NLIMIT_values]
    rv_deviations = [plot_result_dict[k]["randomnode_KLD"][1] for k in NLIMIT_values]
    rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
    #--plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random vertex}$')
    #--plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
    ##
    plotScriptFile.write("NLIMIT_values = %s\n" % str(NLIMIT_values))
    plotScriptFile.write("rv_values = %s\n" % str(rv_values))
    plotScriptFile.write("rv_CI_points = %s\n" % str(rv_CI_points))
    plotScriptFile.write("plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')\n")
    ##
    plotfile.write('NLIMIT_values:' + str(NLIMIT_values) +"\n")
    plotfile.write('rv_values:' + str(rv_values) +"\n")
    plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
    # gathering Furer points
    fu_values = [plot_result_dict[k]["furer_KLD"][0] for k in NLIMIT_values]
    fu_deviations = [plot_result_dict[k]["furer_KLD"][1] for k in NLIMIT_values]
    fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("fu_values = %s\n" % str(fu_values))
    plotScriptFile.write("fu_CI_points = %s\n" % str(fu_CI_points))
    plotScriptFile.write("plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')\n")
    ##
    plotfile.write('fu_values:' + str(fu_values) +"\n")
    plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
    margin = max(NLIMIT_values)*0.1
    minX = min(NLIMIT_values) - margin
    maxX = max(NLIMIT_values) + margin
    minY = 0
    maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
    #--plt.axis([minX,  maxX,  minY,  maxY])
    #--plt.legend()
    #--plt.savefig(name+'.pdf', format="pdf")
    ##plotScriptFile.write("margin = max(NLIMIT_values)*0.1\n")
    ##plotScriptFile.write("minX = min(NLIMIT_values) - margin\n")
    ##plotScriptFile.write("maxX = max(NLIMIT_values) + margin\n")
    ##plotScriptFile.write("minY = 0\n")
    ##plotScriptFile.write("maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))\n")
    ##plotScriptFile.write("plt.axis([minX,  maxX,  minY,  maxY])\n")
    plotScriptFile.write("plt.yscale('log')\n")
    plotScriptFile.write("plt.legend()\n")
    plotScriptFile.write("plt.savefig('%s'+'.pdf', format='pdf')\n" % name)
    plotScriptFile.write("plt.savefig('%s'+'.eps', format='eps')\n" % name)
    plotScriptFile.write("\n\n")
    
    # gathering falseFurer points
    falsefu_values = [plot_result_dict[k]["falsefurer_KLD"][0] for k in NLIMIT_values]
    falsefu_deviations = [plot_result_dict[k]["falsefurer_KLD"][1] for k in NLIMIT_values]
    falsefu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in falsefu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("falsefu_values = %s\n" % str(falsefu_values))
    plotScriptFile.write("falsefu_CI_points = %s\n" % str(falsefu_CI_points))
    plotScriptFile.write("plt.plot( NLIMIT_values, falsefu_values, 'g-', label=r'$\mathrm{falseF\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("plt.errorbar(NLIMIT_values, falsefu_values, yerr=falsefu_CI_points, ecolor='g', fmt='or')\n")
    ##
    plotfile.write('falsefu_values:' + str(falsefu_values) +"\n")
    plotfile.write('falsefu_CI_points:' + str(falsefu_CI_points) +"\n")
    margin = max(NLIMIT_values)*0.1
    minX = min(NLIMIT_values) - margin
    maxX = max(NLIMIT_values) + margin
    minY = 0
    maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
    #--plt.axis([minX,  maxX,  minY,  maxY])
    #--plt.legend()
    #--plt.savefig(name+'.pdf', format="pdf")
    ##plotScriptFile.write("margin = max(NLIMIT_values)*0.1\n")
    ##plotScriptFile.write("minX = min(NLIMIT_values) - margin\n")
    ##plotScriptFile.write("maxX = max(NLIMIT_values) + margin\n")
    ##plotScriptFile.write("minY = 0\n")
    ##plotScriptFile.write("maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))\n")
    ##plotScriptFile.write("plt.axis([minX,  maxX,  minY,  maxY])\n")
    plotScriptFile.write("plt.yscale('log')\n")
    plotScriptFile.write("plt.legend()\n")
    plotScriptFile.write("plt.savefig('%s'+'.pdf', format='pdf')\n" % name)
    plotScriptFile.write("plt.savefig('%s'+'.eps', format='eps')\n" % name)
    plotScriptFile.write("\n\n")
    
    
    #--plt.figure(2)
    plotScriptFile.write("plt.figure(2)\n")
    name = 'BHTof'+str(short_graph_file_name)+'x'+str(repetitions)
    PLTname = 'BHT \/ '+str(short_graph_file_name)+'x'+str(repetitions)
    #--plt.ylabel(r'%s' % PLTname)
    plotScriptFile.write("plt.ylabel(r'$\mathrm{%s}$')\n" % PLTname)
    #--plt.xlabel('number of observations')
    plotScriptFile.write("plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotfile.write('name:' + str(name) +"\n")
    # gathering random vertex points
    rv_values = [plot_result_dict[k]["randomnode_BHT"][0] for k in NLIMIT_values]
    rv_deviations = [plot_result_dict[k]["randomnode_BHT"][1] for k in NLIMIT_values]
    rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
    #--plt.plot(NLIMIT_values, rv_values, 'b-', label='random vertex')
    #--plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
    ##
    plotScriptFile.write("rv_values = %s\n" % str(rv_values))
    plotScriptFile.write("rv_CI_points = %s\n" % str(rv_CI_points))
    plotScriptFile.write("plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')\n")
    ##
    plotfile.write('rv_values:' + str(rv_values) +"\n")
    plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
    # gathering Furer points
    fu_values = [plot_result_dict[k]["furer_BHT"][0] for k in NLIMIT_values]
    fu_deviations = [plot_result_dict[k]["furer_BHT"][1] for k in NLIMIT_values]
    fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label='Fur-Kas')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("fu_values = %s\n" % str(fu_values))
    plotScriptFile.write("fu_CI_points = %s\n" % str(fu_CI_points))
    plotScriptFile.write("plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')\n")
    ##
    plotfile.write('fu_values:' + str(fu_values) +"\n")
    plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
    margin = max(NLIMIT_values)*0.1
    minX = min(NLIMIT_values) - margin
    maxX = max(NLIMIT_values) + margin
    minY = 0
    maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
    #--plt.axis([minX,  maxX,  minY,  maxY])
    #--plt.legend()
    #--plt.savefig(name+'.pdf', format="pdf")
    ##plotScriptFile.write("margin = max(NLIMIT_values)*0.1\n")
    ##plotScriptFile.write("minX = min(NLIMIT_values) - margin\n")
    ##plotScriptFile.write("maxX = max(NLIMIT_values) + margin\n")
    ##plotScriptFile.write("minY = 0\n")
    ##plotScriptFile.write("maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))\n")
    ##plotScriptFile.write("plt.axis([minX,  maxX,  minY,  maxY])\n")
    plotScriptFile.write("plt.yscale('log')\n")
    plotScriptFile.write("plt.legend()\n")
    plotScriptFile.write("plt.savefig('%s'+'.pdf', format='pdf')\n" % name)
    plotScriptFile.write("plt.savefig('%s'+'.eps', format='eps')\n" % name)
    plotScriptFile.write("\n\n")
    
    
    
    #--plt.figure(3)
    plotScriptFile.write("plt.figure(3)\n")
    name = 'HELof'+str(short_graph_file_name)+'x'+str(repetitions)
    PLTname = 'HEL \/ '+str(short_graph_file_name)+'x'+str(repetitions)
    #--plt.ylabel(r'%s' % PLTname)
    plotScriptFile.write("plt.ylabel(r'$\mathrm{%s}$')\n" % PLTname)
    #--plt.xlabel('number of observations')
    plotScriptFile.write("plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotfile.write('name:' + str(name) +"\n")
    # gathering random vertex points
    rv_values = [plot_result_dict[k]["randomnode_HEL"][0] for k in NLIMIT_values]
    rv_deviations = [plot_result_dict[k]["randomnode_HEL"][1] for k in NLIMIT_values]
    rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
    #--plt.plot(NLIMIT_values, rv_values, 'b-', label='random vertex')
    #--plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
    ##
    plotScriptFile.write("rv_values = %s\n" % str(rv_values))
    plotScriptFile.write("rv_CI_points = %s\n" % str(rv_CI_points))
    plotScriptFile.write("plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')\n")
    ##
    plotfile.write('rv_values:' + str(rv_values) +"\n")
    plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
    # gathering Furer points
    fu_values = [plot_result_dict[k]["furer_HEL"][0] for k in NLIMIT_values]
    fu_deviations = [plot_result_dict[k]["furer_HEL"][1] for k in NLIMIT_values]
    fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label='Fur-Kas')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("fu_values = %s\n" % str(fu_values))
    plotScriptFile.write("fu_CI_points = %s\n" % str(fu_CI_points))
    plotScriptFile.write("plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')\n")
    ##
    plotfile.write('fu_values:' + str(fu_values) +"\n")
    plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
    margin = max(NLIMIT_values)*0.1
    minX = min(NLIMIT_values) - margin
    maxX = max(NLIMIT_values) + margin
    maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
    minY = 0
    #--plt.axis([minX,  maxX,  minY,  maxY])
    #--plt.legend()
    #--plt.savefig(name+'.pdf', format="pdf")
    ##plotScriptFile.write("margin = max(NLIMIT_values)*0.1\n")
    ##plotScriptFile.write("minX = min(NLIMIT_values) - margin\n")
    ##plotScriptFile.write("maxX = max(NLIMIT_values) + margin\n")
    ##plotScriptFile.write("minY = 0\n")
    ##plotScriptFile.write("maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))\n")
    ##plotScriptFile.write("plt.axis([minX,  maxX,  minY,  maxY])\n")
    plotScriptFile.write("plt.yscale('log')\n")
    plotScriptFile.write("plt.legend()\n")
    plotScriptFile.write("plt.savefig('%s'+'.pdf', format='pdf')\n" % name)
    plotScriptFile.write("plt.savefig('%s'+'.eps', format='eps')\n" % name)
    plotScriptFile.write("\n\n")
    
    # now also plotting TIME axis --------------------------------------------------------------------------------------------------
    
    ext_pickle = open("extime.pickle", 'rb')
    extimeList = pickle.load(ext_pickle)
    extime = extimeList[0]              # this is the time that we need for exhaustive time
    ext_pickle.close()
    
    
    #--plt.figure(4)
    plotScriptFile.write("fig = plt.figure(4)\n")
    plotScriptFile.write("NLIMIT_values = %s\n" % str(NLIMIT_values))
    plotScriptFile.write("ax1 = fig.add_subplot(111)\n")
    
    name = 'KLDof'+str(short_graph_file_name)+'x'+str(repetitions)
    PLTname = 'KLD \/ '+str(short_graph_file_name)+'x'+str(repetitions)     # name for plotting contains LaTeX math spacing command
    #--plt.ylabel(r'$\mathrm{%s}$' % PLTname)
    plotScriptFile.write("plt.ylabel(r'$\mathrm{%s}$')\n" % PLTname)
    #--plt.xlabel(r'$\mathrm{number of observations}$')
    plotScriptFile.write("plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotfile.write('name:' + str(name) +"\n")
    # gathering random vertex points
    rv_values = [plot_result_dict[k]["randomnode_KLD"][0] for k in NLIMIT_values]
    rv_deviations = [plot_result_dict[k]["randomnode_KLD"][1] for k in NLIMIT_values]
    rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
    #--plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random vertex}$')
    #--plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
    ##
    
    plotScriptFile.write("rv_values = %s\n" % str(rv_values))
    plotScriptFile.write("rv_CI_points = %s\n" % str(rv_CI_points))
    plotScriptFile.write("ax1.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("ax1.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')\n")
    
    
    ##
    plotfile.write('NLIMIT_values:' + str(NLIMIT_values) +"\n")
    plotfile.write('rv_values:' + str(rv_values) +"\n")
    plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
    # gathering Furer points
    fu_values = [plot_result_dict[k]["furer_KLD"][0] for k in NLIMIT_values]
    fu_deviations = [plot_result_dict[k]["furer_KLD"][1] for k in NLIMIT_values]
    fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("fu_values = %s\n" % str(fu_values))
    plotScriptFile.write("fu_CI_points = %s\n" % str(fu_CI_points))
    plotScriptFile.write("ax1.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("ax1.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')\n")
    
    
    # gathering falseFurer points
    falsefu_values = [plot_result_dict[k]["falsefurer_KLD"][0] for k in NLIMIT_values]
    falsefu_deviations = [plot_result_dict[k]["falsefurer_KLD"][1] for k in NLIMIT_values]
    falsefu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in falsefu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("falsefu_values = %s\n" % str(falsefu_values))
    plotScriptFile.write("falsefu_CI_points = %s\n" % str(falsefu_CI_points))
    plotScriptFile.write("ax1.plot( NLIMIT_values, falsefu_values, 'g-', label=r'$\mathrm{F\ddot{u}r-Kas*}$')\n")
    plotScriptFile.write("ax1.errorbar(NLIMIT_values, falsefu_values, yerr=falsefu_CI_points, ecolor='g', fmt='og')\n")
    
    
    plotScriptFile.write("ax1.set_yscale('log')\n")
    plotScriptFile.write("ax1.set_xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotScriptFile.write("ax1.set_ylabel(r'$\mathrm{KLD}$')\n")
    
    
    plotScriptFile.write("ax2 = ax1.twinx()\n")
    
    rv_time_values = [plot_result_dict[k]["randomnode_times"][0] for k in NLIMIT_values]
    rv_time_deviations = [plot_result_dict[k]["randomnode_times"][1] for k in NLIMIT_values]
    rv_time_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_time_deviations]
    
    plotScriptFile.write("rv_time_values = %s\n" % str(rv_time_values))
    plotScriptFile.write("rv_time_deviations = %s\n" % str(rv_time_deviations))
    plotScriptFile.write("rv_time_CI_points = %s\n" % str(rv_time_CI_points))
    plotScriptFile.write("ax2.plot(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("ax2.errorbar(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', yerr=rv_time_CI_points)\n")
    
    fu_time_values = [plot_result_dict[k]["furer_times"][0] for k in NLIMIT_values]
    fu_time_deviations = [plot_result_dict[k]["furer_times"][1] for k in NLIMIT_values]
    fu_time_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_time_deviations]
    
    plotScriptFile.write("fu_time_values = %s\n" % str(fu_time_values))
    plotScriptFile.write("fu_time_deviations = %s\n" % str(fu_time_deviations))
    plotScriptFile.write("fu_time_CI_points = %s\n" % str(fu_time_CI_points))
    plotScriptFile.write("ax2.plot(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("ax2.errorbar(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', yerr=fu_time_CI_points)\n")
    
    falsefu_time_values = [plot_result_dict[k]["falsefurer_times"][0] for k in NLIMIT_values]
    falsefu_time_deviations = [plot_result_dict[k]["falsefurer_times"][1] for k in NLIMIT_values]
    falsefu_time_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in falsefu_time_deviations]
    
    plotScriptFile.write("falsefu_time_values = %s\n" % str(falsefu_time_values))
    plotScriptFile.write("falsefu_time_deviations = %s\n" % str(falsefu_time_deviations))
    plotScriptFile.write("falsefu_time_CI_points = %s\n" % str(falsefu_time_CI_points))
    plotScriptFile.write("ax2.plot(NLIMIT_values, falsefu_time_values, color='k',  linestyle='dotted', label=r'$\mathrm{F\ddot{u}r-Kas*}$')\n")
    plotScriptFile.write("ax2.errorbar(NLIMIT_values, falsefu_time_values, color='k',  linestyle='dotted', yerr=falsefu_time_CI_points)\n")
    
    
    plotScriptFile.write("#ax2.axhline(y=extime,  color='k')       #      set this also, for extime plotting\n")
    plotScriptFile.write("ax2.set_ylabel(r'$\mathrm{time}$')\n")
    ##plotScriptFile.write("ax2.legend(loc=1)\n")
    ##plotScriptFile.write("ax1.legend(loc=2)\n")
    ## INSTEAD of this above, we have a fancy legend now
    plotScriptFile.write("leg1 = ax1.legend(loc=2, fancybox=True)\n")
    plotScriptFile.write("leg1.get_frame().set_alpha(0.5)\n")
    plotScriptFile.write("leg2 = ax2.legend(loc=1, fancybox=True)\n")
    plotScriptFile.write("leg2.get_frame().set_alpha(0.5)\n")
    
    ##
    
    plotfile.write('fu_values:' + str(fu_values) +"\n")
    plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
    ##margin = max(NLIMIT_values)*0.1
    ##minX = min(NLIMIT_values) - margin
    ##maxX = max(NLIMIT_values) + margin
    ##minY = 0
    ##maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
    #--plt.axis([minX,  maxX,  minY,  maxY])
    #--plt.legend()
    #--plt.savefig(name+'.pdf', format="pdf")
    ##plotScriptFile.write("margin = max(NLIMIT_values)*0.1\n")
    ##plotScriptFile.write("minX = min(NLIMIT_values) - margin\n")
    ##plotScriptFile.write("maxX = max(NLIMIT_values) + margin\n")
    ##plotScriptFile.write("minY = 0\n")
    ##plotScriptFile.write("maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))\n")
    ##plotScriptFile.write("plt.axis([minX,  maxX,  minY,  maxY])\n")
    ##plotScriptFile.write("plt.yscale('log')\n")
    ##plotScriptFile.write("plt.legend()\n")
    plotScriptFile.write("plt.savefig('%s'+'time.pdf', format='pdf')\n" % name)
    plotScriptFile.write("plt.savefig('%s'+'time.eps', format='eps')\n" % name)
    plotScriptFile.write("\n\n")
    
    
    #--plt.figure(5)
    plotScriptFile.write("fig = plt.figure(5)\n")
    plotScriptFile.write("NLIMIT_values = %s\n" % str(NLIMIT_values))
    plotScriptFile.write("ax1 = fig.add_subplot(111)\n")
    
    name = 'BHTof'+str(short_graph_file_name)+'x'+str(repetitions)
    PLTname = 'BHT \/ '+str(short_graph_file_name)+'x'+str(repetitions)     # name for plotting contains LaTeX math spacing command
    #--plt.ylabel(r'$\mathrm{%s}$' % PLTname)
    plotScriptFile.write("plt.ylabel(r'$\mathrm{%s}$')\n" % PLTname)
    #--plt.xlabel(r'$\mathrm{number of observations}$')
    plotScriptFile.write("plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotfile.write('name:' + str(name) +"\n")
    # gathering random vertex points
    rv_values = [plot_result_dict[k]["randomnode_BHT"][0] for k in NLIMIT_values]
    rv_deviations = [plot_result_dict[k]["randomnode_BHT"][1] for k in NLIMIT_values]
    rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
    #--plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random vertex}$')
    #--plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
    ##
    
    plotScriptFile.write("rv_values = %s\n" % str(rv_values))
    plotScriptFile.write("rv_CI_points = %s\n" % str(rv_CI_points))
    plotScriptFile.write("ax1.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("ax1.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')\n")
    
    
    ##
    plotfile.write('NLIMIT_values:' + str(NLIMIT_values) +"\n")
    plotfile.write('rv_values:' + str(rv_values) +"\n")
    plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
    # gathering Furer points
    fu_values = [plot_result_dict[k]["furer_BHT"][0] for k in NLIMIT_values]
    fu_deviations = [plot_result_dict[k]["furer_BHT"][1] for k in NLIMIT_values]
    fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("fu_values = %s\n" % str(fu_values))
    plotScriptFile.write("fu_CI_points = %s\n" % str(fu_CI_points))
    plotScriptFile.write("ax1.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("ax1.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')\n")
    
    plotScriptFile.write("ax1.set_yscale('log')\n")
    plotScriptFile.write("ax1.set_xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotScriptFile.write("ax1.set_ylabel(r'$\mathrm{BHT}$')\n")
    
    
    plotScriptFile.write("ax2 = ax1.twinx()\n")
    
    rv_time_values = [plot_result_dict[k]["randomnode_times"][0] for k in NLIMIT_values]
    rv_time_deviations = [plot_result_dict[k]["randomnode_times"][1] for k in NLIMIT_values]
    rv_time_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_time_deviations]
    
    plotScriptFile.write("rv_time_values = %s\n" % str(rv_time_values))
    plotScriptFile.write("rv_time_deviations = %s\n" % str(rv_time_deviations))
    plotScriptFile.write("rv_time_CI_points = %s\n" % str(rv_time_CI_points))
    plotScriptFile.write("ax2.plot(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("ax2.errorbar(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', yerr=rv_time_CI_points)\n")
    
    fu_time_values = [plot_result_dict[k]["furer_times"][0] for k in NLIMIT_values]
    fu_time_deviations = [plot_result_dict[k]["furer_times"][1] for k in NLIMIT_values]
    fu_time_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_time_deviations]
    
    plotScriptFile.write("fu_time_values = %s\n" % str(fu_time_values))
    plotScriptFile.write("fu_time_deviations = %s\n" % str(fu_time_deviations))
    plotScriptFile.write("fu_time_CI_points = %s\n" % str(fu_time_CI_points))
    plotScriptFile.write("ax2.plot(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("ax2.errorbar(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', yerr=fu_time_CI_points)\n")
    
    plotScriptFile.write("#ax2.axhline(y=extime,  color='k')       #      set this also, for extime plotting\n")
    plotScriptFile.write("ax2.set_ylabel(r'$\mathrm{time}$')\n")
    ##plotScriptFile.write("ax2.legend(loc=1)\n")
    ##plotScriptFile.write("ax1.legend(loc=2)\n")
    ## INSTEAD of this above, we have a fancy legend now
    plotScriptFile.write("leg1 = ax1.legend(loc=2, fancybox=True)\n")
    plotScriptFile.write("leg1.get_frame().set_alpha(0.5)\n")
    plotScriptFile.write("leg2 = ax2.legend(loc=1, fancybox=True)\n")
    plotScriptFile.write("leg2.get_frame().set_alpha(0.5)\n")
    
    ##
    
    plotfile.write('fu_values:' + str(fu_values) +"\n")
    plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
    ##margin = max(NLIMIT_values)*0.1
    ##minX = min(NLIMIT_values) - margin
    ##maxX = max(NLIMIT_values) + margin
    ##minY = 0
    ##maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
    #--plt.axis([minX,  maxX,  minY,  maxY])
    #--plt.legend()
    #--plt.savefig(name+'.pdf', format="pdf")
    ##plotScriptFile.write("margin = max(NLIMIT_values)*0.1\n")
    ##plotScriptFile.write("minX = min(NLIMIT_values) - margin\n")
    ##plotScriptFile.write("maxX = max(NLIMIT_values) + margin\n")
    ##plotScriptFile.write("minY = 0\n")
    ##plotScriptFile.write("maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))\n")
    ##plotScriptFile.write("plt.axis([minX,  maxX,  minY,  maxY])\n")
    ##plotScriptFile.write("plt.yscale('log')\n")
    ##plotScriptFile.write("plt.legend()\n")
    plotScriptFile.write("plt.savefig('%s'+'time.pdf', format='pdf')\n" % name)
    plotScriptFile.write("plt.savefig('%s'+'time.eps', format='eps')\n" % name)
    plotScriptFile.write("\n\n")
    
    
    
    #--plt.figure(6)
    plotScriptFile.write("fig = plt.figure(6)\n")
    plotScriptFile.write("NLIMIT_values = %s\n" % str(NLIMIT_values))
    plotScriptFile.write("ax1 = fig.add_subplot(111)\n")
    
    name = 'HELof'+str(short_graph_file_name)+'x'+str(repetitions)
    PLTname = 'HEL \/ '+str(short_graph_file_name)+'x'+str(repetitions)     # name for plotting contains LaTeX math spacing command
    #--plt.ylabel(r'$\mathrm{%s}$' % PLTname)
    plotScriptFile.write("plt.ylabel(r'$\mathrm{%s}$')\n" % PLTname)
    #--plt.xlabel(r'$\mathrm{number of observations}$')
    plotScriptFile.write("plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotfile.write('name:' + str(name) +"\n")
    # gathering random vertex points
    rv_values = [plot_result_dict[k]["randomnode_HEL"][0] for k in NLIMIT_values]
    rv_deviations = [plot_result_dict[k]["randomnode_HEL"][1] for k in NLIMIT_values]
    rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
    #--plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random vertex}$')
    #--plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
    ##
    
    plotScriptFile.write("rv_values = %s\n" % str(rv_values))
    plotScriptFile.write("rv_CI_points = %s\n" % str(rv_CI_points))
    plotScriptFile.write("ax1.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("ax1.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')\n")
    
    
    ##
    plotfile.write('NLIMIT_values:' + str(NLIMIT_values) +"\n")
    plotfile.write('rv_values:' + str(rv_values) +"\n")
    plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
    # gathering Furer points
    fu_values = [plot_result_dict[k]["furer_HEL"][0] for k in NLIMIT_values]
    fu_deviations = [plot_result_dict[k]["furer_HEL"][1] for k in NLIMIT_values]
    fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
    #--plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
    #--plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
    ##
    plotScriptFile.write("fu_values = %s\n" % str(fu_values))
    plotScriptFile.write("fu_CI_points = %s\n" % str(fu_CI_points))
    plotScriptFile.write("ax1.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("ax1.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')\n")
    
    plotScriptFile.write("ax1.set_yscale('log')\n")
    plotScriptFile.write("ax1.set_xlabel(r'$\mathrm{number \/ of \/ observations}$')\n")
    plotScriptFile.write("ax1.set_ylabel(r'$\mathrm{HEL}$')\n")
    
    
    plotScriptFile.write("ax2 = ax1.twinx()\n")
    
    rv_time_values = [plot_result_dict[k]["randomnode_times"][0] for k in NLIMIT_values]
    rv_time_deviations = [plot_result_dict[k]["randomnode_times"][1] for k in NLIMIT_values]
    rv_time_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_time_deviations]
    
    plotScriptFile.write("rv_time_values = %s\n" % str(rv_time_values))
    plotScriptFile.write("rv_time_deviations = %s\n" % str(rv_time_deviations))
    plotScriptFile.write("rv_time_CI_points = %s\n" % str(rv_time_CI_points))
    plotScriptFile.write("ax2.plot(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', label=r'$\mathrm{random \/ vertex}$')\n")
    plotScriptFile.write("ax2.errorbar(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', yerr=rv_time_CI_points)\n")
    
    fu_time_values = [plot_result_dict[k]["furer_times"][0] for k in NLIMIT_values]
    fu_time_deviations = [plot_result_dict[k]["furer_times"][1] for k in NLIMIT_values]
    fu_time_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_time_deviations]
    
    plotScriptFile.write("fu_time_values = %s\n" % str(fu_time_values))
    plotScriptFile.write("fu_time_deviations = %s\n" % str(fu_time_deviations))
    plotScriptFile.write("fu_time_CI_points = %s\n" % str(fu_time_CI_points))
    plotScriptFile.write("ax2.plot(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', label=r'$\mathrm{F\ddot{u}r-Kas}$')\n")
    plotScriptFile.write("ax2.errorbar(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', yerr=fu_time_CI_points)\n")
    
    plotScriptFile.write("#ax2.axhline(y=extime,  color='k')       #      set this also, for extime plotting\n")
    plotScriptFile.write("ax2.set_ylabel(r'$\mathrm{time}$')\n")
    ##plotScriptFile.write("ax2.legend(loc=1)\n")
    ##plotScriptFile.write("ax1.legend(loc=2)\n")
    ## INSTEAD of this above, we have a fancy legend now
    plotScriptFile.write("leg1 = ax1.legend(loc=2, fancybox=True)\n")
    plotScriptFile.write("leg1.get_frame().set_alpha(0.5)\n")
    plotScriptFile.write("leg2 = ax2.legend(loc=1, fancybox=True)\n")
    plotScriptFile.write("leg2.get_frame().set_alpha(0.5)\n")
    
    ##
    
    plotfile.write('fu_values:' + str(fu_values) +"\n")
    plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
    ##margin = max(NLIMIT_values)*0.1
    ##minX = min(NLIMIT_values) - margin
    ##maxX = max(NLIMIT_values) + margin
    ##minY = 0
    ##maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
    #--plt.axis([minX,  maxX,  minY,  maxY])
    #--plt.legend()
    #--plt.savefig(name+'.pdf', format="pdf")
    ##plotScriptFile.write("margin = max(NLIMIT_values)*0.1\n")
    ##plotScriptFile.write("minX = min(NLIMIT_values) - margin\n")
    ##plotScriptFile.write("maxX = max(NLIMIT_values) + margin\n")
    ##plotScriptFile.write("minY = 0\n")
    ##plotScriptFile.write("maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))\n")
    ##plotScriptFile.write("plt.axis([minX,  maxX,  minY,  maxY])\n")
    ##plotScriptFile.write("plt.yscale('log')\n")
    ##plotScriptFile.write("plt.legend()\n")
    plotScriptFile.write("plt.savefig('%s'+'time.pdf', format='pdf')\n" % name)
    plotScriptFile.write("plt.savefig('%s'+'time.eps', format='eps')\n" % name)
    plotScriptFile.write("\n\n")
    
    
    plotfile.close()
    plotScriptFile.close()
    
    os.system("python %s" % plotScriptName)     # call to the script that was created here. This script then creates the plots.
    
