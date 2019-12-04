
#Demo file  to convert output json file to ODF xml

import sys
import json

def convXml():

    mstr = ("{\n"
    "\t\"XML\": {\n"
        "\t\t\"version\": 1.0,\n"
        "\t\t\"encoding\": \"UTF-8\"\n"
    "\t},\n"
    "\t\"Comment\": \" Example of a simple odf structure for a refrigerator. \",\n"
    "\t\"Objects\": {\n"
        "\t\t\"xmlns:xsi\": \"http://www.w3.org/2001/XMLSchema-instance\",\n"
        "\t\t\"xsi:noNamespaceSchemaLocation\": \"odf.xsd\",\n"
    );
    m1 = (
        "\t\t\"Object\": {\n"
            "\t\t\t\"type\": \"Refrigerator Assembly Product\",\n"
    );
    m2 = (
        "\t\t\t\"InfoItem\": {\n"
            "\t\t\t\t\"name\": \"temperature\"\n"
            "\t\t\t\t\"description\": \"Temperature\",\n"
            "\t\t\t\t\"value\": [\n"
			"\t\t\t\t\t{\n"
			"\t\t\t\t\t\t\"unit\": \"mCelsius\",\n"
    );
    m3 = (
        "\t\t\t\t\t}\n"
        "\t\t\t\t]\n"
        "\t\t\t},\n"
        "\t\t\"InfoItem\": {\n"
        "\t\t\t\"name\": \"humidity\",\n"
        "\t\t\t\"description\": \"Humidity\",\n"
        "\t\t\t\t\"value\": [\n"
		"\t\t\t\t\t{\n"
		"\t\t\t\t\t\t\"unit\": \"numbers\",\n"
    );
    m4 = (
		"\t\t\t\t\t}\n"
        "\t\t\t\t]\n"
        "\t\t\t}\n"
        "\t\t},\n"
    );
    m5 = (
        "\t}\n"
        "}"
    );
    fout = 'output/demo.xml'
    with open(fout, 'w') as ofile:
        ofile.write(mstr);

        count = 0;
        f = open('output/iot-1-demo.jsonl','r',encoding="utf8")
        n = 0;
        for row in f:
            #print("row=",row)
            ofile.write(m1);
            if len(row) < 5:
                continue;
            
            d = json.loads(row)
            if d.get("sensors") != None:
                sn = d["sn"]
                ds = d["sensors"]
                ofile.write("\t\t\t\"id\": \"" + sn + "\",\n");
                ofile.write(m2);
                ofile.write("\t\t\t\t\t\t\"value\":" + str(ds["temp"]["value"]) + "\n");
                ofile.write(m3);
                ofile.write("\t\t\t\t\t\t\"value\":" + str(ds["humidity"]["value"]) + "\n");
                ofile.write(m4);
                
            count += 1;
            n += 1;
            if n > 1:
                break;
        ofile.write(m5);

        print ('generated xml file is ',fout)
        

#Demo of convertin the output json file to ODF xml
# This takes the demo file 'output/iot-1-demo.jsonl'
#   and converts it into the xml file - 'output/demo.xml'
if __name__ == '__main__':
    convXml()
