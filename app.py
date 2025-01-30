from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

data = pd.read_csv("Kolhapur.csv")  # Load the CSV file

@app.route('/')
@app.route('/')
def home():
    sources = data['Source'].unique().tolist()
    destinations = data['Destination'].unique().tolist()
    return render_template('index.html', sources=sources, destinations=destinations)


@app.route('/search', methods=['POST'])
def search():
    source = request.form.get('source').strip().lower()
    destination = request.form.get('destination').strip().lower()
    
    filtered_trains = data[(data['Source'].str.lower() == source) & (data['Destination'].str.lower() == destination)]
    
    if filtered_trains.empty:
        return jsonify({"message": "No trains available for this route."})
    
    results = filtered_trains.to_dict(orient='records')
    return jsonify(results)

@app.route('/stations')
def get_stations():
    stations = sorted(set(data['Departure Station(code)'].tolist() + data['Arrival Station(code)'].tolist()))  # Get unique stations
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
