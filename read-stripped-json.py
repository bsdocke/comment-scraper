import json
import requests
with open("stripped_json.json") as f:
    with open("tsv_author_comment_time_score_magnitude.tsv", 'w', encoding="utf-8") as tsvfile:
        payload = json.loads(f.read())
        for jsonLine in payload:
            userIdToNameDict = {}
            for key,value in jsonLine.items():
                if(value['type'] == 'user'):
                    userIdToNameDict[value['id']] = value['name']
            for key,value in jsonLine.items():
                if(value['type'] == 'comment'):
                    value['authorID'] = userIdToNameDict[value['authorID']]
                    reqPay = {'document': {'content': value['body']['text'].replace('\n', '').replace('\r', ''),'type':"PLAIN_TEXT"},'encodingType': "UTF8"}
                    r = requests.post("https://language.googleapis.com/v1/documents:analyzeSentiment?fields=documentSentiment&key=AIzaSyBUXYloODq43OpqK3oneREsZHQs-Pr88HU", json=reqPay)
                    responseObj = json.loads(r.text)
                    output = value['authorID'] + "~" + value['body']['text'].replace('\n', '').replace('\r', '') + "~" + str(value['timestamp']['time']) + "~" + str(responseObj['documentSentiment']['score']) + "~" + str(responseObj['documentSentiment']['magnitude'])+"\n"
                    tsvfile.write(output)

