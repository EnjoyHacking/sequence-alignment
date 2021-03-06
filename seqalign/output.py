
"""
Consensus module
Generate consensus based on multiple sequence alignment

Written by Marshall Beddoe <mbeddoe@baselineresearch.net>
Copyright (c) 2004 Baseline Research

Licensed under the LGPL
"""

from curses.ascii import *
import math

class Output:

    def __init__(self, sequences):

        self.sequences = sequences
        self.consensus = []
	self.signatures = []  # raw 
	self.signatureshex = []  # encoded with hex
	#self.real = [] 
	#self.real_gapped = [] 
	self.histogram = {}
        self._go()

    def _go(self):
        pass

class Ansi(Output):

    def __init__(self, sequences):

        # Color defaults for composition
        self.gap = "\033[41;30m%s\033[0m"
        self.printable = "\033[42;30m%s\033[0m"
        self.space = "\033[43;30m%s\033[0m"
        self.binary = "\033[44;30m%s\033[0m"
        self.zero = "\033[45;30m%s\033[0m"
        self.bit = "\033[46;30m%s\033[0m"
        self.default = "\033[47;30m%s\033[0m"

        Output.__init__(self, sequences)

    def _go(self):

        seqLength = len(self.sequences[0][1])
        rounds = seqLength / 18
        remainder = seqLength % 18
        l = len(self.sequences[0][1])

        start = 0
        end = 18
	# datatype 
        dtConsensus = []
	# mutation 
        mtConsensus = []

        for i in range(rounds):
            for id, seq in self.sequences:
                print "%04d" % id,
                for byte in seq[start:end]:
                    if byte == 256:
                        print self.gap % "___",
                    elif isspace(byte):
                        print self.space % "   ",
                    elif isprint(byte):
                        print self.printable % "x%02x" % byte,
                    elif byte == 0:
                        print self.zero % "x00",
                    else:
                        print self.default % "x%02x" % byte,
                print ""

            # Calculate datatype consensus

            print "DT  ",
            for j in range(start, end):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                dt = self._dtConsensus(column)
                print dt,
                dtConsensus.append(dt)
            print ""

            print "MT  ",
            for j in range(start, end):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                rate = self._mutationRate(column)
                print "%03d" % (rate * 100),
                mtConsensus.append(rate)
            print "\n"

            start += 18
            end += 18

        if remainder:
            for id, seq in self.sequences:
                print "%04d" % id,
                for byte in seq[start:start + remainder]:
                    if byte == 256:
                        print self.gap % "___",
                    elif isspace(byte):
                        print self.space % "   ",
                    elif isprint(byte):
                        print self.printable % "x%02x" % byte,
                    elif byte == 0:
                        print self.zero % "x00",
                    else:
                        print self.default % "x%02x" % byte,
                print ""

            print "DT  ",
            for j in range(start, start + remainder):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                dt = self._dtConsensus(column)
                print dt,
                dtConsensus.append(dt)
            print ""

            print "MT  ",
            for j in range(start, start + remainder):
                column = []
                for id, seq in self.sequences:
                    column.append(seq[j])
                rate = self._mutationRate(column)
                mtConsensus.append(rate)
                print "%03d" % (rate * 100),
            print ""

        # Calculate consensus sequence
        l = len(self.sequences[0][1])

        for i in range(l):
            histogram = {}
            for id, seq in self.sequences:
                try:
                    histogram[seq[i]] += 1
                except:
                    histogram[seq[i]] = 1

            items = histogram.items()
            items.sort()
	    self.histogram = histogram

            #m = 1
            m = math.ceil(len(self.sequences) / 2)
            v = 257
	    if len(histogram) < 5:
		    for j in items:
			if j[1] > m:
			    m = j[1]
			    v = j[0]

            self.consensus.append(v)

            real = []
	    real_gapped = []

            for i in range(len(self.consensus)):
                if self.consensus[i] == 256:
                    real_gapped.append((self.consensus[i], dtConsensus[i], mtConsensus[i]))
                    continue
                real.append((self.consensus[i], dtConsensus[i], mtConsensus[i]))
                real_gapped.append((self.consensus[i], dtConsensus[i], mtConsensus[i]))
            #self.real = real
            #self.real_gapped = real_gapped

        #
        # Display consensus data
        #
        totalLen = len(real)
        rounds = totalLen / 18
        remainder = totalLen % 18

        start = 0
        end = 18

        print "\nUngapped Consensus:"

        for i in range(rounds):
            print "CONS",
            for byte,type,rate in real[start:end]:
                if byte == 256:
                   print self.gap % "___",
                elif byte == 257:
                    print self.default % "???",
                elif isspace(byte):
                    print self.space % "   ",
                elif isprint(byte):
                    print self.printable % "x%02x" % byte,
                elif byte == 0:
                    print self.zero % "x00",
                else:
                    print self.default % "x%02x" % byte,
            print ""

            print "DT  ",
            for byte,type,rate in real[start:end]:
                print type,
            print ""

            print "MT  ",
            for byte,type,rate in real[start:end]:
                print "%03d" % (rate * 100),
            print "\n"

            start += 18
            end += 18

        if remainder:
            print "CONS",
            for byte,type,rate in real[start:start + remainder]:
                if byte == 256:
                   print self.gap % "___",
                elif byte == 257:
                    print self.default % "???",
                elif isspace(byte):
                    print self.space % "   ",
                elif isprint(byte):
                    print self.printable % "x%02x" % byte,
                elif byte == 0:
                    print self.zero % "x00",
                else:
                    print self.default % "x%02x" % byte,
            print ""

            print "DT  ",
            for byte,type,rate in real[start:end]:
                print type,
            print ""

            print "MT  ",
            for byte,type,rate in real[start:end]:
                print "%03d" % (rate * 100),
            print ""

        #
        # Display consensus data with gapped
        #
        totalLen = len(real_gapped)
        rounds = totalLen / 18
        remainder = totalLen % 18

        start = 0
        end = 18

        print "\nGapped Consensus:"

        for i in range(rounds):
            print "CONS",
            for byte,type,rate in real_gapped[start:end]:
                if byte == 256:
                   print self.gap % "___",
                elif byte == 257:
                    print self.default % "???",
                elif isspace(byte):
                    print self.space % "   ",
                elif isprint(byte):
                    print self.printable % "x%02x" % byte,
                elif byte == 0:
                    print self.zero % "x00",
                else:
                    print self.default % "x%02x" % byte,
            print ""

            print "DT  ",
            for byte,type,rate in real_gapped[start:end]:
                print type,
            print ""

            print "MT  ",
            for byte,type,rate in real_gapped[start:end]:
                print "%03d" % (rate * 100),
            print "\n"

            start += 18
            end += 18

        if remainder:
            print "CONS",
            for byte,type,rate in real_gapped[start:start + remainder]:
                if byte == 256:
                   print self.gap % "___",
                elif byte == 257:
                    print self.default % "???",
                elif isspace(byte):
                    print self.space % "   ",
                elif isprint(byte):
                    print self.printable % "x%02x" % byte,
                elif byte == 0:
                    print self.zero % "x00",
                else:
                    print self.default % "x%02x" % byte,
            print ""

            print "DT  ",
            for byte,type,rate in real_gapped[start:end]:
                print type,
            print ""

            print "MT  ",
            for byte,type,rate in real_gapped[start:end]:
                print "%03d" % (rate * 100),
            print ""

	self._extractSignatures()
	# Calculate datatype consensus
	# G: Gap (256)
	# S: Space (\x20)
	# A: Ascii 
	# Z: Zero  (\x00)
	# B: Binary
    def _dtConsensus(self, data):
        histogram = {}

        for byte in data:
            if byte == 256:
                try:
                    histogram["G"] += 1
                except:
                    histogram["G"] = 1
            elif isspace(byte):
                try:
                    histogram["S"] += 1
                except:
                    histogram["S"] = 1
            elif isprint(byte):
                try:
                    histogram["A"] += 1
                except:
                    histogram["A"] = 1
            elif byte == 0:
                try:
                    histogram["Z"] += 1
                except:
                    histogram["Z"] = 1
            else:
                try:
                    histogram["B"] += 1
                except:
                    histogram["B"] = 1

        items = histogram.items()
        items.sort()

        m = 1
        v = '?'
        for j in items:
           if j[1] > m:
               m = j[1]
               v = j[0]

        return v * 3

	# Calculate mutation rate
    def _mutationRate(self, data):

        histogram = {}

        for x in data:
            try:
                histogram[x] += 1
            except:
                histogram[x] = 1

        items = histogram.items()
        items.sort()

        if len(items) == 1:
            rate = 0.0
        else:
            rate = len(items) * 1.0 / len(data) * 1.0

        return rate

    def _extractSignaturesHex(self):
    	flag = 1
	substring = "" 
    	for i in range(len(self.consensus)):
		if self.consensus[i] == 256:
			if flag == 1 :
				if "" != substring:
					self.signatureshex.append(substring)
					substring = ""
				flag = 0
		elif self.consensus[i] == ord('\r'):
			strcr = "x%02x" % self.consensus[i] 
			substring += strcr 
			flag = 1
		elif self.consensus[i] == ord('\n'):
			strlf = "x%02x" % self.consensus[i] 
			substring += strlf 
			flag = 1
		elif self.consensus[i] == ord(' '):
			strspace = "x%02x" % self.consensus[i] 
			substring += strspace 
			flag = 1
		elif self.consensus[i] >=0 and self.consensus[i] < 256:
			substring += str(chr(self.consensus[i])) 
			flag = 1
		else:
			strhex = "x%02x" % self.consensus[i] 
			substring += strhex 
			flag = 1
			
	#print self.signatureshex

    def _extractSignatures(self):
    	flag = 1
	substring = "" 
    	for i in range(len(self.consensus)):
		print self.consensus[i],
		print ", ",
		if self.consensus[i] == 256 or self.consensus[i] == 257:
			if flag == 1 :
				if "" != substring:
					self.signatures.append(substring)
					substring = ""
				flag = 0
		else:
			substring += str(chr(self.consensus[i])) 
			flag = 1
	print self.signatures

    def getSignatures(self):
    	return self.signatures

		
