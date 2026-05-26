#### Farhan Hasan (fhasan@stsci.edu); May 26, 2026
#### simple script to get location of zeroth order features in JWST/NIRISS spectra
#### from dispersed grism images


## import

import glob

import numpy as np
import os

from astropy.wcs import WCS
from astropy.io import fits, ascii
from astropy.table import Table, Column, join, vstack, hstack, unique
import astropy.units as u
from astropy.coordinates import SkyCoord, search_around_sky
from astropy.cosmology import Planck18 as cosmo


## inputs:

field_no = str(input('Please enter a field number\n'))
field = "Par" + field_no

obj_id = int(input('Please enter the object id\n'))

filter = str(input('Please enter the filter\n')).lower()

orient = str(input('Please enter the orientation\n')).lower()

grism = 'gr150' + orient

# orient = str(input('Please enter the orientation'))

x0 = float(input('Please enter the x-coord of zeroth order in dispersed image\n'))
y0 = float(input('Please enter the y-coord of zeroth order in dispersed image\n'))

## define configs for NIRISS:

#+1 BEAM coeffs
config_coeffs = {
'f115w_c':[6.355403e+01,-3.318593e+02,4.177346e-03], 
'f115w_r':[5.901531e+01,-3.311460e+02,-7.935992e-04],
'f150w_c':[6.355406e+01,-3.318593e+02,4.013016e-03],
'f150w_r':[5.901527e+01,-3.311460e+02,-7.094729e-04],
'f200w_c':[6.355443e+01,-3.318604e+02,4.675774e-03],
'f200w_r':[5.901527e+01,-3.311461e+02,-5.351753e-04]
}

###### ###### May need to modify this portion depending on your file structure ###### ###### May need to modify this portion depending on your file structure ###### 

## import files - this is based on file structure:

main_data_dir = "Data/"

field_dir = main_data_dir + str(field) + "/"

disp_image_file = field_dir + f"DATA/{field}_{filter}-{grism}_drz_sci.fits"

photcat_file = field_dir + f"DATA/DIRECT_GRISM/{field}_photcat.fits"


with fits.open(disp_image_file) as disp_file:
    
    disp_header = disp_file[0].header

    disp_file.close()

w = WCS(disp_header)


with fits.open(photcat_file) as phct_file:
    
    phot_cat = Table(phct_file[1].data)
    
    phct_file.close()
    
###### ###### ###### ###### ###### ###### ###### ###### 

## make measurements:

ind_ob = np.where(phot_cat['id'] == obj_id)[0]

ra_ob, dec_ob = phot_cat['ra'][ind_ob], phot_cat['dec'][ind_ob]
skycoord_ob = SkyCoord(ra=ra_ob*u.deg, dec=dec_ob*u.deg)

# values of centroids
x_src, y_src = w.world_to_pixel(skycoord_ob)

# +1 beam coefficients (from CONF file)

a_all = config_coeffs[f'{filter}_{orient}']
a0,a1,a2 = a_all[0],a_all[1],a_all[2]

dx = x0 - x_src[0]   # dispersion-axis offset
dy = y0 - y_src[0]   # y offset


# Evaluate wavelength polynomial (example 2nd order)
# lam0 = a0 + a1*dx + a2*dx**2 


# Solve quadratic: a2 t^2 + a1 t + (a0 - dx) = 0
if orient == 'c':
    coeffs = [a2, a1, a0 - dx]

elif orient == 'r':
    coeffs = [a2, a1, a0 - dy]


roots = np.roots(coeffs)

# choose physically valid root
# t = np.min(roots[np.isreal(roots)])

t = np.min(roots[np.where(roots>0)[0]])  # choose positive root


# wavelength
lamb = 0.75 + 1.55 * t

print("Zeroth order contamination wavelength (micron): ", lamb)
print(f"Other numbers: t={t}, dx={dx}, dy={dy}, coeffs={coeffs}. roots={roots}")

