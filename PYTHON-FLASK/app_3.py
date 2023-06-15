import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import pandas as pd

# Create a Flask app
app = Flask(__name__)

# Connect to the database
conn = psycopg2.connect(database="stockprice_db", 
                        user="elaine", 
                        password="1234", 
                        host="127.0.0.1", 
                        port="5432")

@app.route('/', methods=['GET'])
def index():
    return render_template('search_test_3.html')

@app.route('/search', methods=['GET'])
def search():
    stock_code = request.args.get('stock_code')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Create a cursor
    cur = conn.cursor()

    # Execute the SQL query
    postgres = f"SELECT stock_code,date,opening_price,highest_price,lowest_price,closing_price FROM stock_price WHERE date BETWEEN '{start_date}' AND '{end_date}' AND stock_code='{stock_code}'"
    cur.execute(postgres)

    # Get the data as a pandas DataFrame
    name = [desc[0] for desc in cur.description]
    ## fetchall是將所有收尋的資料都寫入 data 中
    data = pd.DataFrame(cur.fetchall(),columns=name)
    #print(data)

    # Convert the date column to datetime for proper formatting
    data['date'] = pd.to_datetime(data['date'])

    # Generate the Candlestick chart using Plotly
    fig = go.Figure(data=[go.Candlestick(x=data['date'],
                                         open=data['opening_price'],
                                         high=data['highest_price'],
                                         low=data['lowest_price'],
                                         close=data['closing_price'])])


    # Convert the Plotly figure to JSON
    chart_json = fig.to_json()

    # Close the cursor
    cur.close()

    #return render_template('search_test_3.html', data=data.to_dict('records'), chart=chart_json)
    return render_template('search_test_3.html', chart=chart_json)

if __name__ == "__main__":
    app.run(debug=True)
