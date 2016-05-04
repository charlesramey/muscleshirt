import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 

def sendRequest(features_dict):
    #this may be overhead from the features dict generator
    if "_exercise" in features_dict:
        del features_dict["_exercise"]

    col_names = sorted(features_dict.keys())
    feature_vals = [features_dict[x] for x in col_names]

    data =  {

            "Inputs": {

                    "Web Input":
                    {
                        "ColumnNames": col_names,
                        "Values": [ [features_dict[x] for x in col_names] ]
                    },        },
                "GlobalParameters": {
    }
        }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/4925149493ee40cab4f7eafa6a103efe/services/59b6774ecdcb485899a0ea14e9c5c28c/execute?api-version=2.0&details=true'
    api_key = 'F4chWkRYZz0cPLB9H3lv+YUQihhAa9FFPFa+RGHv/J4xlp+2cBhRKFpsR+c903gV2kk0KnKZzTMWbg5GVgOT4A==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib2.Request(url, body, headers) 

    try:
        response = urllib2.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)

        result = response.read()
        return result

    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read()))    