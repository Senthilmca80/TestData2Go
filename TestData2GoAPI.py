from flask import Flask, jsonify, request, render_template
import LinkingCustomDataModel as fDataMapping

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/Health', methods=['GET'])
def Health():
    return jsonify({"message": "Hello, Im listening "})

@app.route('/api/getSampleData', methods=['POST'])
def create_TestData():
    data = request.get_json()  # Get JSON data from request body
    print(data)
    try:
        sresponse = fDataMapping.returnAPIResponse(data)
    except AttributeError as e:
        sresponse = str(e)
        print(f"Error: {e}")
    return jsonify(sresponse), 201

if __name__ == '__main__':
    app.run(debug=True)
