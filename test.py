import sys, os
def test(arg1, arg2):
 print "begin test..."
 fun1('1', '2')
 print arg1
 print arg2
def fun1(arg1, arg2):
         print arg1
         print arg2
   
if __name__ == '__main__':
    test(*sys.argv[1:])
