# zeroth_orders_niriss

Created by Farhan Hasan (fhasan@stsci.edu), May 26, 2026

This script identifies locations of zeroth orders in JWST/NIRISS spectra, from dispersed images.

It inputs details of an object (object ID), filter, grism orientation, and x,y positions of zeroth order feature in a dispersed image. 
It outputs the wavelength of the zeroth order in the 1D spectrum, alongside some other numbers

In the python file, you will likely need to make changes after the line:

"###### ###### May need to modify this portion depending on your file structure ###### ###### May need to modify this portion depending on your file structure ######"


NIRISS Grism configs based on https://github.com/npirzkal/GRISM_NIRISS

Data structure based on, and software originally created for the JWST PASSAGE program (PID 1571; PI M. Malkan)
See the following repos: 
https://github.com/jwstwfss/line-finding
https://github.com/vihangmehta/PASSAGE_pipeline




