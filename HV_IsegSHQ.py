# Luis Ardila 	leardilap@unal.edu.co 	21/11/14

import sys
from PyQt4 import QtGui, QtCore, uic

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
			self.axis = PyTango.DeviceProxy("iss/detlab/hv2")
				
		#CH 1
		self.connect(self.ui.GetVoltage1, QtCore.SIGNAL("clicked()"), self.GetVoltage1)
		self.connect(self.ui.SetVoltage1, QtCore.SIGNAL("clicked()"), self.SetVoltage1)
		self.connect(self.ui.GetRamp1, QtCore.SIGNAL("clicked()"), self.GetRamp1)
		self.connect(self.ui.SetRamp1, QtCore.SIGNAL("clicked()"), self.SetRamp1)
		self.connect(self.ui.Disable1, QtCore.SIGNAL("clicked()"), self.Disable1)
		
		#CH 2
		self.connect(self.ui.GetVoltage2, QtCore.SIGNAL("clicked()"), self.GetVoltage2)
		self.connect(self.ui.SetVoltage2, QtCore.SIGNAL("clicked()"), self.SetVoltage2)
		self.connect(self.ui.GetRamp2, QtCore.SIGNAL("clicked()"), self.GetRamp2)
		self.connect(self.ui.SetRamp2, QtCore.SIGNAL("clicked()"), self.SetRamp2)
		self.connect(self.ui.Disable2, QtCore.SIGNAL("clicked()"), self.Disable2)
		
		#Updating Voltage and Current
		self.timer = QtCore.QTimer()
		self.timer.start(300)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.Update)
		
	# CH 1	   
	
	def GetVoltage1(self):
		if tangoEnable:
			voltage = self.HV_Control.getTargetVoltage1()
		else:
			voltage = 1
		self.ui.DesVoltage1.setValue(voltage)
		
	def SetVoltage1(self):
		voltage = self.ui.DesVoltage1.value()
		if tangoEnable:
			self.HV_Control.setTargetVoltage1(voltage)
			self.HV_Control.changeVoltage1()
		else:
			self.ui.Voltage1.display(voltage)
		
	def GetRamp1(self):
		if tangoEnable:
			ramp = self.HV_Control.getVoltageRamp1()
		else:
			ramp = 1
		self.ui.DesRamp1.setValue(ramp)
	    
	def SetRamp1(self):
		ramp = self.ui.DesRamp1.value()
		if tangoEnable:
			self.HV_Control.setVoltageRamp1(ramp)
		
	def Disable1(self):
		if tangoEnable:
			if self.ui.Disable1.isChecked():
				self.HV_Control.setTargetVoltage1(0)
				self.HV_Control.changeVoltage1()
			else:
				voltage = self.ui.DesVoltage1.value()
				self.HV_Control.setTargetVoltage1(voltage)
				self.HV_Control.changeVoltage1()
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
			voltage = self.HV_Control.getTargetVoltage2()
		else:
			voltage = 1
		self.ui.DesVoltage2.setValue(voltage)
		
	def SetVoltage2(self):
		voltage = self.ui.DesVoltage2.value()
		if tangoEnable:
			self.HV_Control.setTargetVoltage2(voltage)
			self.HV_Control.changeVoltage2()
		else:
			self.ui.Voltage2.display(voltage)
		
	def GetRamp2(self):
		if tangoEnable:
			ramp = self.HV_Control.getVoltageRamp2()
		else:
			ramp = 1
		self.ui.DesRamp2.setValue(ramp)
	    
	def SetRamp2(self):
		ramp = self.ui.DesRamp2.value()
		if tangoEnable:
			self.HV_Control.setVoltageRamp2(ramp)
		
	def Disable2(self):			
		if tangoEnable:
			if self.ui.Disable2.isChecked():
				self.HV_Control.setTargetVoltage2(0)
				self.HV_Control.changeVoltage2()
			else:
				voltage = self.ui.DesVoltage2.value()
				self.HV_Control.setTargetVoltage2(voltage)
				self.HV_Control.changeVoltage2()
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
			if self.HV_Control.getStatus1():
				self.ui.State2.setText("ON")
				current = self.HV_Control.getCurrent1()
				self.ui.Current1.display(current)
				voltage = self.HV_Control.getVoltage1()
				self.ui.Voltage1.display(voltage)
			else:
				self.ui.State1.setText("OFF")
				
			if self.HV_Control.getStatus2():
				self.ui.State2.setText("ON")
				current = self.HV_Control.getCurrent2()
				self.ui.Current2.display(current)
				voltage = self.HV_Control.getVoltage2()
				self.ui.Voltage2.display(voltage)
			else:
				self.ui.State1.setText("OFF")
				
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	win = HV_Control()
	sys.exit(app.exec_())
