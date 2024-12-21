from flask import Flask, request, jsonify
import random
import signal
import os
app = Flask(__name__)

@app.route('/exchange', methods=['GET'])
def request2():
    # Simular falha de crash com 10% de probabilidade
    if random.random() < 0.1:
        print("Request 2 (Exchange): Falha de crash simulada. Serviço indisponível.")
        # Forçar a interrupção do programa rodando
        #raise RuntimeError("Simulated crash")
        return os.kill(os.getpid(), signal.SIGINT)
        

    # Simular resposta bem-sucedida
    exchange_rate = round(random.uniform(4.5, 5.5), 2)  # Exemplo de taxa de conversão
    print(f"Request 2 (Exchange): Sucesso - Taxa de conversão: {exchange_rate}")
    return jsonify({"exchange_rate": exchange_rate})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
