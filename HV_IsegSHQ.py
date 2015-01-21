#! /usr/bin/env python

# Luis Ardila 	leardilap@unal.edu.co 	21/01/15

import sys
from PyQt4 import QtGui, QtCore, uic

from time import sleep

tangoEnable = True
if tangoEnable:
	import PyTango

class HV_Control(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
 
		self.ui = uic.loadUi('GUI_HV_IsegSHQ.ui')
		self.ui.show()
		
		#Declaring Device
		if tangoEnable:
			self.HV = PyTango.DeviceProxy("iss/detlab/hv2")
				
		#CH 1
		self.connect(self.ui.GetVoltage1, QtCore.SIGNAL("clicked()"), self.GetVoltage1)
		self.connect(self.ui.DesVoltage1, QtCore.SIGNAL("valueChanged(double)"), self.SetTargetVoltage1)
		self.connect(self.ui.SetVoltage1, QtCore.SIGNAL("clicked()"), self.SetVoltage1)
		self.connect(self.ui.GetRamp1, QtCore.SIGNAL("clicked()"), self.GetRamp1)
		self.connect(self.ui.SetRamp1, QtCore.SIGNAL("clicked()"), self.SetRamp1)
		self.connect(self.ui.Disable1, QtCore.SIGNAL("clicked()"), self.Disable1)
		
		self.ID = self.HV.getDeviceID()
		
		if str(self.ID) == "484215;3.09;4000V;3mA":		# This HV has only one port
			self.dual = False
		else:
			self.dual = True
		
		if self.dual:	
			#CH 2
			self.connect(self.ui.GetVoltage2, QtCore.SIGNAL("clicked()"), self.GetVoltage2)
			self.connect(self.ui.DesVoltage2, QtCore.SIGNAL("valueChanged(double)"), self.SetTargetVoltage2)
			self.connect(self.ui.SetVoltage2, QtCore.SIGNAL("clicked()"), self.SetVoltage2)
			self.connect(self.ui.GetRamp2, QtCore.SIGNAL("clicked()"), self.GetRamp2)
			self.connect(self.ui.SetRamp2, QtCore.SIGNAL("clicked()"), self.SetRamp2)
			self.connect(self.ui.Disable2, QtCore.SIGNAL("clicked()"), self.Disable2)
		else:
			self.ui.GetVoltage2.setEnabled(False)
			self.ui.SetVoltage2.setEnabled(False)
			self.ui.GetRamp2.setEnabled(False)
			self.ui.SetRamp2.setEnabled(False)
			self.ui.Disable2.setEnabled(False)
			self.ui.DesVoltage2.setEnabled(False)
			self.ui.DesRamp2.setEnabled(False)
		
					
		# Updating Voltage and Current
		self.timer = QtCore.QTimer()
		self.timer.start(2000)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.Update)
		
	# CH 1	   
	
	def GetVoltage1(self):
		if tangoEnable:
			voltage = self.HV.getTargetVoltage1()
		else:
			voltage = 1
		self.ui.DesVoltage1.setValue(voltage)
	
	def SetTargetVoltage1(self):
		voltage = self.ui.DesVoltage1.value()
		if tangoEnable:
			self.HV.setTargetVoltage1(voltage)
			
	def SetVoltage1(self):
		if tangoEnable:
			self.HV.changeVoltage1()
		
	def GetRamp1(self):
		if tangoEnable:
			ramp = self.HV.getVoltageRamp1()
		else:
			ramp = 1
		self.ui.DesRamp1.setValue(ramp)
	    
	def SetRamp1(self):
		ramp = self.ui.DesRamp1.value()
		if tangoEnable:
			self.HV.setVoltageRamp1(ramp)
		
	def Disable1(self):
		if tangoEnable:
			if self.ui.Disable1.isChecked():
				self.HV.setTargetVoltage1(0)
				sleep(1)
				self.SetVoltage1()
			else:
				self.SetTargetVoltage1()
				sleep(1)
				self.SetVoltage1()
		else:
			if self.ui.Disable1.isChecked():
				self.ui.Voltage1.display(0)
				self.ui.State1.setText("OFF")
			else:
				voltage = self.ui.DesVoltage1.value()
				self.ui.Voltage1.display(voltage)
				self.ui.State1.setText("ON")
	
	# CH 2
	
	def GetVoltage2(self):
		if tangoEnable:
			voltage = self.HV.getTargetVoltage2()
		else:
			voltage = 1
		self.ui.DesVoltage2.setValue(voltage)
	
	def SetTargetVoltage2(self):
		voltage = self.ui.DesVoltage2.value()
		if tangoEnable:
			self.HV.setTargetVoltage2(voltage)
			
	def SetVoltage2(self):
		if tangoEnable:
			self.HV.changeVoltage2()
		
	def GetRamp2(self):
		if tangoEnable:
			ramp = self.HV.getVoltageRamp2()
		else:
			ramp = 1
		self.ui.DesRamp2.setValue(ramp)
	    
	def SetRamp2(self):
		ramp = self.ui.DesRamp2.value()
		if tangoEnable:
			self.HV.setVoltageRamp2(ramp)
		
	def Disable2(self):			
		if tangoEnable:
			if self.ui.Disable2.isChecked():
				self.HV.setTargetVoltage2(0)
				sleep(1)
				self.SetVoltage2()
			else:
				self.SetTargetVoltage2()
				sleep(1)
				self.SetVoltage2()
		else:
			if self.ui.Disable2.isChecked():
				self.ui.Voltage2.display(0)
				self.ui.State2.setText("OFF")
			else:
				voltage = self.ui.DesVoltage2.value()
				self.ui.Voltage2.display(voltage)
				self.ui.State2.setText("ON")
	
	# Update
	
	def Update(self):
		if tangoEnable:
			if self.HV.getStatus1() == "ON\r":
				self.ui.State1.setText("ON")
				current = self.HV.getCurrent1()
				self.ui.Current1.display(float(current))
				voltage = self.HV.getVoltage1()
				self.ui.Voltage1.display(voltage)
			else:
				self.ui.State1.setText("OFF")
				
			if self.HV.getStatus2() == "ON\r" and self.dual:
				self.ui.State2.setText("ON")
				current = self.HV.getCurrent2()
				self.ui.Current2.display(float(current))
				voltage = self.HV.getVoltage2()
				self.ui.Voltage2.display(voltage)
			else:
				self.ui.State2.setText("OFF")
				
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = HV_Control()
	sys.exit(app.exec_())
