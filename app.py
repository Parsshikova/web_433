from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route('/name', methods=['POST'])
def get_name():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Поле "name" обязательно'}), 400

    name = data['name']
    return jsonify({
        'message': f'Привет, {name}!',
        'name': name
    }), 200



@app.route('/sum', methods=['POST'])
def get_sum():
    data = request.get_json()

    if not data or 'a' not in data or 'b' not in data:
        return jsonify({'error': 'Поля "a" и "b" обязательны'}), 400

    try:
        a = float(data['a'])
        b = float(data['b'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Поля "a" и "b" должны быть числами'}), 400

    result = a + b
    if result.is_integer():
        result = int(result)

    return jsonify({
        'a': a,
        'b': b,
        'sum': result
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)