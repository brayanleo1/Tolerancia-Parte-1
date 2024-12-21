from flask import Flask, request, jsonify
import random
import threading
import uuid
import time

failing = False

app = Flask(__name__)

@app.route('/bonus', methods=['POST'])
def request4():
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
    user_id = data["user_id"]


    #Manuseia o banco de dados para adicionar o bônus ao usuário

    # Simular resposta bem-sucedida
    print(f"Request 4 (Fidelity): Sucesso - Bônus de {bonus_value} concedido ao usuário {user_id}.")
    return jsonify({"Operation": "Success"}), 200

def activate_error():
    global failing
    failing = False
    print("Request 4 (Fidelity): Situação estabilizada.")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
