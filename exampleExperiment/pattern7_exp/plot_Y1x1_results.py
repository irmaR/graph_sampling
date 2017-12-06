import matplotlib.pyplot as plt

plt.figure(1)
plt.ylabel(r'$\mathrm{KLD \/ Y1x1}$')
plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')
NLIMIT_values = [1, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000]
rv_values = [0.31546680485996181, 0.041892765402729459, 0.039142946866879316, 0.014214022810741441, 0.00998040629651528, 0.0099107595797148715, 0.0056907568222241073, 0.0054267466634797855, 0.01272096965463191]
rv_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')
plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
fu_values = [0.31546680485996181, 0.19503455265209932, 0.059835341190869827, 0.014921447801425817, 0.014501390025876292, 0.010347879259229255, 0.014218084493769876, 0.0083794339685660888, 0.0069462294809580554]
fu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
plt.yscale('log')
plt.legend()
plt.savefig('KLDofY1x1'+'.pdf', format='pdf')
plt.savefig('KLDofY1x1'+'.eps', format='eps')


falsefu_values = [0.31546680485996181, 0.10140118011394812, 0.020204762177258126, 0.015271994916401903, 0.01908661270099464, 0.054541328717741429, 0.036523792111500746, 0.02751649698319172, 0.022950477388082102]
falsefu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
plt.plot( NLIMIT_values, falsefu_values, 'g-', label=r'$\mathrm{falseF\ddot{u}r-Kas}$')
plt.errorbar(NLIMIT_values, falsefu_values, yerr=falsefu_CI_points, ecolor='g', fmt='or')
plt.yscale('log')
plt.legend()
plt.savefig('KLDofY1x1'+'.pdf', format='pdf')
plt.savefig('KLDofY1x1'+'.eps', format='eps')


plt.figure(2)
plt.ylabel(r'$\mathrm{BHT \/ Y1x1}$')
plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')
rv_values = [0.06128139140706923, 0.0067306804667327498, 0.0063302885789938146, 0.0023799598811581838, 0.0016462847865942834, 0.0016551630883376034, 0.00096950852695419643, 0.00091897290926222421, 0.0021406954970106416]
rv_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')
plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
fu_values = [0.06128139140706923, 0.031610274564528758, 0.0089362430412657911, 0.002678306096069089, 0.0025432790612325007, 0.0017909610469109296, 0.002578553901167862, 0.0015120737025265615, 0.0012398248461498024]
fu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
plt.yscale('log')
plt.legend()
plt.savefig('BHTofY1x1'+'.pdf', format='pdf')
plt.savefig('BHTofY1x1'+'.eps', format='eps')


plt.figure(3)
plt.ylabel(r'$\mathrm{HEL \/ Y1x1}$')
plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')
rv_values = [0.24310371665702471, 0.07649338163122256, 0.074386692308798533, 0.04249140811841836, 0.039863892562961252, 0.039677174842252548, 0.030812609518103079, 0.02949962386379253, 0.03901411120984289]
rv_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
plt.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')
plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
fu_values = [0.24310371665702471, 0.16436201134404288, 0.070216886495904698, 0.045324956378736708, 0.047655316706427753, 0.042215153019666975, 0.044367076204819722, 0.032361492053370841, 0.026641350116839779]
fu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
plt.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
plt.yscale('log')
plt.legend()
plt.savefig('HELofY1x1'+'.pdf', format='pdf')
plt.savefig('HELofY1x1'+'.eps', format='eps')


