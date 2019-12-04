import random
import time
from datetime import date, datetime, timedelta
import re


def gen_number(minV, maxV):
    if minV == maxV:
        return minV
    else:
        return random.randrange(minV, maxV);

def gen_dec2(minV,maxV,r):
    n = round(random.uniform(minV, maxV), r);
    return n

def gen_dec200(minV,maxV,m):
    n = random.randrange(int(m * minV),int( m* maxV))/m
    return n

def add_seconds(tm,sec):
    t = tm + timedelta(seconds=sec)
    return t


#start and end should be strings specifying times in the format spec
def strTimeProp(start, end, format, prop):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

#takes only dates after 1980
def gen_date(st_date, end_date,bias):
    return strTimeProp(st_date, end_date, '%m/%d/%Y', bias)

#For older dates (before 1980)
#generate a date approx between the two dates given
def gen_date_old(st_date, end_date,bias):
    stA = st_date.split("/")
    endA=end_date.split("/")
    new_date = [0,0,0]
    new_date[0] = gen_number(1,12) #month
    new_date[1] = gen_number(1,28) #day
    diff_yr = int(endA[2]) - int(stA[2])
    yr_inc = gen_number(0,diff_yr)
    yr = int(stA[2]) + yr_inc
    new_date[2] = yr
    ret_date = "/".join(str(x) for x in new_date)
    
    return ret_date

#add the specified number to the year
def add_year_date(st_date, num):
    stA = st_date.split("/")
    yr = int(stA[2]) + num
    stA[2] = str(yr)
    ret_date = "/".join(x for x in stA)
    return ret_date

def convDateFormat(dt):
    stA = dt.split("/")
    rt = stA[2]+stA[0]+stA[1]
    return rt
    
    
    

#bias array is a percetage of probable values
#ex: A = ['WWII', 'Korea', 'Vietnam', 'GulfWar']
#pct of people belonging to each era [5,10,30,55]
# bias = [5,15,45,100]
def gen_number_bias(biasA):
    n = gen_number(0,99)
    res = 0;

    for i in range(len(biasA)):
        if n < biasA[i]:
            res = i;
            break;
    return res
            
def ufilter(t,pat):
    a = pat.sub(' ', t)
    return a

def test1():
    regex = re.compile('[^a-zA-Z0-9-]')
    a = 'ab3d*-E'
    print (a)
    a = ufilter(a,regex)
    print(a)

def test2():
    iotDateFrom="01/01/2015"
    iotTimeFrom="14/01/01"
    format = '%m/%d/%Y';
    stA = iotDateFrom.split("/")
    tA= iotTimeFrom.split("/")
    t = datetime(int(stA[2]),int(stA[1]),int(stA[0]),int(tA[0]),int(tA[1]),int(tA[2]))
    
    #t = time.mktime(time.strptime(iotDateFrom, format))
    print(t)
    interval = timedelta(seconds=5)
    #t = time.strftime(format, time.localtime(ptime))
    print("int=",interval)
    t2 = t + interval
    #print ("t2=", t2.ctime())
    print ("t2=", t2)
    print ("t2str=", str(t2))

def test3():
    s = "\"{2345"
    print ("s="+s)
    s = s.replace("\"{","-")
    print ("s="+s)

    for i in range(10):
        n = gen_dec2(1.1,20.5,1)
        print("n=",n)
        n2=gen_dec200(1.1,20.5,10)
        print("n2=",n2)

def test():
    biasA= [5,15,45,100]
    
    res = gen_number_bias(biasA)
    print (res)
    
if __name__ == '__main__':
    #test1()
    test2()
    test3()
