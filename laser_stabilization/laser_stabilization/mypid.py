
# Copyright: Giovanni Cerchiari
# date: 04/2021

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
import wx
import numpy as np

# -----------------------------------------------------
# -----------------------------------------------------
# Communication with the Redpitaya hardware
# -----------------------------------------------------
# Redpitaya address on network. Change this according to your network!!!
HOSTNAME = "169.254.107.161"
# open Redpitaya
#r = RedPitaya(hostname=HOSTNAME)
p = Pyrpl(hostname=HOSTNAME)
r = p.rp
na = p.networkanalyzer
na.iq_name = 'iq1'
# -----------------------------------------------------
# -----------------------------------------------------
# Graphical User Interface (GUI)
# -----------------------------------------------------
# preparing the Graphical User Interface enviroment (GUI)
app = wx.App()
frame = wx.Frame(None, -1, 'win.py')
frame.SetDimensions(100,100,800,500)
panel = wx.Panel(frame, wx.ID_ANY)
#------------------------------------------------------
# descriptive textbox
text_actual_value = wx.TextCtrl( panel, value = "value", pos=(140, 10), size=(120, 25),
   style = wx.TE_READONLY | wx.TE_CENTER )
text_actual_value = wx.TextCtrl( panel, value = "new value", pos=(300, 10), size=(100, 25),
   style = wx.TE_READONLY | wx.TE_CENTER ) 
# ---------
# proportional coefficient user interface

