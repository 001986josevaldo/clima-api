from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/clima')
def clima():
    cep = request.args.get('cep')
    return jsonify({"mensagem": f"Consulta de clima para o CEP {cep}"})

if __name__ == '__main__':
    app.run()