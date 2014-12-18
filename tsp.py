#!/usr/bin/python

import signal, getopt, sys, math

# usage: python ./tsp.py -f [inputfilename]

class Point:
    """ Point is an x and y integer with manipulations"""

    #constructor
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    #string return for printing
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    #calculates distance from this point to another
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        #calculate floating point distance
        dist = math.sqrt(dx**2 + dy**2)
        #round to nearest whole number
        dist = round(dist)
        #covert to int
        dist = int(dist)
        return dist

def usage():
    print "To use: python ./tsp.py -f [inputfilename]\n"

def findMinDist(pointIn, setIn):
    allDists = []
    returnDist = []
    #point in is last point popped
    #setIn is the set of remaining points (cities)
    #(that have not yet been popped/visited)
    for point in setIn:
        #inArr will end up [cityName, distance from pointIn as float]
        inArr = []
        inArr.append(point[0])
        inArr.append(point[1].distance(pointIn))
        #then allDists will be an array of all inArrs
        #[[cityName, distance],[cityName, distance]...]
        allDists.append(inArr)  
    #THERE MIGHT BE BETTER WAYS TO INITIALIZE BOTH OF THESE   
    #initialize minDist to first distance for comparison 
    minDist = allDists[0][1]
    #initialize returnDist to [0, alldists[0]]
    #0 might already be the smallest distance
    returnDist = [0, allDists[0]]
    #compare all distances to the minDist
    #if smaller, set minDist to smaller dist and record to minDist
    for idx, dist in enumerate(allDists):
        if dist[1] < minDist:
            minDist = dist[1]
            #BUG MIGHT BE HERE: idx should be the index of the smallest distance!!
            returnDist = idx, dist
    #returnDist should be the smallest
    ##SEE point below where we left off -------->
    return returnDist

# The signal handler. On receiving sigterm, it writes
# the latest result to the file.
def sig_term(num, frame):
    global DIST, setU, fp
    ps = open('partial_solution.txt', 'wb')
    ps.write(str(DIST) + '\n')

    for node in setU:
        ps.write(str(node[0])+ '\n')

    fp.close()
    ps.close()

def main():

    signal.signal(signal.SIGTERM, sig_term)

    global DIST, setU, fp

    #global file in
    fileIn = ""

    #getopts.  To change useage info, modify useage() above
    #check for empty input
    if(len(sys.argv) == 1):
        usage()
        sys.exit(2)
    #check for improper input
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        # "-f" is only valid option to enter filename
        if o in ("-f"):
            fileIn = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    if (fileIn != ""):
        fp = open(fileIn, "r")
        #read entire file into fileBuf
        fileBuf = fp.read()
        
        splitArr = fileBuf.strip().split()
        #numArr is a list of three-tuples 
        numArr = zip(*[iter(splitArr)]*3)
        
        DIST = 0
        #start set
        setV = []
        #result set
        setU = []
        
        #transform into array of ordered points [[0, point0], [1, point1], ...] 
        while numArr:
            inArr = []
            popped = numArr.pop(0)
            point = Point(int(popped[1]), int(popped[2]))
            inArr.append(int(popped[0]))
            inArr.append(point)
            setV.append(inArr)

#________

        #START HERE
        POINT_ONE = setV[0][1]
        #do while loop
        #do
        point = setV.pop(0)
        #algo ALWAYS begins from point 0, so point 0 
        #is always first point in the tour result, setU[]
        setU.append(point)
        #point[1] is the point object associated with the city 0 
        #SEE findMinDist -----> above
        minDist = findMinDist(point[1], setV)
        #now we pop the city at index minDist[0] or the idx returned from above
        #this is our next city
        minPoint = setV.pop(minDist[0])
        #and we add the distance between them to the total.
        DIST += minDist[1][1]
        #finally we move the point into our result array, setU[]
        setU.append(minPoint) 
        #and we do it all over again starting from minPoint
        #until there're no more towns left to visit.
        while setV:
            #(same sequence as above)
            point = minPoint
            minDist = findMinDist(point[1], setV)
            minPoint = setV.pop(minDist[0])
            DIST += minDist[1][1]
            setU.append(minPoint) 
        #complete tour from point n to point 0
        POINT_END = setU[len(setU)-1][1]
        end_dist = POINT_ONE.distance(POINT_END)
        DIST += end_dist



        fileOut = fileIn + ".tour"
        fo = open(fileOut, "wb")
        fo.write(str(DIST) + '\n')

        for node in setU:
            fo.write(str(node[0])+ '\n')

        #close fileIn, fileOut
        fp.close()
        fo.close()

if __name__ == "__main__":
    main()