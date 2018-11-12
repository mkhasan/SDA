import matplotlib.pyplot as plt 
import sys

def GetData():
    fname = "SKI_DATA/msg2.txt"
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
                        print(data[k])
           
        
            if count > 10:
                break    
        print("size is %d line" % count)        
        


def main():
    #print("hello")
    
    GetData()


if __name__ == '__main__':
    main()