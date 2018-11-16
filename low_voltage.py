import matplotlib.pyplot as plt 
import sys
import datetime
from collections import namedtuple


JointData = namedtuple("JointData", ["LHP", "LHR", "LHY" , "LKP", "LAP", "RHP", "RHR", "RHY", "RKP", "RAP"])
nodeId = 0x40e

class Joint: 
    def __init__(self, elapsed_sec, ctrl_or_status, encoder_count):
        self.elapsed_sec = elapsed_sec
        self.ctrl_or_status = ctrl_or_status
        self.encoder_count = encoder_count


def GetStrToInt(list):
    val = []
    for k in range(4):
        val.append(int(list[k], 16))
    
    ret = val[3] << 24 | val[2] << 16 | val[1] << 8 | val[0]
    return ret    
        
    
def GetData():
    fname = "SKI_DATA/t2.txt"
    try:
        f = open(fname, 'r')
    except IOError:
        print ("Could not read file:", fname)
        sys.exit()
    
    span = 1000
    startRow = 1549220-span
    totalRow = span
    
    targetStartId = 0x409
    actualStartId = 0x389
    
    target = JointData(LHP=[], LHR=[], LHY=[], LKP=[], LAP=[], RHP=[], RHR=[], RHY=[], RKP=[], RAP=[])
    
    actual = JointData(LHP=[], LHR=[], LHY=[], LKP=[], LAP=[], RHP=[], RHR=[], RHY=[], RKP=[], RAP=[])
    
    with f:
        count = 0
        okay = False;
        while  True:
            line = f.readline()
            if len(line) == 0:
                break;
            
            if count >= startRow and count < startRow+totalRow:
           
                data = line.split(" ")
                #for k in range(len(data)):
                #    print("data %d is %s" % (k, data[k]))
                if len(data) > 5: 
                    for k in range(len(data)):
                        if len(data[k])>1 and data[k][0] == '[':
                            data[k]=data[k].strip('[')
                            data[k]=data[k].strip(':')
                            for l in range(len(data)-1):
                                if len(data[l+1]) > 0:
                                    break
                            if l < len(data)-1:    
                                l += 1;
                                data[l]=data[l].strip(']')
                                
                                if count == startRow:
                                    start = datetime.timedelta(seconds=int(data[k]), microseconds=int(data[l]))
                                    okay = True;
                                now = datetime.timedelta(seconds=int(data[k]), microseconds=int(data[l]))
                                
                                id = int(data[l+2],16)
                                
                                if id >= targetStartId and id < targetStartId+len(target):     
                                    #if int(data[l+2],16) == nodeId:
                                    #print("count: %d %s %s %s %s " %(count+1, data[k], data[l], data[l+2], data[l+5]))
                                    #    print((now-start).total_seconds())
                                    
                                    value = GetStrToInt([data[l+5], data[l+6], data[l+7], data[l+8]])
                                    
                                    if value > 20000:
                                        print("line no %d value %d" % (count+1, value))
                                    joint = Joint((now-start).total_seconds(), "", value)
                                    target[id-targetStartId].append(joint)
                                '''    
                                if id >= actualStartId and id < actualStartId+len(actual):     
                                    #if int(data[l+2],16) == nodeId:
                                    #print("count: %d %s %s %s %s " %(count+1, data[k], data[l], data[l+2], data[l+5]))
                                    #    print((now-start).total_seconds())
                                    
                                    value = GetStrToInt(data[l+5], data[l+6], data[l+7], data[l+8])
                                    actual[id-actualStartId].append(Joint((now-start).total_seconds(), "", value))
     
                                    
                                        #target[nodeId-0x409].append((now-start).total_seconds())
                                    
                                    
                                for i in range(len(data)-l-1):
                                    print("data %d is %s" % (i, data[i+l+1]))
                                    
                                '''    

            
                
            if count >= startRow and okay == False:
                print("Error !!!")
                sys.exit(1)
                
            count += 1
                
        print("size is %d line" % count)        
        
        return [target, actual]


def main():
    #print("hello")
    
    #str = "5f 49 00 00"
    #list = str.split(" ")
    #print("resutl is %d " % GetValue(list))
    [target, actual] = GetData()
    
    time = []
    count = []
    list 
    index = 0
    for k in range(len(target[index])):
        joint = target[index][k]
        time.append(joint.elapsed_sec)
        count.append(joint.encoder_count)

    print("size is %d %d" %(len(time), len(count)))
    plt.plot(time, count)
    
    plt.xlabel('time') 
    # naming the y axis 
    plt.ylabel('value') 
      
    # giving a title to my graph 
    plt.title("test") 
   
    plt.legend() 
   
    plt.show()
    #print("done")
    plt.close()   
        
    #plt.plot(target.elapsed_sec, blockData[count], label=BlockData._fields[count])
    #print("target of %s  size %d also len is %d " % (target._fields[nodeId-0x409], len(target[nodeId-0x409]), len(target) ))

if __name__ == '__main__':
    main()