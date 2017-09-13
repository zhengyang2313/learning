#import os, sys
import argparse
import matplotlib.pyplot as plt
import pdb
import logging

logger_name = "log"

class ParseLog:
   def __init__(self, name, log):
      self.name = name
      self.logger = log
      self.time_dict = {}
      self.value_dict = {}
      self.result_time = {}
      self.result_value = {}
      self.starttime = 0
      self.endtime = 0
      #a = os.system("del *.rlt")


   def parseFile(self):
      logName = self.name
      with open(logName,'r') as sourcefile:
         for l in sourcefile:
            if l.find("LOG_HSDL_MAC_DL_DTCH_DCCH_SDU_DATA_HEADER_2") != -1:

               index = l.find(".")
               t=int(float(l[:index+4])*1000)

               index = l.find("HWI: ")
               ll = l[index+len("HWI: "):]
               index = ll.find(",")
               hwi = ll[:index]

               index = l.find("SduByteLen=")
               ll = l[index + len("SduByteLen="):]
               index = ll.find(",")
               dataLen = ll[:index]

               #pdb.set_trace()


               if not hwi in self.time_dict.keys():
                  self.time_dict[hwi] = [t]
                  self.value_dict[hwi] = [int(dataLen)]
                  if self.starttime > t or self.starttime == 0:
                     self.starttime = t
               else:
                  self.time_dict[hwi].append(t)
                  self.value_dict[hwi].append(int(dataLen))
                  if self.endtime < t:
                     self.endtime = t
      self.logParseResult_1()
      self.parseResultAllHwi()



   def logParseResult_1(self):
      self.logger.debug("start time:"+str(self.starttime))
      self.logger.debug("end time:"+str(self.endtime))
      for hwi in self.time_dict.keys():
         self.logger.debug("parse step 1, HWI:"+hwi)
         for i in range(len(self.time_dict[hwi])):
            self.logger.debug(str(self.time_dict[hwi][i])+":"+ str(self.value_dict[hwi][i]))

   def logParseResult_2(self):
      for hwi in self.result_time.keys():
         self.logger.debug("parse step 2, HWI:"+hwi)
         for i in range(len(self.result_time[hwi])):
            self.logger.debug(str(self.result_time[hwi][i])+":"+ str(self.result_value[hwi][i]))

   def parseResultAllHwi(self):
      for hwi in self.time_dict.keys():
         self.result_time[hwi], self.result_value[hwi] = self.parseResultHwi(hwi)
      self.logParseResult_2()


   def parseResultHwi(self, hwi):
      result_t = []
      result_v = []
      lt = self.time_dict[hwi]
      lv = self.value_dict[hwi]
      result_index = 0;
      result_t.append(self.starttime)
      result_v.append(0)

      for i in range(len(lt)):
         current_time = lt[i]
         if current_time == result_t[result_index]:
            result_v[result_index] += lv[i]
         elif current_time == result_t[result_index]+1:
            result_t.append(current_time)
            result_v.append(lv[i])
            result_index +=  1
         elif current_time > result_t[result_index]+1:
            while(result_t[result_index]+1 < current_time):
               result_t.append(result_t[result_index]+1)
               result_v.append(0)
               result_index = result_index + 1
            result_t.append(current_time)
            result_v.append(lv[i])
            result_index += 1

      timeDelta = self.endtime - self.starttime + 1 - len(result_t)
      if timeDelta > 0:
         result_v += [0]*timeDelta
         result_t += [result_t[-1]+1+i for i in range(timeDelta)]


      return result_t, result_v


   def preparePlotHwi(self, hwi, xscale, yscale='Mbps'):
      time_array = []
      byte_array = []

      mytime = self.result_time[hwi]
      value = self.result_value[hwi]

      for i in range(len(mytime)):
         if i % xscale == 0:
            time_array.append(mytime[i])
            byte_array.append(value[i])
         else:
            byte_array[i/xscale] += value[i]

      #x_array = map(lambda x:x-time_array[0], time_array)
      x_array = time_array

      if yscale == 'Mbps':
         y_array = map(lambda x:x*8*1000/1024/1024/xscale, byte_array)
         #plt.ylabel('throughput(Mbps)')
         #plt.ylim([0,250])
      elif yscale == 'Kbps':
         y_array = map(lambda x:x*8*1000/1024/xscale, byte_array)
         #plt.ylabel('throughput(Kbps)')
      else:
         y_array = map(lambda x:x*8*1000/xscale, byte_array)
         #plt.ylabel('throughput(bps)')

      return x_array, y_array

