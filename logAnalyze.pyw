# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import os

###########################################################################
## Class LogAnalyse
###########################################################################

class LogAnalyseFrame ( wx.Frame ):
	
	def __init__( self, parent, title):
		super(LogAnalyseFrame, self).__init__(parent, title = title,size = (350,250))
			
		vBox = wx.BoxSizer( wx.VERTICAL )
		
		hBox1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.start = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		hBox1.Add( self.start, 0, wx.ALL, 5 )
		
		
		vBox.Add( hBox1, 1, wx.EXPAND, 5 )
		
		hBox2 = wx.BoxSizer( wx.VERTICAL )
		
		self.logPath = wx.StaticText( self, wx.ID_ANY, u"Log Path", wx.Point( 0,0 ), wx.DefaultSize, 0 )
		self.logPath.Wrap( -1 )
		hBox2.Add( self.logPath, 0, wx.ALL, 5 )
		
		self.textCtrlLogPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		hBox2.Add( self.textCtrlLogPath, 0, wx.ALL, 5 )
		
		
		vBox.Add( hBox2, 1, wx.EXPAND, 5 )
		
		hBox3 = wx.BoxSizer( wx.VERTICAL )
		
		self.logFile = wx.StaticText( self, wx.ID_ANY, u"LogFile", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.logFile.Wrap( -1 )
		hBox3.Add( self.logFile, 0, wx.ALL, 5 )
		
		self.textCtrlLogFile = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		hBox3.Add( self.textCtrlLogFile, 0, wx.ALL, 5 )
		
		
		vBox.Add( hBox3, 1, wx.EXPAND, 5 )
		
		hBox4 = wx.BoxSizer( wx.VERTICAL )
		
		self.viewPath = wx.StaticText( self, wx.ID_ANY, u"View Path", wx.Point( 0,0 ), wx.DefaultSize, 0 )
		self.viewPath.Wrap( -1 )
		hBox4.Add( self.viewPath, 0, wx.ALL, 5 )
		
		self.textCtrlViewPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( 5,5 ), wx.DefaultSize, 0 )
		hBox4.Add( self.textCtrlViewPath, 0, wx.ALL, 5 )
		
		
		vBox.Add( hBox4, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( vBox )
		self.Layout()		
		self.Centre( wx.BOTH )
		self.Show()
		self.Fit()
		
		# Connect Events
		self.start.Bind( wx.EVT_BUTTON, self.LogAnalyse )
		self.textCtrlLogPath.Bind( wx.EVT_TEXT_ENTER, self.GetLogPath )
		self.textCtrlLogFile.Bind( wx.EVT_TEXT_ENTER, self.GetLogFileName )
		self.textCtrlViewPath.Bind( wx.EVT_TEXT_ENTER, self.GetViewPath )
	
	
	# Virtual event handlers, overide them in your derived class
	def LogAnalyse( self, event ):
		cmd_1 = r'loganalyse.exe -dhlc ' 
		cmd_2 = r' |cfgdb_decoder.exe -'
		cmd_cfgdb = cmd_1+self.logPath+self.logFile+cmd_2+ '> '+self.logPath+self.decodedFile
		os.chdir(self.cmdPath) 
		os.system(cmd_cfgdb)
		event.Skip()
	
	def GetLogPath( self, event ):
		self.logPath = event.GetString()
		self.logPath = self.logPath+'\\'
		print self.logPath
		event.Skip()
		
	def GetLogFileName( self, event ):
		self.logFile = event.GetString()
		portion = os.path.splitext(self.logFile)
		self.decodedFile = portion[0]+".txt"
		print self.logFile
		print self.decodedFile
		event.Skip()
	
	def GetViewPath( self, event ):		
		self.cmdPath = event.GetString()
		self.cmdPath = self.cmdPath+r'\tm_build_system\build\host32'
		print self.cmdPath
		event.Skip()
	
app = wx.App() 
LogAnalyseFrame(None, 'LogAnalyse')

app.MainLoop()
