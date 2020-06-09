#!/home/luis98/Documents/git-proyects/biostructure/Match_mrc_graph/pdb_mrc/EMAN2_py2/extlib/bin/python
# this simple program will find the approximate resolution of the first zero as a function of defocus
# computationally. While you could compute a functional form as well, this demonstrates some useful
# EMAN2 programming techniques

from EMAN2 import *
from numpy import *

c=EMAN2Ctf()
c.voltage=200
c.cs=1
c.ampcont=100.0		# this is for phase plate imaging (roughly)

for d in arange(0,20.0,.1):
	c.defocus=d
	ct=c.compute_1d(5002,.0001,c.CtfType.CTF_AMP)
	for i,s in enumerate(arange(0,0.25,.0001)):
		if ct[i]*ct[i+1]<=0 : break	

	print "%1.2f\t%1.2f"%(d,1/s)
