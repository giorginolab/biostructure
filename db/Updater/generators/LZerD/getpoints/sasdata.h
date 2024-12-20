/*=============================================================================
 $Id: sas.h,v 1.5 2007/03/27 15:38:27 jkleinj Exp $
 POPS-A : Parameter OPtimised Surfaces at atomic resolution         
		  F. Fraternali and L. Cavallo (2002), 
		  Nucleic Acids Res. 30(13), 2950-2960.

C version

Copyright (C) 2002-2007 Franca Fraternali, program author
Copyright (C) 2002-2007 Luigi Cavallo, program author
Copyright (C) Kuang Lin (translation of original Fortran code to C, 07.08.2002)
Copyright (C) 2007 Jens Kleinjung, code support
                                      
License:
    This program is free software; you can redistribute it and/or modify                                                                       
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
=============================================================================*/

#ifndef SAS_H
#define SAS_H

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <cfloat>
#include <vector>

using namespace std;

#include "classes.h"

/*
#ifndef BOOL
#define BOOL int 
#endif
#ifndef TRUE
#define TRUE  (1)
#define FALSE (0)
#endif
*/

static const double  SAS_PI    = 3.141592654;
static const double  SAS_RSOLV = 1.4000;

/*____________________________________________________________________________*/
/* common keys stores the keywords set up in the input */
static bool SAS_k_fast=true; 

/*____________________________________________________________________________*/
/* AMINO ACID NAMES AND PROPERTIES */
static const char NUM_CHAR[30]="ARNDCQEGHILKMFPSTWYVBZX-"; 

#define SAS_maxAtoms (35000)
#define SAS_maxBonds (SAS_maxAtoms +1000)
    
/*____________________________________________________________________________*/
/*  common topol stores:
  nMol = number of molecules
  nRes = number of residues in the molecule
  nAt  = number of atoms in the molecule
  nTotAt = total number of atoms 
  nBon = total number of bonds
  nAng = total number of angles
  nTor = total number of torsions
  nNonBon = total number of overlapping L-J (non-bonded) atoms
  arrays ib & jb            = atoms forming the bonds
  arrays it & jt & kt       = atoms forming the angles
  arrays ip & jp & kt & lp  = atoms forming the torsions
  arrays in & jn            = atoms forming the L-J overlaps*/
/*____________________________________________________________________________*/
int SAS_nMol,SAS_nRes,SAS_nTotAt,SAS_nAt,SAS_nBon,SAS_nAng,SAS_nTor,
  SAS_nNonBon;
int SAS_ib[SAS_maxBonds], SAS_jb[SAS_maxBonds];
int SAS_it[ 3*SAS_maxBonds], SAS_jt[ 3*SAS_maxBonds ],
  SAS_kt[3*SAS_maxBonds];
int SAS_ip[ 5*SAS_maxBonds ], SAS_jp[ 5*SAS_maxBonds ],
  SAS_kp[5*SAS_maxBonds], SAS_lp[5*SAS_maxBonds];
int SAS_in[30*SAS_maxAtoms], SAS_jn[30*SAS_maxAtoms]; 

/*____________________________________________________________________________*/
/*  common datay stores data from the sas.data file
  array SAS_ARADIUS = radius of all atom types
  array SAS_APARA   = sas param of atom types
  array SAS_AKPOL   = keyword to mark atoms as polar or not
  array SAS_RTYPES  = labels of residue types
  array SAS_ATYPES  = labels of atom types
  int   SAS_NUM_ATYPES  = number of atom types*/
/*____________________________________________________________________________*/
/* number of atom types */
static const int SAS_NUM_ATYPES = 39; /* for atoms */

/*____________________________________________________________________________*/
/* residue types */
static const char SAS_RTYPES[22][4]={"",
    "ALA","ARG","ASN","ASP","CYS", /* ARNDC  */
    "GLN","GLU","GLY","HIS","ILE", /* QEGHI  */
    "LEU","LYS","MET","OXT","PHE", /* LKMOF */
    "PRO","SER","THR","TRP","TYR","VAL"};/* PSTWYV  */

