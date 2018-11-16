import matplotlib.pyplot as plt 
import sys

def GetData():
    fname = "SKI_DATA/msg.txt"
    try:
        f = open(fname, 'r')
    except IOError:
        print ("Could not read file:", fname)
        sys.exit()
    
    with f:
        count = 0
        while  True:
            line = f.readline()
            if len(line) == 0:
                break;
            count += 1
            
           
            data = line.split(" ")
            if len(data) > 0:
                for k in range(len(data)):
                    if len(data[k])>1 and data[k][0] == '[':
                        #data[k]=data[k].strip('[')
                        #data[k]=data[k].strip(':')
                        for l in range(len(data)-1):
                            if len(data[l+1] > 0):
                                break
                        if l <     
                            
                            
                        print("%s %s %s" %(data[k], len(data[k+1]), len(data[k+2])))
           
        
            if count > 10:
                break    
        print("size is %d line" % count)        
        


def main():
    #print("hello")
    
    GetData()


if __name__ == '__main__':
    main()