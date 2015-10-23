#!/usr/bin/python -u


from seqalign import *
import sys, getopt
import multiprocessing




def main(argv, no, totalSignatures):

    # Defaults
    format = None
    weight = 1.0
    graph = False
    print "main %d ..." % no

    #
    # Parse command line options and do sanity checking on arguments
    #
    try:
        (opts, args) = getopt.getopt(argv[1:], "pahgw:")
	#print "args: %d" % args
	#print "argv: %s" % argv
    except:
        usage()

    for o,a in opts:
        if o in ["-p"]:
            format = "pcap"
        elif o in ["-a"]:
            format = "ascii"
        elif o in ["-h"]:
            format = "hex"
        elif o in ["-w"]:
            weight = float(a)
        elif o in ["-g"]:
            graph = True
        else:
            usage()

    if len(args) == 0:
        usage()

    if weight < 0.0 or weight > 1.0:
        print "FATAL: Weight must be between 0 and 1"
        sys.exit(-1)

    clusterFile = "cluster_" + str(no) + ".txt"
    base = argv[len(argv) - 1]
    if base.rindex("/") == len(base) - 1:
    	file = argv[len(argv) - 1] + clusterFile
    else:
    	file = argv[len(argv) - 1] + "/" + clusterFile


    try:
        file
    except:
        usage()

    #
    # Open file and get sequences
    #
    if format == "pcap":
        try:
            sequences = input.Pcap(file)
        except:
            print "FATAL: Error opening '%s'" % file
            sys.exit(-1)
    elif format == "ascii":
        try:
            sequences = input.ASCII(file)
        except:
            print "FATAL: Error opening '%s'" % file
            sys.exit(-1)
    elif format == "hex":
        try:
            sequences = input.HEX(file)
        except:
            print "FATAL: Error opening '%s'" % file
            sys.exit(-1)
    else:
        print "FATAL: Specify file format"
        sys.exit(-1)

    if len(sequences) == 0:
        print "FATAL: No sequences found in '%s'" % file
        sys.exit(-1)
    else:
        print "Found %d unique sequences in '%s'" % (len(sequences), file)


    #
    # Create distance matrix (LocalAlignment, PairwiseIdentity, Entropic)
    #
    print "Creating distance matrix ..",
    dmx = distance.LocalAlignment(sequences)
    print "complete"

    #
    # Pass distance matrix to phylogenetic creation function
    #
    print "Creating phylogenetic tree ..",
    phylo = phylogeny.UPGMA(sequences, dmx, minval=weight)
    print "complete"

    #
    # Output some pretty graphs of each cluster
    #
    if graph:
        cnum = 1
        for cluster in phylo:
            out = "graph-%d" % cnum
            print "Creating %s .." % out,
            cluster.graph(out)
            print "complete"
            cnum += 1

    print "\nDiscovered %d clusters using a weight of %.02f" % \
        (len(phylo), weight)

    #
    # Perform progressive multiple alignment against clusters
    #
    i = 1
    alist = []
    for cluster in phylo:
        print "Performing multiple alignment on cluster %d .." % i,
        aligned = multialign.NeedlemanWunsch(cluster)
        print "complete"
        alist.append(aligned)
        i += 1
    print ""

    #
    # Display each cluster of aligned sequences
    #
    localSignatures = [] # Store the extracted substrings from the result of alignment
    i = 1
    for seqs in alist:
        print "Output of cluster %d" % i
        align = output.Ansi(seqs)
	print "No.%d: " % i,
	print align.getSignatures()
	localSignatures.extend(align.getSignatures())
        i += 1
        print ""
    #
    # Save the extracted signatures to file
    print localSignatures
    totalSignatures.extend(localSignatures)
    """
    print signatures
    path = file[0 : file.rindex("/") + 1]
    no = file[file.rindex("_") + 1 : file.rindex(".txt")]
    filename = path + "signature_" + no + ".txt"
    fsig = open(filename, "a")
    for element in signatures:
    	for i in element:
		fsig.write(i)
		fsig.write("\n")
    fsig.close()
    """


def usage():
    print "usage: %s [-gpah] [-w <weight>] <sequence file>" % \
        sys.argv[0]
    print "       -g\toutput graphviz of phylogenetic trees"
    print "       -p\tpcap format"
    print "       -a\tascii format"
    print "       -h\thex format"
    print "       -w\tdifference weight for clustering"
    sys.exit(-1)


# Filter by the constrain of substring len 
def refineByLen(e):
	return len(e) > 1 and len(e) <= 20


def removeNonDistinct(l):
	siglist = [] 
	for i in xrange(len(l)):
		for j in xrange(len(l)):
			if i == j:
				continue	
			else:
				if l[j].find(l[i]) == True:
					break	
				else:
					siglist.append(l[i])
	return siglist




if __name__ == "__main__":

    totalSignatures = multiprocessing.Manager().list() 
    pool = multiprocessing.Pool(processes = 3)
    for i in xrange(3) :
    	pool.apply(main, (sys.argv, i, totalSignatures))
    pool.close()
    pool.join()
    print "Total Signatures:"
    print totalSignatures
    print "Total Signatures (By len):"
    print filter(refineByLen, totalSignatures)
    candiate_substrings =  filter(refineByLen, totalSignatures)
    sigset = set(removeNonDistinct(candiate_substrings))
    print "sigset:"
    print sigset


    """
    print "Set Signatures:"
    print sigSet
    print "list : %d " % len(totalSignatures)
    print "set : %d " % len(sigSet)
    """
    print "All sub-processes done!"
    sys.exit(0)

