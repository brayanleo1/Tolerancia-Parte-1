from flask import Flask, request, jsonify
import random
import uuid
import threading

app = Flask(__name__)
failing = False

@app.route('/sell', methods=['POST'])
def request3():
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
    print(f"Request 3 (Store): Sucesso - Transação ID: {transaction_id}")
    return jsonify({"transaction_id": transaction_id}), 200

def activate_error():
    global failing
    failing = False
    print("Request 3 (Store): Falha temporária finalizada.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)