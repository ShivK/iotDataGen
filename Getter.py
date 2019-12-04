import Util as ut
#FieldTypes
#selFromList
#  select from a list (random, next)


def getValueFromList(clusA,rec,valA):
    n = ut.gen_number(0,len(vA))
    #print ("HCPGEnVal n=",n)
    val = valA[n]
    return val

#def genData(sensors,prevRec):
def genData(dev,num,tm):
    sensors = dev["sensors"]
    rec= {}

    for s in sensors:
        fieldType = s["type"]
        fieldName = s["name"]
        val = ""

        if fieldType == "selFromList":
            if s.get("random") != None:
                valA = s["random"]  
                val = valA[ut.gen_number(0,len(valA))]             
            elif s.get("next") != None:
                valA = s["next"]
                val = valA[valA.index(fieldName) + 1]
        elif fieldType == "IntRange":
            minV = s["min"]
            maxV = s["max"]
            val = ut.gen_number(minV,maxV)
        elif fieldType == "DecRange":
            minV = s["min"]
            maxV = s["max"]
            rnd = s["dec"]
            val = ut.gen_dec2(minV,maxV,rnd)
        elif fieldType == "dev.uuid2":
            uuidFormat = dev["uuid"]
            num1 = num // 10
            num2 = num % 10
            val = uuidFormat.format(num1,num2)
        elif fieldType == "dev.uuid":
            uuidFormat = dev["uuid"]
            val = uuidFormat.format(num)
        elif fieldType == "timestamp":
            val = str(tm)
            
        
        rec[fieldName] = val

        #print ("Getter:gendata() ftype,fname,val=",fieldType,fieldName,val)
    #print ("rec",rec)
        
    return rec
