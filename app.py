from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API_KEY
API_KEY = '3d46f3a54983571379d54b094b1be228'

@app.route('/', methods=['GET', 'POST'])
def currency_converter():
    if request.method == 'POST':
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])

        # API Endpoint, access key, and required parameters
        endpoint = 'convert'

        # API URL
        url = f'http://api.exchangerate.host/{endpoint}?access_key={API_KEY}&from={from_currency}&to={to_currency}&amount={amount}'

        # API request using the requests library
        response = requests.get(url)
        data = response.json()

        # Errors in the API response
        if 'error' in data and isinstance(data['error'], dict):
            error_info = data['error'].get('info', 'Unknown Error')
            
            # Print the complete API response for debugging
            print("Complete API Response:", data)
            
            return render_template('error.html', error_message=error_info)

        # Access the conversion result
        if 'result' in data and isinstance(data['result'], (int, float)):
            conversion_result = data['result']
            return render_template('result.html', from_currency=from_currency, to_currency=to_currency,
                                   amount=amount, converted_amount=conversion_result)
        else:
            return render_template('error.html', error_message='Result Not Available')


    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


