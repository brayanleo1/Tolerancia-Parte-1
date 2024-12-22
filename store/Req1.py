from flask import Flask, request, jsonify
import random
import uuid
import requests
from requests.adapters import HTTPAdapter, Retry
import threading

app = Flask(__name__)

failing = False

@app.route('/product', methods=['GET'])
def request1():
    s = requests.Session()

    retries = Retry(total=0,
                    backoff_factor=0.1,
                    status_forcelist=[ 500, 502, 503, 504 ])

    s.mount('http://', HTTPAdapter(max_retries=retries))

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Simular falha de omissão com 20% de probabilidade
    if random.random() < 0.2:
        print("Request 1 (Store): Falha de omissão simulada.")
    else:
        data = request.get_json()
        product_id = data["product_id"]

        # Mandar requisição para o banco de dados
        product_data = '{"command": "select", "table": "products", "value_1": ' + str(product_id) + '}'
        store = s.post('http://database:5005/data_access', headers=headers, data=product_data)
        store = store.json()
        # Simular resposta bem-sucedida
        #product = {"id": product_id, "name": store["name"], "value": store["value"]}
        print("Request 1 (Store): Sucesso - {product}")
        return store, 200
    

failing = False
@app.route('/sell', methods=['POST'])
def request3():
    s = requests.Session()

    retries = Retry(total=0,
                    backoff_factor=0.1,
                    status_forcelist=[ 500, 502, 503, 504 ])

    s.mount('http://', HTTPAdapter(max_retries=retries))

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    global failing
    # Simular falha de erro com 10% de probabilidade e duração de 5 segundos

    if failing:
        print("Request 3 (Store): Falha de erro simulada.")
        return jsonify({"message": "Internal server error"}), 500

    if random.random() < 0.1:
        print("Request 3 (Store): Falha temporária.")
        failing = True
        timer_name = threading.Timer(5, activate_error)
        timer_name.start()
        return jsonify({"message": "Internal server error"}), 500
    
    data = request.get_json()
    product_id = data["product_id"]

    # Simular resposta bem-sucedida
    transaction_id = str(uuid.uuid4())  # Gerar ID único para a transação

    # Mandar requisição para o banco de dados
    transaction_data = '{"command": "insert", "table": "transactions", "value_1": ' + transaction_id + ', "value_2": ' + str(product_id) + '}'
    s.post('http://database:5005/data_access', headers=headers, data=transaction_data)
    
    print(f"Request 3 (Store): Sucesso - Transação ID: {transaction_id}")
    return jsonify({"transaction_id": transaction_id}), 200

def activate_error():
    global failing
    failing = False
    print("Request 3 (Store): Falha temporária finalizada.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
