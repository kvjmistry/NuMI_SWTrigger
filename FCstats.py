import sys
from ROOT import TEfficiency

if ( len(sys.argv) != 3):
    print
    print 'USAGE : python FCstats.py Ntotal Npass'
    print
    exit()
    
tot     = int(sys.argv[-2])
passing = int(sys.argv[-1])


k=TEfficiency()
k.SetStatisticOption(TEfficiency.kFFC)

# get +/- 1 sigma interval from Feldman Cousins statistics
eff       = passing/float(tot)
eff_upper = k.FeldmanCousins(tot,passing,0.6827,True)
eff_lower = k.FeldmanCousins(tot,passing,0.6827,False)

print 'Efficiency : %.03f.'%(eff)
print '1-sigma interval : [%.03f, %.03f]'%(eff_lower,eff_upper)
