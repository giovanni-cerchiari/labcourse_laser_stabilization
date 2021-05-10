# Copyright: Giovanni Cerchiari
# date: 05/2021

# This application is designed for the teaching the 
# module "laser stabilization" of the course "FPA"
# at the University of Innsbruck.

# This is a free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# Diffmicro is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with the files. If not, see <https://www.gnu.org/licenses/>.

from pyrpl import Pyrpl
import time
import datetime
from matplotlib import pyplot as plt
import numpy as np
import os

# -----------------------------------------------
# USER SPECIFIC VARIABLES

# directory where the files will be saved
directory = os.path.join("D:\\","giovanni", "teaching", "data")
# Redpitaya address on network. Change this according to your network!!!
HOSTNAME = "169.254.107.161"
#-------------------------------------------------
# -----------------------------------------------
# FUNCTIONS

def Bode_plot(title, frequency, complex_signal):
  ''' This function shows a complex signal via a Bode plot.
  frequency -> vector of real numbers containing the frequencies.
  complex_signal -> vector of complex numbers containing the signal.
  '''
  fig = plt.figure()
  ax = fig.add_subplot(2, 1, 1)
  ax.plot(frequency, np.abs(complex_signal))
  ax.set_title(title)
  ax.set_xscale('log')
  ax.set_yscale('log')
  ax.set_xlabel('frequency')
  ax.set_ylabel('amplitude')
  ax = fig.add_subplot(2, 1, 2)
  ax.plot(frequency, np.angle(complex_signal))
  ax.set_xscale('log')
  ax.set_yscale('linear')
  ax.set_xlabel('frequency')
  ax.set_ylabel('phase (rad)')
  plt.show()
  return

def write_Bode_data_to_file(filename, red_pitaya, frequency, complex_signal):
  '''This function writes a complex signal to file.
  filename -> complete path of the file to be written
  frequency -> vector of real numbers containing the frequencies.
  complex_signal -> vector of complex numbers containing the signal.
  '''
  fileout = open(filename, "w")

  #------------------------
  # writing PI parameters to file
  fileout.write("PI data\n")
  fileout.write("p, %f\n" % red_pitaya.pid0.p)
  fileout.write("i, %f\n" % red_pitaya.pid0.p)
  fileout.write("filter")
  for n in range(4):
    fileout.write(", %f" % red_pitaya.pid0.inputfilter[n])
  fileout.write("\n\n")

  #-------------------------
  # writing Bode plot data
  fileout.write("Bode plot data\n")
  fileout.write("frequency, real, imaginary\n")
  dim = len(frequency)
  for n in range(dim):
    f = frequency[n]
    re = np.real(complex_signal[n]);
    im = np.imag(complex_signal[n])
    buf = "%f, %f, %f\n" % (f, re, im)
    fileout.write(buf)
  fileout.close()
  return

# -----------------------------------------------
# EXECUTION

# open Redpitaya
#r = RedPitaya(hostname=HOSTNAME)
p = Pyrpl(hostname=HOSTNAME)
na = p.networkanalyzer

# ------------------------------------------
# initialization of PI and network analyzer
# (uncomment if necessary)

na = p.networkanalyzer
na.iq_name = 'iq1'

# initializing ival to maximum value
p.rp.pid0.ival = -0.0
# waiting for the system to get in lock
time.sleep(5)

#--------------------------------------------------
# MAIN LOOP
# initializing cycle
iteration = 0
# continous measurements
while(True):
  #----------------
  # preparing output names
  identifier_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
  filename = "na_data_" + identifier_str + ".txt"
  filename_complete = os.path.join(directory, filename)
  #-----------------
  # Bode plot (uncomment if necessary)
  # acquiring data
  complex_signal = na.curve()

  # write to file
  write_Bode_data_to_file(filename_complete, p.rp, na.frequencies, complex_signal)

  # display Bode plot
  Bode_plot(filename, na.frequencies, complex_signal)
  
  #cycle iteration
  iteration = iteration+1
  print('iteration = %d' % iteration)
  time.sleep(5)
 
#--------------------------------------------------
