import pdb
import logging
import subprocess
import urllib
import argparse

logger_name = "log"
chrome = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
entry_url = "http://ukrav/results/history_plot.php?table=lte_3gpp_fdd_platc_cue&branch=ALL&var=ALL&tnum="

class pageParse:
   def __init__(self, log, openChrome=False, n=1, base="NULL", mode = "all"):
      self.label = []
      self.branch = []
      self.build = []
      self.run_setup = []
      self.link = []
      self.n = n
      self.openChrome = openChrome
      self.logger = log
      self.base = base
      self.case =""
      self.baseResult = "PASS"
      self.mode = mode

      self.parse = {
         0:self.parse_line_step_0,
         1:self.parse_line_step_1,
         2:self.parse_line_step_2,
         3:self.parse_line_step_3,
         4:self.parse_line_step_4,
         5:self.parse_line_step_5,
         6:self.parse_line_step_6,
         7:self.parse_line_step_7,
         8:self.parse_line_step_8,
         9:self.parse_line_step_9
      }

   def __enter__(self):
      return self

   def __exit__(self, exc_type, exc_val, exc_tb):
      self.logger.debug("exit case "+ self.case)
      return False

   def check_case(self, case):
      self.logger.debug("check case "+ case)
      self.case = case
      self.entry = entry_url + case
      if self.openChrome:
         self.logger.debug(chrome + " " + self.entry)
         subprocess.call([chrome, self.entry])

      if(self.base == "NULL"):
         self.parse_entry_page()
      else:
         self.parse_entry_page_find_base()

   def dump_info(self):
      self.logger.debug("dump info start")
      for i in range(len(self.label)):
         self.logger.debug("label: "+self.label[i])
         self.logger.debug("branch: "+self.branch[i])
         self.logger.debug("build: "+self.build[i])
         self.logger.debug("run setup: "+self.run_setup[i])
         self.logger.debug("link: "+self.link[i])
         self.logger.debug("\n")
      self.logger.debug("dump info end")

   def print_fail_link_info(self, link):
      response = urllib.urlopen(link)
      data = response.read()
      index_start = data.find("The Test: FAIL")
      if index_start < 0:
         index_start = data.find("The Test: CRASH")
      if index_start < 0:
         index_start = data.find("The Test: PASS")
      if index_start < 0:
         index_start = data.find("The Test: FATAL")
      if index_start < 0:
         index_start = data.find("The Test: MISSING_RESOURCE")
      assert index_start >0, data
      context = data[index_start:]
      index_end = context.find("</td>")
      l = context[:index_end]
      ll = l.replace("<br>","\n")
      self.logger.info(ll)
      print ll+"\n"

   def print_lastest_n_fails(self, n):
      if n <= len(self.link):
         j = n
      else:
         j = len(self.link)

      for i in range(j):
         print "label: "+self.label[i]
         self.logger.info("label: "+self.label[i])
         print "branch: "+self.branch[i]
         self.logger.info("branch: "+self.branch[i])
         print "build: "+self.build[i]
         self.logger.info("build: "+self.build[i])
         print "run setup: "+self.run_setup[i]
         self.logger.info("run setup: "+self.run_setup[i])
         print "link: "+self.link[i]
         self.logger.info("link: "+self.link[i])

         self.print_fail_link_info(self.link[i])

         if self.openChrome:
            subprocess.call([chrome, self.link[i]])

   def parse_line(self, l, step):
      self.logger.debug(l)
      self.parse[step](l)

   def parse_line_step_0(self, l):
      if l.find("CRASH") > 0:
         headStr = "<td><span class=\"CRASH\">"
      elif l.find("FAIL") > 0:
         headStr = "<td><span class=\"FAIL\">"
      elif l.find("FATAL") > 0:
         headStr = "<td><span class=\"FATAL\">"
      elif l.find("MISSING_RESOURCE") > 0:
         headStr = "<td><span class=\"MISSING_RESOURCE\">"
      else:
         assert l.find("PASS") > 0, l
         headStr = "<td><span class=\"PASS\">"
      i_start = l.find(headStr)
      i_end = l.find("</span></td>")
      tmp = l[i_start+len(headStr):i_end]
      self.logger.debug(tmp)
      self.label.append(tmp)

   def parse_line_step_1(self, l):
      i_start = l.find(", 1, '")
      i_end = l.find("');")
      tmp = l[i_start+len(", 1, '"):i_end]
      self.logger.debug(tmp)
      self.branch.append(tmp)

   def parse_line_step_2(self, l):
      i_start = l.find(", 2, '")
      i_end = l.find("');")
      tmp = l[i_start+len(", 2, '"):i_end]
      self.logger.debug(tmp)
      self.build.append(tmp)

   def parse_line_step_3(self, l):
      pass
   def parse_line_step_4(self, l):
      pass
   def parse_line_step_5(self, l):
      pass

   def parse_line_step_6(self, l):
      i_start = l.find(", 6, '")
      i_end = l.find("');")
      tmp = l[i_start+len(", 6, '"):i_end]
      self.logger.debug(tmp)
      self.run_setup.append(tmp)

   def parse_line_step_7(self, l):
      pass
   def parse_line_step_8(self, l):
      i_start = l.find("<td><span><a href = ")
      i_end = l.find(">Detail Result logs")
      tmp = l[i_start+len("<td><span><a href = "):i_end]
      tmp = "http://ukrav/results/" + tmp
      self.logger.debug(tmp)
      self.link.append(tmp)

   def parse_line_step_9(self, l):
      pass

   def parse_entry_page(self):
      response = urllib.urlopen(self.entry)
      data = response.read()
      context = data
      step = 10

      while(True):
         index = context.find("\n")
         if(index < 0):
            break
         l = context[0:index]
         context = context[index+1:]
         if l.find(", 0, '<td><span class=\"") > 0:
            if self.mode == "fail" and l.find("PASS") > 0:
               continue
            else:
               step = 0
         if step < 10:
            if l.find(", 7, '<td><span class=\"") > 0:
               #pdb.set_trace()
               assert step == 7

            self.parse_line(l, step)
            step += 1

      self.dump_info()
      self.print_lastest_n_fails(self.n)

   def parse_entry_page_find_base(self):
      response = urllib.urlopen(self.entry)
      data = response.read()
      context = data
      step = 10

      while(True):
         index = context.find("\n")
         if(index < 0):
            break
         l = context[0:index]
         context = context[index+1:]
         if l.find(self.base) > 0:
            step = 0;
         if step < 10:
            self.parse_line(l, step)
            step += 1

      self.dump_info()
      self.print_lastest_n_fails(self.n)

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

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='fetch LTE CUE test case result from UK RAV')
   parser.add_argument('printResult', default='all', choices=['all', 'fail'], help='print only fail results or all results, meanless if -b is specified')
   parser.add_argument('-n', type=int, default=1, help='print latest n result, default is 1')
   parser.add_argument('-c', '--chrome', default='n', choices=['y', 'n'], help='open all links with chrome')
   parser.add_argument('-l', '--logging', default='INFO', choices=['INFO', 'DEBUG'], help='log level to set. Default is INFO')
   parser.add_argument('-b', '--build', nargs='?', default='NULL', help='specify the BUILD to fetch the result, for example: LTE-CUE-LS2_L1_15_12_14_20_24_13')


   args = parser.parse_args()
   if args.logging == "DEBUG":
      loggingLevel = logging.DEBUG
   else:
      loggingLevel = logging.INFO
   logger = set_logging(loggingLevel)

   while(True):
      test_number = raw_input("test case number(type q to quit):")
      if RepresentsInt(test_number):
         with pageParse(log = logger, openChrome=(args.chrome == 'y'), n=args.n, base=args.build, mode=args.printResult) as web_parser:
            web_parser.check_case(test_number)
      else:
         if test_number == "q" or test_number == "quit":
            break
         else:
            print "wrong case number"
