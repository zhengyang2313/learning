#import os, sys
import argparse
import matplotlib.pyplot as plt
import pdb


class ParseLog:
   def __init__(self, name):
      self.name = name
      self.saeList = []
      self.time_dict = {}
      self.value_dict = {}
      self.result_t = []
      self.result_v = []
      #a = os.system("del *.rlt")


   def parseFile(self):
      logName = self.name
      with open(logName,'r') as sourcefile:
         for l in sourcefile:
            if l.find("LOG_HSDL_PDCP_DL_SDU_INFO") != -1:
               
               index = l.find(".")
               t=int(float(l[:index+4])*1000)

               index = l.find("SAE Id:")
               ll = l[index+8:]
               index = ll.find(",")
               saeId = ll[:index]

               index = l.find("(Bytes):")
               ll = l[index + len("(Bytes):"):]
               index = ll.find(",")
               dataLen = ll[:index]

               if not saeId in self.saeList:
                  self.saeList.append(saeId)
                  self.time_dict[saeId] = [t]
                  self.value_dict[saeId] = [int(dataLen)]
               else:
                  self.time_dict[saeId].append(t)
                  self.value_dict[saeId].append(int(dataLen))

               #self.saveInfo(saeId, t + ":" + dataLen + "\n")


         
   #def saveInfo(self, saeId, l):
   #   filename = "sae_" + saeId + ".rlt"
   #   with open(filename,'a+') as resultFile:
   #      resultFile.write(l)

   def getSaeFromUser(self):
      print "there are " + str(len(self.saeList)) + " SAE in log, they IDs are:"
      for a in self.saeList:
         print a
      while(True):
         b = raw_input("please input SAE:")
         if b in self.saeList:
            break
      return b



   def parseResult(self, saeId):
   #   filename = "sae_" + saeId + ".rlt"
   #   resultFile = open(filename,'a+')
       lt = self.time_dict[saeId]
       lv = self.value_dict[saeId]
       result_index = 0;
       self.result_t.append(lt[0])
       self.result_v.append(lv[0])

       for i in range(1, len(lt)):
         current_time = lt[i]
         if current_time == self.result_t[result_index]:
            self.result_v[result_index] = self.result_v[result_index] + lv[i]
         elif current_time == self.result_t[result_index]+1:
            self.result_t.append(current_time)
            self.result_v.append(lv[i])
            result_index = result_index + 1
         elif current_time > self.result_t[result_index]+1:
            while(self.result_t[result_index]+1 < current_time):
               self.result_t.append(self.result_t[result_index]+1)
               self.result_v.append(0)
               result_index = result_index + 1
            self.result_t.append(current_time)
            self.result_v.append(lv[i])
            result_index = result_index + 1


   def display_result(self, xscale, yscale):
      time_array = []
      byte_array = []

      for i in range(len(self.result_t)):
         if i % xscale == 0:
            time_array.append(self.result_t[i])
            byte_array.append(self.result_v[i])
         else:
            byte_array[i/xscale] += self.result_v[i]

      x_array = map(lambda x:x-time_array[0], time_array)

      if yscale == 'Mbps':
         y_array = map(lambda x:x*8*1000/1024/1024/xscale, byte_array)
         plt.ylabel('throughput(Mbps)')
         plt.ylim([0,450])
      elif yscale == 'Kbps':
         y_array = map(lambda x:x*8*1000/1024/xscale, byte_array)
         plt.ylabel('throughput(Kbps)')
      else:
         y_array = map(lambda x:x*8*1000/xscale, byte_array)
         plt.ylabel('throughput(bps)')

      for i in range(len(x_array)):
         print x_array[i], y_array[i]

      plt.plot(x_array,y_array,linewidth=1.0)
      plt.xlabel('time(millisecond)')
      plt.grid(True)
      plt.xlim(0)

      plt.show()



parser = argparse.ArgumentParser(description='Process HLC log and plot throughput over time')
parser.add_argument('file', metavar='file', nargs='?', help='file path and name, for example: .\hlc.log')
parser.add_argument('-t', '--time', type=int, default=5, help='time scale (millisecond) for X-axis, default is 5')
parser.add_argument('-p', '--throughput', default='Mbps', choices=['Mbps', 'Kbps', 'bps'], help='throughput scale for Y-axis, default is Mbps')

args = parser.parse_args()

if args.time <= 0:
   print "time must be positive integer"
   exit(0)

a = ParseLog(args.file)

a.parseFile()
sel = a.getSaeFromUser()
a.parseResult(sel)
a.display_result(args.time, args.throughput)

