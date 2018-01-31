# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import os
import wx
import wx.xrc

###########################################################################
## Class LogAnalyse
###########################################################################

class LogAnalyseFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"LogAnalyse", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.LogFileName = wx.StaticText( self, wx.ID_ANY, u"The Log File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.LogFileName.Wrap( -1 )
		bSizer1.Add( self.LogFileName, 0, wx.ALL, 5 )
		
		self.LogFile = wx.FilePickerCtrl( self, wx.ID_ANY, u"SLOG_LDMA_MUX_DATA_7699_20180123-09-44-10_1.dat", u"Select a file", u"*.log ; *.mux; *.dat", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer1.Add( self.LogFile, 0, wx.ALL, 5 )
		
		self.ViewPath = wx.StaticText( self, wx.ID_ANY, u"The View Path", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ViewPath.Wrap( -1 )
		bSizer1.Add( self.ViewPath, 0, wx.ALL, 5 )
		
		self.ViewPath = wx.DirPickerCtrl( self, wx.ID_ANY, u"C:Projectsyzheng_view_CUE_TOT_uk", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer1.Add( self.ViewPath, 0, wx.ALL, 5 )
		
		self.Start = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.Start, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.LogFile.Bind( wx.EVT_FILEPICKER_CHANGED, self.GetLogFile )
		self.ViewPath.Bind( wx.EVT_DIRPICKER_CHANGED, self.GetViewPath )
		self.Start.Bind( wx.EVT_BUTTON, self.LogAnalyse )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def GetLogFile( self, event ):
		self.logFile = event.GetPath()
		portion = os.path.splitext(self.logFile)
		self.decodedFile = portion[0]+".txt"
		event.Skip()
	
	def GetViewPath( self, event ):
		self.viewPath = event.GetPath()
		self.cmdPath = self.viewPath+r'\tm_build_system\build\host32'
		print self.cmdPath 
		event.Skip()
	
	def LogAnalyse( self, event ):
		cmd_1 = r'loganalyse.exe -dhlc ' 
		cmd_2 = r' |cfgdb_decoder.exe -'
		cmd_cfgdb = cmd_1+self.logFile+cmd_2+ '> '+self.decodedFile
		os.chdir(self.cmdPath) 
		os.system(cmd_cfgdb)
		event.Skip()
	


app = wx.App(0)
# create a MyFrame instance and show the frame
LogAnalyseFrame(None).Show()
app.MainLoop()