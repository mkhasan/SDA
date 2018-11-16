import matplotlib.pyplot as plt 
import sys
import datetime
from collections import namedtuple
import ctypes


JointData = namedtuple("JointData", ["LHP", "LHR", "LHY" , "LKP", "LAP", "RHP", "RHR", "RHY", "RKP", "RAP"])
nodeId = 0x40e

class Joint: 
    def __init__(self, elapsed_sec, ctrl_or_status, encoder_count):
        self.elapsed_sec = elapsed_sec
        self.ctrl_or_status = ctrl_or_status
        self.encoder_count = encoder_count


def ListToInt(list):
    
    str = ""
    for k in range(4):
        str += list[4-k-1]
    
    ret = ctypes.c_int(int(str, 16))
        
    
    
    return ret.value
    
    
        
    """
    val = []
    for k in range(4):
        val.append(int(list[k], 16))
    
    ret = val[3] << 24 | val[2] << 16 | val[1] << 8 | val[0]
    return ret
    """    
        
    
def GetData():
    fname = "SKI_DATA/t2.txt"
    try:
        f = open(fname, 'r')
    except IOError:
        print ("Could not read file:", fname)
        sys.exit()
    
    span = 6000
    startRow = 1549220-span
    totalRow = span
    
    targetStartId = 0x409
    actualStartId = 0x389
    errorStartId = 0x89
    
    target = JointData(LHP=[], LHR=[], LHY=[], LKP=[], LAP=[], RHP=[], RHR=[], RHY=[], RKP=[], RAP=[])
    
    actual = JointData(LHP=[], LHR=[], LHY=[], LKP=[], LAP=[], RHP=[], RHR=[], RHY=[], RKP=[], RAP=[])
    
    error = JointData(LHP=[], LHR=[], LHY=[], LKP=[], LAP=[], RHP=[], RHR=[], RHY=[], RKP=[], RAP=[])
    
    with f:
        count = 0
        okay = False;
        actual_total = 0;
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
                                    
                                    value = ListToInt([data[l+5], data[l+6], data[l+7], data[l+8]])
                                    
                                    if value > 50000:
                                        pass #print("line no %d value %d" % (count+1, value))
                                    joint = Joint((now-start).total_seconds(), "", value)
                                    target[id-targetStartId].append(joint)
                                    
                                if id >= actualStartId and id < actualStartId+len(actual) and len(data) > l+8:     
                                    #if int(data[l+2],16) == nodeId:
                                    #print("count: %d %s %s %s %s " %(count+1, data[k], data[l], data[l+2], data[l+5]))
                                    #    print((now-start).total_seconds())
                                    if id == 0x38b:
                                        actual_total += 1
                                    
                                    if actual_total == 194:
                                        print("looking for the line %d" % count) 
                                    
                                    value = ListToInt([data[l+5], data[l+6], data[l+7], data[l+8]])
                                    
                                    if value > 50000000:
                                        pass #print("line no %d value %d" % (count+1, value))
                                    joint = Joint((now-start).total_seconds(), "", value)
                                    actual[id-actualStartId].append(joint)
                                    
                                    
                                if id >= errorStartId and id < errorStartId+len(error):
                                    error[id-errorStartId].append((now-start).total_seconds())      
                                    #if int(data[l+2],16) == nodeId:
                                    #print("count: %d %s %s %s %s " %(count+1, data[k], data[l], data[l+2], data[l+5]))
                                    #    print((now-start).total_seconds())
                                    
                                    
                                    
                                for i in range(len(data)-l-1):
                                    pass #print("data %d is %s" % (i, data[i+l+1]))
                                    
                                    

            
                
            if count >= startRow and okay == False:
                print("Error !!!")
                sys.exit(1)
                
            count += 1
                
        print("size is %d line" % count)        
        
        return [target, actual, error]


def main():
    #print("hello")
    
    #str = "5f 49 00 00"
    #list = str.split(" ")
    #print("resutl is %d " % GetValue(list))
    
    #str = "75 f5 ff ff"
    #list = str.split(" ")
    
    
    
    #print("str is %s value is %d" % (str, ListToInt(list)))
    
    #return
    [target, actual, error] = GetData()
    
    time_target = []
    count_target = []
    
    index = 0
    
    if len(sys.argv) > 1:
        for k in range(len(JointData._fields)):
            if sys.argv[1] == JointData._fields[k]:
                break
        
        if k == len(JointData._fields)-1:
            print("Invalid argument")
            sys.exit(1)
        
        index = k
        
    for k in range(len(target[index])):
        joint = target[index][k]
        time_target.append(joint.elapsed_sec)
        count_target.append(joint.encoder_count)

    print("Joint is %s" % JointData._fields[index])
    print("target size is %d %d" %(len(time_target), len(count_target)))

    time_actual = []
    count_actual = []
    list 
    
    for k in range(len(actual[index])):
        joint = actual[index][k]
        time_actual.append(joint.elapsed_sec)
        count_actual.append(joint.encoder_count)
        
        
    

    print("actual size is %d %d" %(len(time_actual), len(count_actual)))
    
    print(("# of times error occured %d" % len(error[index])))
    
    gap = 0.0
    gapIndex = -1
    for k in range(len(count_actual)):
        if gap < abs(count_target[k]-count_actual[k]):
            gap = abs(count_target[k]-count_actual[k])
            gapIndex = k
    
    print("gap index %d gap is %f target %f actual %f final time %f" %(gapIndex, gap, time_target[gapIndex], time_actual[gapIndex], time_actual[len(time_actual)-1]))
    plt.plot(time_target, count_target)
    
    plt.plot(time_actual, count_actual)
    
    plt.xlabel('time') 
    # naming the y axis 
    plt.ylabel('value') 
      
    # giving a title to my graph 
    if len(error[index]) > 0:
        plt.title("%s error occured at %f" %(JointData._fields[index], error[index][0]))
    else:
        plt.title("%s no error occured " %(JointData._fields[index]))     
   
    plt.legend() 
   
    plt.show()
    #print("done")
    plt.close()   
        
    #plt.plot(target.elapsed_sec, blockData[count], label=BlockData._fields[count])
    #print("target of %s  size %d also len is %d " % (target._fields[nodeId-0x409], len(target[nodeId-0x409]), len(target) ))

if __name__ == '__main__':
    main()