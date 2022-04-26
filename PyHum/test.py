## PyHum (Python program for Humminbird(R) data processing) 
## has been developed at the Grand Canyon Monitoring & Research Center,
## U.S. Geological Survey
##
## Author: Daniel Buscombe
## Project homepage: <https://github.com/dbuscombe-usgs/PyHum>
##
##This software is in the public domain because it contains materials that originally came from 
##the United States Geological Survey, an agency of the United States Department of Interior. 
##For more information, see the official USGS copyright policy at 
##http://www.usgs.gov/visual-id/credit_usgs.html#copyright
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

#"""
# ____        _   _                         
#|  _ \ _   _| | | |_   _ _ __ ___    _   _ 
#| |_) | | | | |_| | | | | '_ ` _ \  (_) (_)
#|  __/| |_| |  _  | |_| | | | | | |  _   _ 
#|_|    \__, |_| |_|\__,_|_| |_| |_| (_) (_)
#       |___/                               
#
##+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
#|b|y| |D|a|n|i|e|l| |B|u|s|c|o|m|b|e|
#+-+-+ +-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|d|a|n|i|e|l|.|b|u|s|c|o|m|b|e|@|n|a|u|.|e|d|u|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#"""

#python -c "import PyHum; PyHum.test.dotest()"

from cgi import print_environ
import PyHum
import os
import sys
import getopt
import shutil
import errno
 
def dircopy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

__all__ = [
    'dotest',
    ]

def dotest():

   argv=sys.argv[1:]
   options, args= getopt.getopt(argv, "c:n:")
   files=options[0][1]

   # copy files over to somewhere read/writeable
   dircopy(PyHum.__path__[0], os.path.expanduser("~")+os.sep+'pyhum_test')
   
   shutil.copy(PyHum.__path__[0]+os.sep+'input'+os.sep+files+'.DAT', os.path.expanduser("~")+os.sep+'pyhum_test'+os.sep+'input'+os.sep+files+'.DAT')

   # general settings   
   humfile = os.path.normpath(os.path.join(os.path.expanduser("~"),'pyhum_test','input',files+'.DAT'))
   input_dir = os.path.normpath(os.path.join(os.path.expanduser("~"),'pyhum_test','input',files))
   output = os.path.normpath(os.path.join(os.path.expanduser("~"),'pyhum_test','output'))

   doplot = 0 #yes

   # reading specific settings
   cs2cs_args = "epsg:26949" #arizona central state plane
   bedpick = 1 # auto bed pick
   c = 1450 # speed of sound fresh water
   t = 0.108 # length of transducer
   draft = 0.1 # draft in metres
   flip_lr = 0 # flip port and starboard
   model = "helix" # humminbird model
   calc_bearing = 1 #1=yes
   filt_bearing = 1 #1=yes
   chunk = '1' ##'d100' # distance, 100m
   #chunk = 'p1000' # pings, 1000
   #chunk = 'h10' # heading deviation, 10 deg

   ## read data in SON files into PyHum memory mapped format (.dat)
   PyHum.read(output,humfile, input_dir, cs2cs_args, c, draft, doplot, t, bedpick, flip_lr, model, calc_bearing, filt_bearing, chunk)

    # correction specific settings
   maxW = 500 # rms output wattage
   dofilt = 0 # 1 = apply a phase preserving filter (WARNING!! takes a very long time for large scans)
   correct_withwater = 1 # don't retain water column in radiometric correction (1 = retains water column for radiomatric corrections)
   ph = 8.0 # acidity on the pH scale
   temp = 30.0 # water temperature in degrees Celsius
   salinity = 0.0
   dconcfile = None

   PyHum.correct(humfile, output, maxW, doplot, dofilt, correct_withwater, ph, temp, salinity, dconcfile)


if __name__ == '__main__':
   dotest()

