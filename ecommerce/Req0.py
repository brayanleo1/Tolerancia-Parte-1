from flask import Flask, request, jsonify
import requests
import threading
from requests.adapters import HTTPAdapter, Retry

app = Flask(__name__)

last_exchange_rate = 1
process_in_the_log = False

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
    global process_in_the_log

    s = requests.Session()

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
    product = s.get('http://store:5001/product', headers=headers, data=product_data)
    print(product)

    if product.status_code != 200:
        if ft:
            for i in range(3):
                product = s.get('http://store:5001/product', headers=headers, data=product_data)
                if product.status_code == 200:
                    break
            return jsonify({"message": "Erro ao tentar conectar com o product"}), 500
        else:
            return jsonify({"message": "Erro ao tentar conectar com o product"}), 500
    
    # Request to the exchange rate service
    try:
        exchange = s.get('http://exchange:5002/exchange', headers=headers)
    except requests.exceptions.RequestException:
        if ft:
            exchange = jsonify({"exchange_rate": last_exchange_rate})
        else:
            return jsonify({"message": "Erro ao tentar conectar com o exchange"}), 500


    if exchange.status_code == 200:
        last_exchange_rate = exchange.json()["exchange_rate"]

    sell_data = '{"product_id": ' + str(product_id) + '}'

    # Request to the store selling service
    sell = s.post('http://store:5001/sell', headers=headers, data=sell_data)

    if sell.status_code != 200:
        if ft:
            for i in range(3):
                sell = s.post('http://store:5001/sell', headers=headers, data=sell_data)
                if sell.status_code == 200:
                    break
            return jsonify({"message": "Erro ao tentar conectar com o /sell"}), 500
        else:
            return jsonify({"message": "Erro ao tentar conectar com o /sell"}), 500
    
    bonus_data = '{"user_id": ' + str(user_id) + ', "bonus_value": ' + str(round(product.json()["value"])) + '}'

    # Request to the fidelity service
    bonus = s.post('http://fidellity:5004/bonus', headers=headers, data=bonus_data)

    if bonus.status_code != 200:
        if ft:
            # Now open the file log.txt and write the user_id and bonus_value on the last line
            with open("log.txt", "a") as file:
                file.write(" " + str(user_id) +" "+ str(round(product.json()["value"])) + f"\n")
            # Now set the process_in_the_log to True
            process_in_the_log = True

            # Now create a timer thread to try to process the log in 20 seconds
            timerT =  threading.Timer(20, process_log)
            timerT.start()
            print("Log saved")
        else:
            return jsonify({"message": "Erro ao tentar conectar com o bonus"}), 500

    return jsonify({"message": "Success"}), 200

def process_log():
    print("Processing log")
    global process_in_the_log

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    if process_in_the_log:
        print("Let's process the log")
        with open("log.txt", "r") as file:
            for line in file:
                user_id, bonus_value = line.split()
                bonus_data = '{"user_id": ' + str(user_id) + ', "bonus_value": ' + str(bonus_value) + '}'
                bonus = requests.post('http://fidellity:5004/bonus', headers=headers, data=bonus_data)
                if bonus.status_code == 200:
                    # Remove the line from the log file
                    with open("log.txt", "r") as file:
                        lines = file.readlines()
                    with open("log.txt", "w") as file:
                        for line2 in lines:
                            if line2 != line:
                                file.write(line2)
                                break
                else:
                    threading.Timer(20, process_log) #Try again in 20 seconds
    process_in_the_log = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)