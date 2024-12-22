from flask import Flask, request, jsonify

app = Flask(__name__)

#products will have a product_id, name and value
products = [
    {"product_id": 1, "name": "laptop", "value": 1000},
    {"product_id": 2, "name": "mouse", "value": 20},
    {"product_id": 3, "name": "keyboard", "value": 50}
    ] #Initialize with values

#users will have user_id and bonus
users = [
    {"user_id": 1, "bonus": 100},
    {"user_id": 2, "bonus": 50},
    {"user_id": 3, "bonus": 200}
    ] #Initialize with values

#transactions will have transaction_id and product_id
transactions = [
    {"transaction_id": 1, "product_id": 1},
    {"transaction_id": 2, "product_id": 2},
    {"transaction_id": 3, "product_id": 3}
    ] #Initialize with values

@app.route('/data_access', methods=['POST'])
def handle_request():
    global products
    global users
    global transactions
    data = request.get_json()
    #data will have the command, the table and the value_1, value_2 or value_3
    if data['command'] == 'select':
        if data['table'] == 'products':
            #If the user wants to select the products table, return the products
            if data['value_1'] == 'all':
                return jsonify(products)
            #If the user wants to select a specific product, return the product by product_id
            else:
                for product in products:
                    if product['product_id'] == data['value_1']:
                        return jsonify(product)
        elif data['table'] == 'users':
            if data['value_1'] == 'all':
                return jsonify(users)
            else:
                for user in users:
                    if user['user_id'] == data['value_1']:
                        return jsonify(user)
        elif data['table'] == 'transactions':
            if data['value_1'] == 'all':
                return jsonify(transactions)
            else:
                for transaction in transactions:
                    if transaction['transaction_id'] == data['value_1']:
                        return jsonify(transaction)
        

    elif data['command'] == 'insert':
        if data['table'] == 'products':
            #If the user wants to insert a product, append the product to the products list
            products.append(data['value_1'], data['value_2'], data['value_3'])
            return jsonify({"message": "Product inserted"})
        elif data['table'] == 'users':
            users.append(data['value_1'], data['value_2'])
            return jsonify({"message": "User inserted"})
        elif data['table'] == 'transactions':
            transactions.append(data['value_1'], data['value_2'])
            return jsonify({"message": "Transaction inserted"})
        
    elif data['command'] == 'update':
        if data['table'] == 'products':
            #If the user wants to update a product, update the product by product_id
            for product in products:
                if product['product_id'] == data['value_1']:
                    product['name'] = data['value_2']
                    product['value'] = data['value_3']
                    return jsonify({"message": "Product updated"})
        elif data['table'] == 'users':
            for user in users:
                if user['user_id'] == data['value_1']:
                    user['bonus'] = data['value_2']
                    return jsonify({"message": "User updated"})
        elif data['table'] == 'transactions':
            for transaction in transactions:
                if transaction['transaction_id'] == data['value_1']:
                    transaction['product_id'] = data['value_2']
                    return jsonify({"message": "Transaction updated"})
        
    return jsonify({"message": "Invalid command"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)