#      plt.plot(x_array,y_array,linewidth=1.0)
#      plt.xlabel('time(millisecond)')
#      plt.grid(True)
#      plt.xlim(0)
#      plt.show()

   def plotAllHwi(self, xscale):
      all_y = []
      n1 = len(self.result_time.keys())+1
      n2 = 1
      n3 = 1
      for hwi in self.result_time.keys():
         x_array, y_array = self.preparePlotHwi(hwi, xscale)
         all_y.append(y_array)
         ax = plt.subplot(n1, n2, n3)
         plt.plot(x_array, y_array)
         #ax.text(0.2, 0.2, 'HWI='+hwi, fontsize=12,bbox=dict(facecolor='red', alpha=0.5))
         ax.annotate('HWI='+hwi, xy=(0.01, 0.92), xycoords='axes fraction', fontsize=12,
                #xytext=(-5, 5),
                #textcoords='offset points',
                #ha='right', va='top'
                )
         #plt.xlabel('time(millisecond)')
         #plt.setp(ax.get_xticklabels(), visible=False)
         plt.ylabel('throughput(Mbps)')
         n3 += 1

      length = len(all_y[0])
      sum_y = [0]*length

      for i in range(len(all_y)):
         self.logger.debug("all_y[%d]=%d",i,len(all_y[i]))
         assert length == len(all_y[i])
         sum_y = [sum(x) for x in zip(sum_y, all_y[i])]

      ax = plt.subplot(n1, n2, n3)
      plt.plot(x_array, sum_y)
      ax.annotate('combined throughput', xy=(0.01, 0.92), xycoords='axes fraction', fontsize=12,
                #xytext=(-5, 5),
                #textcoords='offset points',
                #ha='right', va='top'
                )
      plt.xlabel('time(millisecond)')
      plt.ylabel('throughput(Mbps)')

      plt.show()





def set_logging(Level=logging.INFO):
      logger = logging.getLogger(logger_name)
      logger.setLevel(Level)
      fh = logging.FileHandler("logger.log", mode='w')
      fh.setLevel(Level)
      fmt = "%(asctime)s %(funcName)s %(lineno)d %(message)s"
      datefmt = "%H:%M:%S"
      formatter = logging.Formatter(fmt, datefmt)
      fh.setFormatter(formatter)
      logger.addHandler(fh)
      return logger


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Process HLC log and plot throughput over time')
   parser.add_argument('file', metavar='file', nargs='?', help='file path and name, for example: .\hlc.log')
   parser.add_argument('-t', '--time', type=int, default=5, help='time scale (millisecond) for X-axis, default is 5')
   parser.add_argument('-l', '--logging', default='INFO', choices=['INFO', 'DEBUG'], help='log level to set. Default is INFO')
   #parser.add_argument('-p', '--throughput', default='Mbps', choices=['Mbps', 'Kbps', 'bps'], help='throughput scale for Y-axis, default is Mbps')

   args = parser.parse_args()

   if args.time <= 0:
      print "time must be positive integer"
      exit(0)

   if args.logging == "DEBUG":
      loggingLevel = logging.DEBUG
   else:
      loggingLevel = logging.INFO
   logger = set_logging(loggingLevel)

   a = ParseLog(args.file, logger)
   a.parseFile()
   a.plotAllHwi(args.time)

#a.parseResult(sel)
#a.display_result(args.time, args.throughput)

