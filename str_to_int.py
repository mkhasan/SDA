

from low_voltage import ListToInt
import sys


    

        
def main():
    #print("hello")
    
    
    
    if len (sys.argv) < 5:
        print("Invalid input !!!") 
        sys.exit(1)
        
    list = []
    
    for k in range(4):
        list.append(sys.argv[1+k])
    
    print(ListToInt(list))
    
        
if __name__ == '__main__':
    main()