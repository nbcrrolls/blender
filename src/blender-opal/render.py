#! /usr/bin/env python

import os
import sys
import string
import getopt
import types
import UserDict
import re
from pprint import pprint
import zipfile
import gzip

class Struct:
    """ base structure """
    pass

class Blender:
    """ Base class """
    def __init__(self, argv):
        self.args = argv[1:]
        self.usageName  = os.path.basename(argv[0])

        self.setDefaults()
        self.parseArgs()
        self.checkArgs()

    def setDefaults(self):
        """ set default class attributes """
        self.setDefaultOpts()

        self.input      = None       # input file name
        self.start      = None       # input start frame
        self.end        = None       # input end frame
        self.outframe   = None       # input prefix to use for output frames
        self.sgesub     = "sge.sub"  # SGE submit script 
        self.format     = None       # input file format 
        self.fname      = None       # base name of input file (without compression sufffix if any)

    def setDefaultOpts(self):
        """ set default command line options """
        self.getopt = Struct()
        self.getopt.s = ['h']
        self.getopt.l = ['help']

        self.getopt.s.extend([('f:', 'file'),
                              ('o:', 'oframe'),
                              ('s:', 'start'),
                              ('e:', 'end')
                              ])
        self.getopt.l.extend([('file=', 'file'),
                              ('oframe=', 'oframe'),
                              ('start=', 'start'),
                              ('end=', 'end')
                              ])

    def parseArg(self, c):
        """ parse single command line argument """
        if c[0] in ('-h', '--help'):
            self.help()
        elif c[0] in ('-f', '--file'):
            self.input = c[1]
        elif c[0] in ('-o', '--oframe'):
            self.outframe = c[1]
        elif c[0] in ('-s', '--start'):
            self.start = c[1]
        elif c[0] in ('-e', '--end'):
            self.end = c[1]
        else:
            return 0

        return 1

    def parseArgs(self):
        """ parse command line arguments """
        short = ''
        for e in self.getopt.s:
            if type(e) == types.TupleType:
                short = short + e[0]
            else:
                short = short + e

        long = []
        for e in self.getopt.l:
            if type(e) == types.TupleType:
                long.append(e[0])
            else:
                long.append(e)
        try:
            opts, args = getopt.getopt(self.args, short, long)
        except getopt.error:
            self.help()

        for c in opts:
            self.parseArg(c)
        self.args = args


    def checkArgs(self):
        """ check correctness of command line arguments """
        missing = 0;
        self.msg = "ERROR in input:\n"
        if self.input == None: 
            self.msg += ('\tmissing input file \n')
            missing += 1
        if self.start == None:  
            self.msg += ('\tmissing start frame (int) \n')
            missing += 1
        if self.end == None:  
            self.msg += ('\tmissing end frame (int) \n')
            missing += 1
        if self.outframe == None:  
            self.msg += ('\tmissing output frame name porefix \n')
            missing += 1
        if missing:
            self.inputErrExit()

        self.msg = ""


    def checkZipFile(self):
        """ check zip file contents list """
        if zipfile.is_zipfile(self.input) == True :
            zf = zipfile.ZipFile(self.input, 'r')
            self.fname =  zf.namelist()[0]
            self.format = "zip"
            zf.close()
        else:
            self.msg += "\tCompressed file %s is not in zip format." % self.input
            self.inputErrExit()

    def checkGzipFile(self):
        """ check gzip file contents list """
        f = os.popen('gunzip -t %s' % (self.input), 'r')
        info = f.read()
        f.close()
        if len(info):
            self.msg += "\tCompressed file %s is not in gzip format." % self.input
            self.inputErrExit()
        else:
            self.format = "gzip"

        f = os.popen('gunzip -l %s | tail -1' % (self.input), 'r')
        info = f.read()
        f.close()
        self.fname = info.split()[-1]


    def checkInputFile(self):
        """ Checks if file is zip or gzip type and checks its content names """
        f = os.popen('file -bi %s' % self.input, 'r')
        info = f.read()
        f.close()
        print info

        # check input file format
        if  string.find (info, 'gzip') > -1:
                self.checkGzipFile()
        elif string.find (info, 'zip') > -1:
                self.checkZipFile()
        elif string.find (info, 'cannot open') > -1:
            self.msg = info
            self.inputErrExit()
        elif string.find (info, 'ERROR') > -1:
            self.msg = info
            self.inputErrExit()
        else:
            self.format = None 
            self.fname = self.input 

        # uncompresss archive
        if self.format:
            self.uncompressInputFile()

    def uncompressInputFile(self):
        """ uncompress input file """
        if self.format == "zip":
                f = os.popen('unzip %s' % (self.input), 'r')
                info = f.read()
                f.close()
        elif self.format == "gzip":
                f = os.popen('gunzip  %s' % (self.input), 'r')
                info = f.read()
                f.close()
        else :
            self.msg += "Wrong file format %s." % self.input
            self.inputErrExit()

        if not os.path.isfile(self.fname) :
            self.msg += "Could not uncompress file %s.  Decompression results in error:\n%s" % (self.input, info)
            self.inputErrExit()


    def writeFile(self, fname, lines):
        """ writes verified input lines in a new file that will be passed to SGE """
        f = open(fname, 'w')
        f.write(lines)
        f.close()

    def inputErrExit(self):
        """ prints input related error and exits """
        print (self.msg)
        self.help()
        sys.exit(0)

    def help(self):
        """ print usage """
        print '\nNAME: \n' , \
              '\t%s - batch rendering of frames.\n' % self.usageName, \
              '\nSYNOPSIS:\n' , \
              '\t%s -f FILE -s NUM [-h|help]\n' % self.usageName, \
              '\nDESCRIPTION:\n' , \
              '    -f|--file FILE       - input blender file. Example : blender-frame.blend \n', \
              '    -o|--oframe NAME     - string to use as a prefix for output frames. Examle: target-scene. Default is "frame" \n', \
              '    -s|--start NUM       - integer NUM to specify start frame. Examle: 10. Default is 1 \n', \
              '    -e|--end NUM         - integer NUM to specify end frame. Examle: 20. Default is 5 \n', \
              '    -h|--help            - prints usage\n', \
        sys.exit(0)

    def checkFrameNumber(self):
        """ check numbers for start and end frame"""
        err = 0

        try:
            self.start = int(self.start)
        except:
            err = 1
            self.msg += "ERROR: input value for start frame is not an integer: %s " % self.start

        try:
            self.end = int(self.end)
        except:
            err = 1
            self.msg += "ERROR: input value for end frame is not an integer: %s " % self.end

        if err:
            self.inputErrExit()

        # sheck start and end values 
	if self.start < 1:
            self.msg += "WARNING: resetting start frame to 1 from %s " % self.start
            self.start = 1
	if self.end <= self.start:
            self.msg += "WARNING: resetting end frame to %d+1 from %s " % (self.start, self.end)
            self.end = self.start + 1

        # number of tasks for SGE array job
        self.tasks = self.end - self.start + 1

        # number to add to  SGE task id if start frame is not 1
        self.skip = self.start - 1

    def checkFrameName(self):
        NAME_MAX=20                          # allowed filename length
        length = len(self.outframe)
        if length >=NAME_MAX:
            newname = self.outframe[:20]
            print "WARNING:\t '%s' is too long, using '%s' " % (self.outframe, newname)
            self.outframe = newname

    def checkValidFileName(self, name, num):
        """ check output file name validity """
        NAME_MAX=50                          # allowed filename length
        defname = "img%d.png" % num          # default name made from line number

        strip_name = os.path.basename(name)  # strip / and . from the front
        length = len(strip_name)

        if length < 5 :
            print "WARNING:\t '%s' is too short, using '%s' " % (name, defname)
            return defname
        if length >=NAME_MAX :
            print "WARNING:\t '%s' is too long, using '%s' " % (name, defname)
            return defname

        valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
        valid_name = ''.join(c for c in strip_name if c in valid_chars)

        if strip_name != valid_name:
            print "WARNING:\t '%s' filename contains invalid characters, using '%s' " % (name, defname)
            return defname

        return valid_name

    def writeSubmitScript(self):
        """ create SGE submit script """
        subtxt  = "#!/bin/bash\n"
        subtxt += "#$ -cwd\n"
        subtxt += "#$ -S /bin/bash\n"
        subtxt += "#$ -N render\n"
        subtxt += "#$ -o render.$TASK_ID.out\n"
        subtxt += "#$ -e render.$TASK_ID.err\n"
        subtxt += "#$ -t 1-%d\n\n" % self.tasks
        subtxt += 'let FRAME=$SGE_TASK_ID+%d\n' % self.skip
        subtxt += "input=%s\n\n" % self.fname 
        subtxt += "/opt/blender/blender -b $input -t 1 -x 1 -o output//%s -s $FRAME -e $FRAME -a\n\n" % self.outframe

        self.writeFile(self.sgesub, subtxt)

    def runSGEjob(self):
        command = "qsub -sync y %s" % self.sgesub
        os.system(command)

    def postSGEjob(self):
        os.system("tail -n +1 *.err > render-err; rm -rf *.err")
        os.system("tail -n +1 *.out > render-out; rm -rf *.out")
        os.system("tar czf output-frames.tar.gz output/; rm -rf output/")

    def run(self):
        """ main function """
        self.checkFrameNumber()
        self.checkFrameName()
        self.checkInputFile()
        self.writeSubmitScript()
        self.runSGEjob()
        self.postSGEjob()

        print self.msg
        sys.exit(0);

    def test(self):
        """ test """
        pprint (self.__dict__)

if __name__ == "__main__":
        app=Blender(sys.argv)
        app.run()

