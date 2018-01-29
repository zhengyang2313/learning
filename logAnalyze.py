import os  
import argparse
import pdb

parser = argparse.ArgumentParser(description='Process HLC log')
parser.add_argument('view_path', metavar='view_path', nargs='?', help='The view path of loganalyse.exe, for example: C:\Projects\yzheng_view_CUE_TOT_uk')
parser.add_argument('log_path', metavar='log_path', nargs='?', help='The path of the log, for example: C:\Users\yzheng\Downloads\Run1')
parser.add_argument('log_filename', metavar='log_filename', nargs='?', help='filename of the log, for example: SLOG_LDMA_MUX_DATA_7699_20180123-10-11-20_1.dat')

args = parser.parse_args()


cmdpath = args.view_path+r'\tm_build_system\build\host32'

cmd_1 = r'loganalyse.exe -dhlc ' 
cmd_2 = r' |cfgdb_decoder.exe -'

logpath = args.log_path

#logfile = args.log_filename
#portion = os.path.splitext(logfile)
#decodedfile = portion[0]+".txt"

#cmd = cmd_1+logpath+logfile+' > '+logpath+decodefile
#cmd_cfgdb = cmd_1+logpath+logfile+cmd_2+ '> '+logpath+decodedfile
#print(cmd_cfgdb)
#print(cmdpath)
#os.chdir(cmdpath) 
#os.system(cmd_cfgdb)