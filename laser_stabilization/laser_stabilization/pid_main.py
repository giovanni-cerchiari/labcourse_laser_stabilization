# Copyright: Giovanni Cerchiari
# date: 04/2021

# This application is designed for the teaching course "FPA"
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

#---------------------------------------------
from pyrpl import Pyrpl
import time
from matplotlib import pyplot as plt
import numpy as np
import wx
import threading
#----------------------------------------------
# -- Import that are part of this application --
# this import is designed to put the variables of the hardware
# and of the Graphical User Interface (GUI) as global
import mypid

# -----------------------------------------------------
# -----------------------------------------------------
# Configuration of the Redpitaya hardware
# -----------------------------------------------------
#-----------------------------------------------
# the input and output ports of the module "pid0" are configured
mypid.r.pid0.input = 'in1'
mypid.r.pid0.output_direct = 'out1'
# initialization of the proportional and integral coefficients
mypid.r.pid0.p = 0.0
mypid.r.pid0.i = 0.0
# initialization of the minimum and maximum output voltages
mypid.r.pid0.min_voltage = -1
mypid.r.pid0.max_voltage = 1
# defining a pre-filter to the data
# mypid.r.pid0.inputfilter = [0, 0]
# This is a second order filter with cutoff at 200 Hz
mypid.r.pid0.inputfilter = [200, 200]

# There exist a second PID module named "pid1"
# mypid.r.pid1.input = 'in2'
# mypid.r.pid1.output_direct = 'out2'
# initialization of the proportional and integral coefficients
# mypid.r.pid1.p = 0.0
# mypid.r.pid1.i = 0.0

def pid_idle():
  '''This function contains the main loop of the application.
  The user can interact with the PID controller via the main loop
  by using the appropriate callback. Callback functions are not intended
  to take over responsabilities of the main loop, but rather they 
  should execute as fast as possible. In this example the callbacks set
  some boolean variable to signal to the main loop the user request. Then,
  the main loop takes care of updating the status of the hardware according
  to the user wishes.'''

  print("entering main loop...")
  # cycle counter
  n=0
  dim = 1024

  # initializations necessary before entering into the main loop
  t_old = time.time()

  #--------------------------------------------------------------
  #--------------------------------------------------------------
  # Main Loop
  #--------------------------------------------------------------
  while(True):

    #------------------------------------------------
    # user interaction with the idle loop

    # Updating the p coefficient of the PID if requested
    if mypid.flg_button_p_update == True:
      mypid.update_p()
    # Updating the i coefficient of the PID if requested
    if mypid.flg_button_i_update == True:
      mypid.update_i()
    # Updating the setpoint of the PID if requested
    if mypid.flg_button_s_update == True:
      mypid.update_s()
    # Reading one voltage value from in1 if requested
    if mypid.flg_button_get_in1 == True:
      # read voltage value
      in1_value = r.scope.voltage_in1
      # display the value to the user
      text_in1_actual_value.SetValue(str(in1_value))
      # reset the condition
      mypid.flg_button_get_in1 = False
      #time.sleep(10)
    # The integral value of the PID is set to zero
    if mypid.flg_button_zero_ival==True:
      mypid.r.pid0.ival = 0
      mypid.flg_button_zero_ival = False
    #------------------------------------------------
    # time
    t = time.time()
    # time difference
    delta_t = t-t_old

    # the set point of the PID can be modified
    # to obtain a change of the output voltage 
    # r.pid0.setpoint = 0.5*np.cos(3*t)

    # the integral value can be modified
    # to obtain a change of the output voltage
    # r.pid0.setpoint = 0.5*np.cos(3*t)

    # update loop variables
    t_old = t
    n = (n+1)%dim

    # This sleep of 200 ms slows down the loop.
    # It is used to interact with Redpitaya via Pyrpl GUI,
    # which otherwise appears stuck.
    time.sleep(0.2)
  return


#-----------------------------------------------
#-----------------------------------------------
# Here, the idle function function containing
# the main loop that controls the PID is started.
# This function is started on a separate thread
# because it is designed execute in parralel to
# the Graphical User Interface (GUI)
# 
x = threading.Thread(target=pid_idle, args=())
x.start()
#---------------------------------------------
# opening the graphical user interface
mypid.frame.Show()
mypid.frame.Centre()
mypid.app.MainLoop()