/*____________________________________________________________________________*/
/* atom types */
static const char SAS_ATYPES[39][4]={
    "C","CA","CB","CD","CD1","CD2","CE","CE1","CE2","CE3",
    "CG","CG1","CG2","CH2","CZ","CZ2","CZ3","N","ND1",
    "ND2","NE","NE1","NE2","NH1","NH2","NZ","O","O1","O2",
    "OD1","OD2","OE1","OE2","OG","OG1","OH","OXT","SD","SG"};

/*____________________________________________________________________________*/
/* atom radii per residue */
static double const SAS_ARADIUS[22][39]={
        {0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00}, /**/
        {1.72,1.80,2.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*ALA*/
        {1.72,1.80,1.90,1.90,0.00,0.00,0.00,0.00,0.00,0.00,1.90,0.00,0.00,0.00,1.72,0.00,0.00,1.55,0.00,0.00,1.55,0.00,0.00,1.55,1.55,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*ARG*/
        {1.72,1.80,1.90,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.72,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*ASN*/
        {1.72,1.80,1.90,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.72,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*ASP*/
        {1.72,1.80,1.90,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,1.80}, /*CYS*/
        {1.72,1.80,1.90,1.72,0.00,0.00,0.00,0.00,0.00,0.00,1.90,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,1.50,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*GLN*/
        {1.72,1.80,1.90,1.72,0.00,0.00,0.00,0.00,0.00,0.00,1.90,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,1.50,1.50,0.00,0.00,0.00,1.50,0.00,0.00}, /*GLU*/
        {1.90,1.80,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*GLY*/
        {1.72,1.80,1.90,0.00,0.00,1.80,0.00,1.80,0.00,0.00,1.72,0.00,0.00,0.00,0.00,0.00,0.00,1.55,1.55,0.00,0.00,0.00,1.55,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*HIS*/
        {1.72,1.80,1.80,2.00,2.00,0.00,0.00,0.00,0.00,0.00,0.00,1.90,2.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*ILE*/
        {1.72,1.80,1.90,0.00,2.00,2.00,0.00,0.00,0.00,0.00,1.80,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*LEU*/
        {1.72,1.80,1.90,1.90,0.00,0.00,1.90,0.00,0.00,0.00,1.90,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.55,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*LYS*/
        {1.72,1.80,1.90,0.00,0.00,0.00,2.00,0.00,0.00,0.00,1.90,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.80,0.00}, /*MET*/
        {0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*OXT*/
        {1.72,1.80,1.90,0.00,1.80,1.80,0.00,1.80,1.80,0.00,1.72,0.00,0.00,0.00,1.80,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*PHE*/
        {1.72,1.80,1.90,1.90,0.00,0.00,0.00,0.00,0.00,0.00,1.90,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*PRO*/
        {1.72,1.80,1.90,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,1.50,0.00,0.00,1.50,0.00,0.00}, /*SER*/
        {1.72,1.80,1.80,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,2.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,1.50,0.00,1.50,0.00,0.00}, /*THR*/
        {1.72,1.80,1.90,0.00,1.80,1.72,0.00,0.00,1.72,1.80,1.72,0.00,0.00,1.80,0.00,1.80,1.80,1.55,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00}, /*TRP*/
        {1.72,1.80,1.90,0.00,1.80,1.80,0.00,1.80,1.80,0.00,1.72,0.00,0.00,0.00,1.72,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,1.50,0.00,0.00,0.00,0.00,0.00,0.00,1.50,1.50,0.00,0.00}, /*TYR*/
        {1.72,1.80,1.80,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,2.00,2.00,0.00,0.00,0.00,0.00,1.55,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.50,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00} /*VAL*/
};

/*____________________________________________________________________________*/
/* atom parameters per residue */
static double const SAS_APARA[22][39]={
        {0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00}, /**/
        {1.58277,1.13196,0.85415,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.27927,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.01366,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*ALA*/
        {1.53010,1.29665,1.14901,1.18411,0.00,0.00,0.00,0.00,0.00,0.00,1.09637,0.00,0.00,0.00,1.73775,0.00,0.00,1.41986,0.00,0.00,1.18332,0.00,0.00,0.92815,0.82331,0.00,0.97459,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*ARG*/
        {1.50052,1.41296,1.07744,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.40541,0.00,0.00,0.00,0.00,0.00,0.00,1.41861,0.00,0.73229,0.00,0.00,0.00,0.00,0.00,0.00,0.97085,1.01573,1.01573,0.89982,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*ASN*/
        {1.52156,1.37347,1.03193,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.24446,0.00,0.00,0.00,0.00,0.00,0.00,1.36263,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95044,1.01573,1.01573,0.90135,0.86936,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*ASP*/
        {1.64337,1.32918,1.05026,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.37480,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.01921,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.91062}, /*CYS*/
        {1.52142,1.27569,1.23213,1.40162,0.00,0.00,0.00,0.00,0.00,0.00,1.02930,0.00,0.00,0.00,0.00,0.00,0.00,1.38443,0.00,0.00,0.00,0.00,0.81290,0.00,0.00,0.00,0.96669,1.01573,1.01573,0.00,0.00,1.01573,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*GLN*/
        {1.65417,1.27657,1.22284,1.23713,0.00,0.00,0.00,0.00,0.00,0.00,1.02489,0.00,0.00,0.00,0.00,0.00,0.00,1.31333,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.96273,1.01573,1.01573,0.00,0.00,0.99838,0.97070,0.00,0.00,0.00,0.95021,0.00,0.00}, /*GLU*/
        {1.58371,0.80624,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.21888,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.87720,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*GLY*/
        {1.57469,1.33273,1.14506,0.00,0.00,0.99188,0.00,0.90798,0.00,0.00,1.45878,0.00,0.00,0.00,0.00,0.00,0.00,1.47688,0.95877,0.00,0.00,0.00,0.81807,0.00,0.00,0.00,0.96123,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*HIS*/
        {1.70209,1.54049,1.29118,1.00563,1.00563,0.00,0.00,0.00,0.00,0.00,0.00,1.12289,1.11352,0.00,0.00,0.00,0.00,1.56373,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.99356,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*ILE*/
        {1.42167,1.60971,1.28219,0.00,0.98706,0.98376,0.00,0.00,0.00,0.00,1.24985,0.00,0.00,0.00,0.00,0.00,0.00,1.44831,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.97860,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*LEU*/
        {1.62377,1.28771,1.15853,1.02432,0.00,0.00,1.04330,0.00,0.00,0.00,1.15034,0.00,0.00,0.00,0.00,0.00,0.00,1.46057,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.96664,0.95563,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*LYS*/
        {1.35015,1.31812,1.25099,0.00,0.00,0.00,0.97466,0.00,0.00,0.00,1.13077,0.00,0.00,0.00,0.00,0.00,0.00,1.15247,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.02411,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.96051,0.00}, /*MET*/
        {0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*OXT*/
        {1.51887,1.36164,1.17335,0.00,1.18006,1.17640,0.00,1.05697,1.06879,0.00,1.52449,0.00,0.00,0.00,0.97986,0.00,0.00,1.33648,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.98697,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*PHE*/
        {1.65542,1.19567,0.93773,1.06677,0.00,0.00,0.00,0.00,0.00,0.00,0.81343,0.00,0.00,0.00,0.00,0.00,0.00,1.44795,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.93809,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*PRO*/
        {1.60037,1.17963,0.88991,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.41407,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.98617,1.01573,1.01573,0.00,0.00,0.00,0.00,0.91711,0.00,0.00,0.95021,0.00,0.00}, /*SER*/
        {1.73769,1.31990,1.11971,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.85245,0.00,0.00,0.00,0.00,1.49152,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.96399,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.97343,0.00,0.95021,0.00,0.00}, /*THR*/
        {1.56445,1.31052,1.17397,0.00,1.00759,1.43736,0.00,0.00,1.44270,1.34460,1.49060,0.00,0.00,0.93948,0.00,1.07916,0.98392,1.37426,0.00,0.00,0.00,0.94377,0.00,0.00,0.00,0.00,0.95927,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95021,0.00,0.00}, /*TRP*/
        {1.56517,1.32843,1.18076,0.00,1.18400,1.19825,0.00,1.03021,1.07430,0.00,1.48453,0.00,0.00,0.00,1.31196,0.00,0.00,1.31289,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.95088,1.01573,1.01573,0.00,0.00,0.00,0.00,0.00,0.00,1.00596,0.95021,0.00,0.00}, /*TYR*/
        {1.74084,1.42217,1.19676,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.96158,0.95586,0.00,0.00,0.00,0.00,1.54371,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.00253,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00} /*VAL*/
};

/*____________________________________________________________________________*/
/* */
static int const SAS_AKPOL[22][39]={
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, /**/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*ALA*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*ARG*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0}, /*ASN*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,0,0}, /*ASP*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*CYS*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,1,0,0,0,0,1,0,0}, /*GLN*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,0,0,1,0,0}, /*GLU*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*GLY*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*HIS*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*ILE*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*LEU*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*LYS*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*MET*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0}, /*OXT*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*PHE*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*PRO*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1,0,0}, /*SER*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,1,0,0}, /*THR*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0}, /*TRP*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0}, /*TYR*/
        {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0} /*VAL*/
};

/*____________________________________________________________________________*/
/*  common ressy stores the following data for the molecule:
  array aNames = names of the atoms
  array rNames = residue name to which the atom belongs
  array aNum   = atom number
  array rNum   = residue number to which the atom belongs
  array aCoord  = cartesian coordinates
  array aTotSurface  = area of isolated atoms
  array aSasa  = sasa of atoms in the molecule
  array nOverlap = number of overlaps for each atom
  array ntotOverlap = number of overlaps for each residue
  array aPhobicSasa = sum of hydrophobic atoms sasa for each residue
  array aPhilicSasa = sum of hydrophilic atoms sasa for each residue
  array akPol  = keyword to mark atoms as polar or not
  array rType  = identifier to denote residue types
  array aType  = identifier to denote atom types*/
/*____________________________________________________________________________*/
char   SAS_aNames[SAS_maxAtoms][8],SAS_rNames[SAS_maxAtoms][8] ;
int    SAS_aNum[SAS_maxAtoms];
int    SAS_rNum[SAS_maxAtoms];
double SAS_aCoord[3*SAS_maxAtoms];

double SAS_aTotSurface[SAS_maxAtoms],SAS_aSasa[SAS_maxAtoms];
int    SAS_nOverlap[SAS_maxAtoms], SAS_ntotOverlap[SAS_maxAtoms];
double SAS_aPhobicSasa[SAS_maxAtoms],SAS_aPhilicSasa[SAS_maxAtoms];
int    SAS_akPol[SAS_maxAtoms],SAS_rType[SAS_maxAtoms],SAS_aType[SAS_maxAtoms];

/*____________________________________________________________________________*/
/* SAS_PCON =  connectivity parameters */
static double const SAS_PCON12 = 0.91463, SAS_PCON13 = 0.24511;   
static double const SAS_PCON14 = -0.32226, SAS_PCON15 = 0.58720 ;

void get_topology();                     /* get the topology */
void calc_atomic_sasa(double pcon,int i,int j);/* calculate sasa of atom */
void calc_mol_sasa();                       /* calculate sasa of molecule */
void assign_param(vector<atom>&);
void assign_areas(vector<atom>&, int&);

#endif /* SAS_H */