ypos = 40
text_p_description = wx.TextCtrl( panel, value = "p coefficient", pos=(10, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
text_p_actual_value = wx.TextCtrl( panel, value = "", pos=(140, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
text_p_write = wx.TextCtrl( panel, value = "", pos=(300, ypos), size=(100, 40),
   style = wx.TE_LEFT ) 
button_p_update = wx.Button(panel, wx.ID_ANY, 'Update p coefficient', pos=(500, ypos), size=(200, 40))

# variable that is monitored in the main loop
flg_button_p_update = False

#callback
def onButton_p_update(event):
    global flg_button_p_update
    if flg_button_p_update == False:
        flg_button_p_update = True

# binding callback to the button
button_p_update.Bind(wx.EVT_BUTTON, onButton_p_update)
#-----------
# integral coefficient user interface
ypos = 90
text_i_description = wx.TextCtrl( panel, value = "i coefficient", pos=(10, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
text_i_actual_value = wx.TextCtrl( panel, value = "", pos=(140, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
text_i_write = wx.TextCtrl( panel, value = "", pos=(300, ypos), size=(100, 40),
   style = wx.TE_LEFT ) 
button_i_update = wx.Button(panel, wx.ID_ANY, 'Update i coefficient', pos=(500, ypos), size=(200, 40))

# variable that is monitored in the main loop
flg_button_i_update = False

# callback
def onButton_i_update(event):
    global flg_button_i_update
    if flg_button_i_update == False:
        flg_button_i_update = True

# binding callback to the button
button_i_update.Bind(wx.EVT_BUTTON, onButton_i_update)
#-----------
# set-point user interface
ypos = 140
text_s_description = wx.TextCtrl( panel, value = "set point", pos=(10, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
text_s_actual_value = wx.TextCtrl( panel, value = "", pos=(140, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
text_s_write = wx.TextCtrl( panel, value = "", pos=(300, ypos), size=(100, 40),
   style = wx.TE_LEFT ) 
button_s_update = wx.Button(panel, wx.ID_ANY, 'Update set point', pos=(500, ypos), size=(200, 40))

# variable that is monitored in the main loop
flg_button_s_update = False

# callback
def onButton_s_update(event):
    global flg_button_s_update
    if flg_button_s_update == False:
        flg_button_s_update = True

# binding callback to the button
button_s_update.Bind(wx.EVT_BUTTON, onButton_s_update)
#-----------
# read in1 user interface
ypos = 400
text_get_in1_description = wx.TextCtrl( panel, value = "voltage in1", pos=(10, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
text_in1_actual_value = wx.TextCtrl( panel, value = "", pos=(140, ypos), size=(120, 40),
   style = wx.TE_READONLY | wx.TE_LEFT ) 
button_get_in1_update = wx.Button(panel, wx.ID_ANY, 'Get value', pos=(500, ypos), size=(200, 40))
# variable that is monitored in the main loop
flg_button_get_in1 = False
#----------------------------------
# zero the integral value of the PID -> user interface
ypos = 350 
button_zero_ival = wx.Button(panel, wx.ID_ANY, 'Zero integral value', pos=(500, ypos), size=(200, 40))
# variable that is monitored in the main loop
flg_button_zero_ival = False
# callback
def onButton_zero_ival(event):
    global flg_button_zero_ival
    if flg_button_zero_ival == False:
        flg_button_zero_ival = True

# binding call back to the visual object
button_zero_ival.Bind(wx.EVT_BUTTON, onButton_zero_ival)

#---------------------------------
# zero the integral value of the PID -> user interface
ypos = 350 
button_na = wx.Button(panel, wx.ID_ANY, 'Start na', pos=(200, ypos), size=(200, 40))
# variable that is monitored in the main loop
flg_button_na = False
# callback
def onButton_na(event):
    global flg_button_na
    if flg_button_na == False:
        flg_button_na = True

# binding call back to the visual object
button_na.Bind(wx.EVT_BUTTON, onButton_na)

#---------------------------------

def update_p():
  ''' Update the p coefficient of the PID.
  To update, write in the textbox and click on the button.'''
  global r
  global text_p_actual_value
  global text_p_write
  global flg_button_p_update
  # read the string set by the user
  thestring = text_p_write.GetValue()
  try:
    # convert the string into a floating point number
    new_value = np.float(thestring)
    # modify the coefficient of the pid
    r.pid0.p = new_value
    # notify the user the new value
    text_p_actual_value.SetValue(str(new_value))
    print(new_value)
  except:
    print("Invalid number input")
  # reset the condition
  flg_button_p_update = False

def update_i():
  ''' Update the i coefficient of the PID.
 To update, write in the textbox and click on the button.'''
  global r
  global text_i_actual_value
  global text_i_write
  global flg_button_i_update
  # read the string set by the user
  thestring = text_i_write.GetValue()
  try:
    # convert the string into a floating point number
    new_value = np.float(thestring)
    # modify the coefficient of the pid
    r.pid0.i = new_value
    # notify the user the new value
    text_i_actual_value.SetValue(str(new_value))
    print(new_value)
  except:
    print("Invalid number input")
  # reset the condition
  flg_button_i_update = False

def update_s():
  ''' Update the set point of the PID .
  To update, write in the textbox and click on the button.'''
  global r
  global text_s_actual_value
  global text_s_write
  global flg_button_s_update
  # read the string set by the user
  thestring = text_s_write.GetValue()
  try:
    # convert the string into a floating point number
    new_value = np.float(thestring)
    # modify the coefficient of the pid
    r.pid0.setpoint = new_value
    # notify the user the new value
    text_s_actual_value.SetValue(str(new_value))
    print(new_value)
  except:
    print("Invalid number input")
  # reset the condition
  flg_button_s_update = False


def start_network_analyzer():
  ''' Update the set point of the PID .
  To update, write in the textbox and click on the button.'''
  global na

    # setup network analyzer with the right parameters
  #na.setup(start=1e3,stop=62.5e6,points=1001,rbw=1000, avg=1,
  #amplitude=0.2,input='iq1',output_direct='off', acbandwidth=0)

  #take transfer functions. first: iq1 -> iq1, second iq1->out1->(your cable)->adc1
  #iq1 = na.curve()
  #na.setup(input='in1', output_direct='out1')
  in1 = na.curve()

  # get x-axis for plotting
  f = na.frequencies

  flg_button_na = False
  return