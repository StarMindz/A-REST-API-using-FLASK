import pandas as pd
from flask import Flask, jsonify, request


data =pd.read_csv("dataset_diabetes\\diabetic_data.csv")
data =data.head(100)
data=data.dropna()

#identity= list(data.encounter_id)
identity = data.encounter_id.values.tolist()

data = data.set_index(data["encounter_id"], drop = True)
#data =data.drop("encounter_id",1)

record = []

#features = list(data.columns)

features = data.columns.values.tolist()
def get_record(ids):
    global data
    global features
    data1 = data.loc[ids]
    dicts = {}
    for items in features:
        dicts[items]=str(data1[items])
    return dicts

for ids in identity:
    record.append(get_record(ids))


app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return "An api for returning the health records of hospital patients under Kaduna state Health Insurance"

@app.route('/records/all', methods=['GET'])
def api_all():
    global record
    return jsonify(record)

@app.route('/records', methods=['GET'])
def api_id():
    global record
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

        # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for item in record:
        if int(item["encounter_id"]) == id:
            results.append(item)



    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()