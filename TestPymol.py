import __main__
__main__.pymol_argv = [ 'pymol', '-qei' ]
 
# Importing the PyMOL module will create the window.
import pymol
 
# Call the function below before using any PyMOL modules.
pymol.finish_launching()
 
pymol.cmd.stereo('walleye')
pymol.cmd.set('stereo_shift', 0.23)
pymol.cmd.set('stereo_angle', 1.0)