fig = plt.figure(4)
NLIMIT_values = [1, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000]
ax1 = fig.add_subplot(111)
plt.ylabel(r'$\mathrm{KLD \/ Y1x1}$')
plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')
rv_values = [0.31546680485996181, 0.041892765402729459, 0.039142946866879316, 0.014214022810741441, 0.00998040629651528, 0.0099107595797148715, 0.0056907568222241073, 0.0054267466634797855, 0.01272096965463191]
rv_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax1.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')
ax1.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
fu_values = [0.31546680485996181, 0.19503455265209932, 0.059835341190869827, 0.014921447801425817, 0.014501390025876292, 0.010347879259229255, 0.014218084493769876, 0.0083794339685660888, 0.0069462294809580554]
fu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax1.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
ax1.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
falsefu_values = [0.31546680485996181, 0.10140118011394812, 0.020204762177258126, 0.015271994916401903, 0.01908661270099464, 0.054541328717741429, 0.036523792111500746, 0.02751649698319172, 0.022950477388082102]
falsefu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax1.plot( NLIMIT_values, falsefu_values, 'g-', label=r'$\mathrm{F\ddot{u}r-Kas*}$')
ax1.errorbar(NLIMIT_values, falsefu_values, yerr=falsefu_CI_points, ecolor='g', fmt='og')
ax1.set_yscale('log')
ax1.set_xlabel(r'$\mathrm{number \/ of \/ observations}$')
ax1.set_ylabel(r'$\mathrm{KLD}$')
ax2 = ax1.twinx()
rv_time_values = [5.4121017456054688e-05, 15.434289932250977, 30.512920141220093, 45.412091970443726, 60.64211893081665, 75.574176073074341, 90.450778007507324, 105.30454301834106, 120.12457299232483]
rv_time_deviations = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
rv_time_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax2.plot(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', label=r'$\mathrm{random \/ vertex}$')
ax2.errorbar(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', yerr=rv_time_CI_points)
fu_time_values = [9.822845458984375e-05, 3.8530950546264648, 7.7004661560058594, 11.548807144165039, 15.393929004669189, 19.224869012832642, 23.072908163070679, 26.92710018157959, 30.773489236831665]
fu_time_deviations = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
fu_time_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax2.plot(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', label=r'$\mathrm{F\ddot{u}r-Kas}$')
ax2.errorbar(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', yerr=fu_time_CI_points)
falsefu_time_values = [6.008148193359375e-05, 3.3735520839691162, 6.7104589939117432, 10.087679147720337, 13.434842109680176, 16.78682017326355, 20.111610174179077, 23.464076042175293, 26.814467191696167]
falsefu_time_deviations = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
falsefu_time_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax2.plot(NLIMIT_values, falsefu_time_values, color='k',  linestyle='dotted', label=r'$\mathrm{F\ddot{u}r-Kas*}$')
ax2.errorbar(NLIMIT_values, falsefu_time_values, color='k',  linestyle='dotted', yerr=falsefu_time_CI_points)
#ax2.axhline(y=extime,  color='k')       #      set this also, for extime plotting
ax2.set_ylabel(r'$\mathrm{time}$')
leg1 = ax1.legend(loc=2, fancybox=True)
leg1.get_frame().set_alpha(0.5)
leg2 = ax2.legend(loc=1, fancybox=True)
leg2.get_frame().set_alpha(0.5)
plt.savefig('KLDofY1x1'+'time.pdf', format='pdf')
plt.savefig('KLDofY1x1'+'time.eps', format='eps')


fig = plt.figure(5)
NLIMIT_values = [1, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000]
ax1 = fig.add_subplot(111)
plt.ylabel(r'$\mathrm{BHT \/ Y1x1}$')
plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')
rv_values = [0.06128139140706923, 0.0067306804667327498, 0.0063302885789938146, 0.0023799598811581838, 0.0016462847865942834, 0.0016551630883376034, 0.00096950852695419643, 0.00091897290926222421, 0.0021406954970106416]
rv_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax1.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')
ax1.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
fu_values = [0.06128139140706923, 0.031610274564528758, 0.0089362430412657911, 0.002678306096069089, 0.0025432790612325007, 0.0017909610469109296, 0.002578553901167862, 0.0015120737025265615, 0.0012398248461498024]
fu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax1.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
ax1.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
ax1.set_yscale('log')
ax1.set_xlabel(r'$\mathrm{number \/ of \/ observations}$')
ax1.set_ylabel(r'$\mathrm{BHT}$')
ax2 = ax1.twinx()
rv_time_values = [5.4121017456054688e-05, 15.434289932250977, 30.512920141220093, 45.412091970443726, 60.64211893081665, 75.574176073074341, 90.450778007507324, 105.30454301834106, 120.12457299232483]
rv_time_deviations = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
rv_time_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax2.plot(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', label=r'$\mathrm{random \/ vertex}$')
ax2.errorbar(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', yerr=rv_time_CI_points)
fu_time_values = [9.822845458984375e-05, 3.8530950546264648, 7.7004661560058594, 11.548807144165039, 15.393929004669189, 19.224869012832642, 23.072908163070679, 26.92710018157959, 30.773489236831665]
fu_time_deviations = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
fu_time_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax2.plot(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', label=r'$\mathrm{F\ddot{u}r-Kas}$')
ax2.errorbar(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', yerr=fu_time_CI_points)
#ax2.axhline(y=extime,  color='k')       #      set this also, for extime plotting
ax2.set_ylabel(r'$\mathrm{time}$')
leg1 = ax1.legend(loc=2, fancybox=True)
leg1.get_frame().set_alpha(0.5)
leg2 = ax2.legend(loc=1, fancybox=True)
leg2.get_frame().set_alpha(0.5)
plt.savefig('BHTofY1x1'+'time.pdf', format='pdf')
plt.savefig('BHTofY1x1'+'time.eps', format='eps')


fig = plt.figure(6)
NLIMIT_values = [1, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000]
ax1 = fig.add_subplot(111)
plt.ylabel(r'$\mathrm{HEL \/ Y1x1}$')
plt.xlabel(r'$\mathrm{number \/ of \/ observations}$')
rv_values = [0.24310371665702471, 0.07649338163122256, 0.074386692308798533, 0.04249140811841836, 0.039863892562961252, 0.039677174842252548, 0.030812609518103079, 0.02949962386379253, 0.03901411120984289]
rv_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax1.plot(NLIMIT_values, rv_values, 'b-', label=r'$\mathrm{random \/ vertex}$')
ax1.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
fu_values = [0.24310371665702471, 0.16436201134404288, 0.070216886495904698, 0.045324956378736708, 0.047655316706427753, 0.042215153019666975, 0.044367076204819722, 0.032361492053370841, 0.026641350116839779]
fu_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax1.plot( NLIMIT_values, fu_values, 'r-', label=r'$\mathrm{F\ddot{u}r-Kas}$')
ax1.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
ax1.set_yscale('log')
ax1.set_xlabel(r'$\mathrm{number \/ of \/ observations}$')
ax1.set_ylabel(r'$\mathrm{HEL}$')
ax2 = ax1.twinx()
rv_time_values = [5.4121017456054688e-05, 15.434289932250977, 30.512920141220093, 45.412091970443726, 60.64211893081665, 75.574176073074341, 90.450778007507324, 105.30454301834106, 120.12457299232483]
rv_time_deviations = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
rv_time_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax2.plot(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', label=r'$\mathrm{random \/ vertex}$')
ax2.errorbar(NLIMIT_values, rv_time_values, color='k',  linestyle='dashed', yerr=rv_time_CI_points)
fu_time_values = [9.822845458984375e-05, 3.8530950546264648, 7.7004661560058594, 11.548807144165039, 15.393929004669189, 19.224869012832642, 23.072908163070679, 26.92710018157959, 30.773489236831665]
fu_time_deviations = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
fu_time_CI_points = [nan, nan, nan, nan, nan, nan, nan, nan, nan]
ax2.plot(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', label=r'$\mathrm{F\ddot{u}r-Kas}$')
ax2.errorbar(NLIMIT_values, fu_time_values, color='k',  linestyle='solid', yerr=fu_time_CI_points)
#ax2.axhline(y=extime,  color='k')       #      set this also, for extime plotting
ax2.set_ylabel(r'$\mathrm{time}$')
leg1 = ax1.legend(loc=2, fancybox=True)
leg1.get_frame().set_alpha(0.5)
leg2 = ax2.legend(loc=1, fancybox=True)
leg2.get_frame().set_alpha(0.5)
plt.savefig('HELofY1x1'+'time.pdf', format='pdf')
plt.savefig('HELofY1x1'+'time.eps', format='eps')


