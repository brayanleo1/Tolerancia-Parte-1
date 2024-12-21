from flask import Flask, request, jsonify
import random
import time
import uuid

app = Flask(__name__)

@app.route('/product', methods=['GET'])
def request1():
    # Simular falha de omissão com 20% de probabilidade
    if random.random() < 0.2:
        print("Request 1 (Store): Falha de omissão simulada.")
    else:
        data = request.get_json()
        product_id = data["product_id"]

        # Simular resposta bem-sucedida
        product = {"id": product_id, "name": "Produto X", "value": 100.0}
        print(f"Request 1 (Store): Sucesso - {product}")
        return jsonify(product), 200
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
