from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

last_exchange_rate = 1

#This request will receive
"""
product – id do produto a ser comprado
• user – id do usuário que está executando a compra
• ft – parâmetro que vai indicar se a tolerância a falhas está ativada ou não (true ou
false) 
"""
#And will return success or failure after requesting the other services
"""
It applies the following failure tolerance strategy if the ft parameter is true:
* If the request to the store product information service fails, the request must be retried up to 3 times.
  - This goes to the route /product
* If the request to the exchange rate service fails, the request must use the last known exchange rate.
  - This goes to the route /exchange
* If the request to the store selling service fails, it must be retried up to 3 times with a 5-second interval between retries.
    - This goes to the route /sell
* If the request to the fidelity service fails, it will store a log with the user ID and the bonus value for later processing.
    - This goes to the route /bonus
"""
@app.route('/buy', methods=['POST'])
def request0():
    global last_exchange_rate

    data = request.get_json()
    product_id = data["product_id"]
    user_id = data["user_id"]
    ft = False
    if data["ft"] == "True":
        ft = True

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    product_data = '{"product_id": ' + str(product_id) + '}'
    
    # Request to the store product information service
    product = requests.get('http://localhost:5001/product', headers=headers, data=product_data)
    print(product)

    if product.status_code != 200:
        if ft:
            for i in range(3):
                product = requests.get('http://localhost:5001/product', headers=headers, data=product_data)
                if product.status_code == 200:
                    break
        else:
            return jsonify({"message": "Internal server error"}), 500
    
    # Request to the exchange rate service
    exchange = requests.get('http://localhost:5002/exchange', headers=headers)

    if exchange.status_code == 200:
        last_exchange_rate = exchange.json()["exchange_rate"]

    if exchange.status_code != 200:
        if ft:
            exchange = jsonify({"exchange_rate": last_exchange_rate})
        else:
            return jsonify({"message": "Internal server error"}), 500

    sell_data = '{"product_id": ' + str(product_id) + '}'

    # Request to the store selling service
    sell = requests.post('http://localhost:5003/sell', headers=headers, data=sell_data)

    if sell.status_code != 200:
        if ft:
            for i in range(3):
                sell = requests.post('http://localhost:5003/sell', headers=headers, data=sell_data)
                if sell.status_code == 200:
                    break
        else:
            return jsonify({"message": "Internal server error"}), 500
    
    bonus_data = '{"user_id": ' + str(user_id) + ', "bonus_value": ' + str(round(product.json()["value"])) + '}'

    # Request to the fidelity service
    bonus = requests.post('http://localhost:5004/bonus', headers=headers, data=bonus_data)

    if bonus.status_code != 200:
        if ft:
            # Store log with user ID and bonus value
            print(f"Request 0 (Store): Falha ao conceder bônus de {bonus_data['bonus_value']} ao usuário {bonus_data['user_id']}.")
        else:
            return jsonify({"message": "Internal server error"}), 500

    return jsonify({"message": "Success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)