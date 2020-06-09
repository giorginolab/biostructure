#!/home/luis98/Documents/git-proyects/biostructure/Match_mrc_graph/pdb_mrc/EMAN2_py2/extlib/bin/python

'''
====================
Author: Jesus Galaz - 02/March/2013, Last update: 02/March/2013
====================

# This software is issued under a joint BSD/GNU license. You may use the
# source code in this file under either license. However, note that the
# complete EMAN2 and SPARX software packages have some GPL dependencies,
# so you are responsible for compliance with the licenses of these packages
# if you opt to use BSD licensing. The warranty disclaimer below holds
# in either instance.
#
# This complete copyright notice must be included in any revised version of the
# source code. Additional authorship citations may be added, but existing
# author citations must be preserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  2111-1307 USA
'''

from EMAN2 import *
import sys
from sys import argv
import EMAN2
import operator
import random
import numpy


def main():

	usage = """e2orthoproject.py <options> . 
			The options should be supplied in "--option=value" format (or --options=value:parameter1=value:parameter2=value... etc, 
			replacing "option" for a valid option name, and "value", "parameter" for a acceptable entries for that option. 
			This program extracts slices from a volume. By default, it will extract three orthogonal slices (one from each direction X, Y and Z) that go through the middle of the volume.
			"""
			
	parser = EMArgumentParser(usage=usage,version=EMANVERSION)	
	
	parser.add_argument("--path",type=str,default=None,help="""Directory to store results in. The default is a numbered series of directories containing the prefix 'orthoproject';
														for example, orthoproject_02 will be the directory by default if 'orthoproject_01' already exists.""")

	parser.add_argument("--onlymidx",action='store_true',default=False,help="Only extract the middle slice of the volume parallel to the YZ plane.")
	parser.add_argument("--onlymidy",action='store_true',default=False,help="Only extract the middle slice of the volume parallel to the XZ plane.")
	parser.add_argument("--onlymidz",action='store_true',default=False,help="Only extract the middle slice of the volume parallel to the XY plane.")
	
	parser.add_argument("--singlestack",action='store_true',default=False,help="""This option will save slices from all particles into a single .hdf stack file if --onlymidz or --onlymidy or --onlymidx are provided.""")
	
	parser.add_argument("--shrink",type=int,default=0,help="""Integer factor to use for shrinking volumes prior to extracting slices.""")
	
	parser.add_argument("--allx",action='store_true',default=False,help="Get ALL the slices in a volume along the x axis.")
	parser.add_argument("--ally",action='store_true',default=False,help="Get ALL the slices in a volume along the y axis.")
	parser.add_argument("--allz",action='store_true',default=False,help="Get ALL the slices in a volume along the z axis.")
	
	parser.add_argument("--orthogonaloff",action='store_true',default=False,help="""By default, the program will extract three orthogonal slices through the middle of the volume. 
																				If this parameter is specified, it will not.""")
	
	#parser.add_argument("--saverotvol",action='store_true',default=False,help="Will save the volume in each rotated position used to generate a projection.")

	parser.add_argument("--input", type=str, help="""The name of the input volume from which you want to generate orthogonal projections.
													You can supply more than one model either by providing an .hdf stack of models, or by providing multiple files
													separated by commas.""", default=None)

	parser.add_argument("--verbose", "-v", dest="verbose", action="store", metavar="n",type=int, default=0, help="verbose level [0-9], higner number means higher level of verboseness.")

	parser.add_argument("--ppid", type=int, help="Set the PID of the parent process, used for cross platform PPID",default=-1)

	parser.add_argument("--mask",type=str,help="Mask processor applied to particles before alignment. Default is None", default=None)
	parser.add_argument("--lowpass",type=str,help="A lowpass filtering processor (as in e2proc3d.py) to be applied to each volume prior to alignment. Not applied to aligned particles before averaging.", default=None)

	#parser.add_argument("--transformsfile",type=str,help="A text files containing lines with one triplet of az,alt,phi values each, representing the transforms to use to project a single volume supplied. ", default='')
	#parser.add_argument("--angles",type=str,help="A single comma or space separated triplet of az,alt,phi values representing the particle rotation to apply before projecting it.", default='')
	#parser.add_argument("--tag",type=str,help="When supplying --angles, tag the output projection with a string provided through --tag", default='')

	parser.add_argument("--normproc",type=str,help="""Normalization processor applied to particles before alignment. 
													Default is to use normalize.mask. If normalize.mask is used, results of the mask option will be passed in automatically. 
													If you want to turn this option off specify \'None\'""", default="normalize.mask")

	(options, args) = parser.parse_args()	
	
	
	if not options.input:
		try:
			print 'argv[1] is', argv[1]
			testimg = EMData(argv[1],0,True)
			options.input = argv[1]
		except:		
			#print 'argv[1] is', argv[1]
			print """\nERROR: Supply volume(s) through --input or as the first argument after the program name. For example, program.py volume.hdf --parameter1=value1 --parameter2=value2... etc."""
			sys.exit()
		
	logger = E2init(sys.argv, options.ppid)

	if options.mask: 
		options.mask=parsemodopt(options.mask)
		
	if options.lowpass: 
		options.lowpass=parsemodopt(options.lowpass)
		
	if options.normproc: 
		options.normproc=parsemodopt(options.normproc)

	
	'''
	Check for sanity of some supplied parameters
	'''

	if options.onlymidz:
		if options.onlymidx or options.onlymidy:
			print "ERROR: You can only supply one of --onlymidx, --onlymidy or --onlymidz at a time."
			sys.exit()
	
	if options.onlymidx:
		if options.onlymidy or options.onlymidz:
			print "ERROR: You can only supply one of --onlymidx, --onlymidy or --onlymidz at a time."
			sys.exit()
			
	if options.onlymidy:
		if options.onlymidx or options.onlymidz:
			print "ERROR: You can only supply one of --onlymidx, --onlymidy or --onlymidz at a time."
			sys.exit()


	'''
	Make a directory where to store the results
	'''

	if options.path and ("/" in options.path or "#" in options.path) :
		print "Path specifier should be the name of a subdirectory to use in the current directory. Neither '/' or '#' can be included. "
		sys.exit(1)

	if not options.path: 
		options.path = "slicer_01"
	
	files=os.listdir(os.getcwd())
	while options.path in files:
		if '_' not in options.path:
			options.path = options.path + '_00'
		else:
			jobtag=''
			components=options.path.split('_')
			if components[-1].isdigit():
				components[-1] = str(int(components[-1])+1).zfill(2)
			else:
				components.append('00')
						
			options.path = '_'.join(components)
			#options.path = path

	if options.path not in files:
		
		os.system('mkdir ' + options.path)
	
	
	'''
	Generate orthogonal slice regions
	'''
	
	sliceRs = []
	
	n = EMUtil.get_image_count( options.input )
	
	for i in range(n):
		print "processing particle", i
		a = EMData(options.input,i)
		
		ap = a.copy()
		if options.shrink:
			nyquist = ap['apix_x'] * 2.0
			shnyquist = nyquist * options.shrink
			ap.process_inplace('filter.lowpass.tanh',{'cutoff_freq':1.0/shnyquist})
			ap.process_inplace('math.meanshrink',{'n':options.shrink})
			
		nx=ap['nx']
		ny=ap['ny']
		nz=ap['nz']
		
		ptcltag = ''
		slicestag = ''
		
		if n > 1:
			slicestag = '_SLICESmid'
			
			if options.allz or options.ally or options.allx or not options.singlestack:
				ptcltag = '_ptcl' + str(i).zfill( len( str(n) ))
		
		rmid = None
					
		if options.onlymidz or options.onlymidy or options.onlymidx:
			
			if options.onlymidz:	
				rmid = Region(0, 0, nz/2, nx, ny, 1)
				print "The region for the orthogonal z slice is", rmid
				
				slicestag += 'z'
				if n < 2:
					slicestag = '_SLICEmidz'			
									
			elif options.onlymidx:
				rmid = Region(nx/2, 0, 0, 1, ny, nz)
				print "The region for the orthogonal x slice is", rmid

				#slicemidx=a.get_clip(rmidx)
				#slicemidx.write_image(options.path + '/' + options.input.replace('.',ptcltag+'_SLICEmidx.'),0)
				
				slicestag += 'x'
				if n < 2:
					slicestag = '_SLICEmidx'
				
				#Tx = Transform({'type':'eman','az':0,'alt':-90,'phi':0})
				#ap.transform( Tx )
	
			elif options.onlymidy:
				rmid = Region(0, ny/2, 0, nx, 1, nz)
				print "The region for the orthogonal y slice is", rmid
	
				#slicemidy=a.get_clip(rmidy)
				#slicemidy.write_image(options.path + '/' + options.input.replace('.',ptcltag+'_SLICEmidy.'),0)
				
				slicestag += 'y'
				if n < 2:
					slicestag = '_SLICEmidy'
				
				#Ty = Transform({'type':'eman','az':0,'alt':-90,'phi':-90})
				#ap.transform( Ty )
							
			
			slicemid = ap.get_clip( rmid )
			slicemid.set_size( nx, ny, 1)
			slicemid.write_image(options.path + '/' + os.path.basename( options.input ).replace('.',ptcltag + slicestag + '.'),i)
		
		elif not options.onlymidz and not options.onlymidy and not options.onlymidx:
			app = a.copy()
			if options.shrink:
				nyquist = app['apix_x'] * 2.0
				shnyquist = nyquist * options.shrink
				app.process_inplace('filter.lowpass.tanh',{'cutoff_freq':1.0/shnyquist})
				app.process_inplace('math.meanshrink',{'n':options.shrink})
			
			#regions={}
			if not options.orthogonaloff:
				print "Generating orthogonal slices"
				rmidz = Region(0, 0, nz/2, nx, ny, 1)
				rmidx = Region(nx/2, 0, 0, 1, ny, nz)
				rmidy = Region(0, ny/2, 0, nx, 1, nz)
				#tz = Transform({'type':'eman','az':0,'alt':0,'phi':0})

				regions={0:rmidz,1:rmidx,2:rmidy}
				#k=0
				for kk in regions:
					z=1
					if kk == 0:
						x=nx
						y=ny
				
					elif kk == 1:
						x=nz
						y=ny
					
					elif kk == 2:
						x=nx
						y=nz
				
					#if options.threed2threed or options.threed2twod:
					#d = EMData()
					#d.read_image(options.input, 0, False, regions[tag])
				
					print "I have extracted this orthogonal region", regions[kk]
					slice = app.get_clip(regions[kk])
					slice.set_size(x,y,1)
					slice.write_image(options.path + '/' + os.path.basename( options.input ).replace('.',ptcltag+'_SLICESortho.'),kk)
					print "The mean and index are", slice['mean'],kk
					#k+=1
				
			if options.allz:
				print "Generating all z slices"
				#Tz = Transform({'type':'eman','az':0,'alt':0,'phi':0})
				
				outname = options.path + '/' + os.path.basename( options.input ).replace('.',ptcltag+'_SLICESz.')
				os.system('e2proc2d.py ' + options.input + ' ' + outname + ' --threed2twod')
		
			if options.allx:
				print "Generating all x slices"
				Tx = Transform({'type':'eman','az':0,'alt':-90,'phi':0})
				volx = app.copy()
				volx.transform(Tx)
				rotvolxname = options.path + '/' + os.path.basename( options.input ).replace('.', ptcltag+'rotx.')
				volx.write_image(rotvolxname,0)
			
				outname = options.path + '/' + os.path.basename( options.input ).replace('.',ptcltag+'_SLICESx.')
			
				os.system('e2proc2d.py ' + rotvolxname + ' ' + outname + ' --threed2twod')
		
			if options.ally:	
				print "Generating all y slices"
				Ty = Transform({'type':'eman','az':0,'alt':-90,'phi':-90})
				voly = app.copy()
				voly.transform(Ty)
				rotvolyname = options.path + '/' + os.path.basename( options.input ).replace('.', ptcltag+'roty.')
				voly.write_image(rotvolyname,0)
			
				outname = options.path + '/' + os.path.basename( options.input ).replace('.',ptcltag+'_SLICESy.')
			
				os.system('e2proc2d.py ' + rotvolyname + ' ' + outname + ' --threed2twod')
			
	return()	

if __name__ == '__main__':
	main()
