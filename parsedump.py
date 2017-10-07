import json

with open('stripped_json.json', 'w') as wf:
    wf.write("[")
    for i in range(3, 4475):
        strIndex = str(i)
        if i < 10:
            strIndex = "000" + strIndex
        elif i < 100:
            strIndex = "00" + strIndex
        elif i < 1000:
            strIndex = "0" + strIndex


        with open('raw/' + strIndex + '_s.txt', 'r') as f:
            read_data = f.read()
            try:
                instanceJson = json.loads(read_data.split("<script>require(\"TimeSlice\").guard(function() {require(\"ServerJSDefine\").handleDefines")[-1].split("handleServerJS(")[-1].split(",\"h0\"")[-2])
                if(instanceJson['require']):
                    for rNode in instanceJson['require'][4][3]:
                        if rNode['props']['comments']['idMap']:
                            wf.write(json.dumps(rNode['props']['comments']['idMap']) + ",")
            except IndexError:
                print("Skipping one at " + strIndex)
                #Do nothing, just eat the error
    wf.write("]")