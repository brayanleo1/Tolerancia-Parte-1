from flask import Flask, request, jsonify
import random
import threading
import time
import requests
from requests.adapters import HTTPAdapter, Retry


failing = False

app = Flask(__name__)

@app.route('/bonus', methods=['POST'])
def request4():
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
        print("Request 4 (Fidelity): Simulando atraso de 2 segundos (falha de tempo).")
        time.sleep(2)
        return jsonify({"Operation": "Fail by timeout"}), 408

    if random.random() < 0.1:
        print("Request 4 (Store): Falha de timeout.")
        failing = True
        timer_name = threading.Timer(30, activate_error)
        timer_name.start()
        time.sleep(2)
        return jsonify({"Operation": "Fail by timeout"}), 408
    
    data = request.get_json()
    bonus_value = data["bonus_value"]

    # Select the bonus value from the database
    bonus_data = '{"command": "select", "table": "users", "value_1": ' + str(data["user_id"]) + '}'
    bonus = s.post('http://localhost:5005/data_access', headers=headers, data=bonus_data)
    
    #now sum the bonus value
    bonus_value += bonus["bonus"]

    user_id = data["user_id"]

    database_data = '{"command": "update", "table": "users", "value_1": ' + str(user_id) + ', "value_2": ' + str(bonus_value) + '}'

    #Manuseia o banco de dados para adicionar o bônus ao usuário
    s.post('http://localhost:5005/data_access', headers=headers, data=database_data)

    

    # Simular resposta bem-sucedida
    print(f"Request 4 (Fidelity): Sucesso - Bônus de usuário {user_id} agora totaliza {bonus_value}.")

    return jsonify({"Operation": "Success"}), 200

def activate_error():
    global failing
    failing = False
    print("Request 4 (Fidelity): Situação estabilizada.")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
