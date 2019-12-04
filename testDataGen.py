import sys
import json

#Counts the number of records
#  and verifies that the records are valid json
def testCount(fname):
    count = 0;
    f = open(fname,'r',encoding="utf8")
    for row in f:
        if len(row) < 5:
            continue;
        d = json.loads(row)
        count += 1;
    print ('Number of records in the file {} is {}'.format(fname,count));

#Entry into the testDataGen CLI command
#Current usage is 'testDataGen <output json file>'
if __name__ == '__main__':
    if len(sys.argv) == 2:
        fname = sys.argv[1].strip()
        testCount(fname)
    else:
        print("Usage: testDataGen <outout json file>")
        print("Example: testDataGen iot-1-out.jsonl")

