
# para executar
# python3.10 app.py



from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clima')
def clima_por_cep():
    cep = request.args.get('cep')
    if cep:
        cep = cep.replace("-", "").strip()
    if not cep:
        return jsonify({"erro": "CEP não informado"}), 400

    try:
        # Etapa 1: Endereço via ViaCEP
        res_cep = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        endereco = res_cep.json()
        logradouro = endereco.get("logradouro", "")
        cidade = endereco["localidade"]
        estado = endereco["uf"]

        # Etapa 2: Coordenadas via Nominatim
        query = f"{logradouro}, {cidade}, {estado}, Brasil"
        res_geo = requests.get("https://nominatim.openstreetmap.org/search", params={
            "q": query,
            "format": "json"
        }, headers={"User-Agent": "Mozilla/5.0"})
        local = res_geo.json()[0]
        lat, lon = local["lat"], local["lon"]
        #print(local)
        altitude = "indisponível"
        try:
            res_elev = requests.get("https://api.open-elevation.com/api/v1/lookup", params={
                "locations": f"{lat},{lon}"
            })
            if res_elev.status_code == 200:
                altitude = res_elev.json()["results"][0]["elevation"]
        except Exception as e:
            print(f"Erro ao obter altitude: {e}")

        print("Altitude: ",altitude)

        # Etapa 3: WeatherAPI
        clima_url = "http://api.weatherapi.com/v1/current.json"
        api_key = os.getenv("WEATHER_API_KEY")
        parametros = {
            "key": api_key,
            "q": f"{lat},{lon}",
            "lang": "pt"
        }

        resposta = requests.get(clima_url, params=parametros)
        if resposta.status_code != 200:
            return jsonify({"erro": "Erro na WeatherAPI"}), 500

        dados = resposta.json()
        #print(dados)
        resultado = {
            "local": f"{logradouro} - {cidade} - {dados['location']['region']} - {dados['location']['country']}",
            "temperatura": dados["current"]["temp_c"],
            "condicao": dados["current"]["condition"]["text"],
            "humidade": dados["current"]["humidity"],
            "pressao": dados["current"]["pressure_mb"],
            "vento": dados["current"]["wind_kph"],
            "direcao_vento": f"{dados['current']['wind_degree']}° ({dados['current']['wind_dir']})",
            "data_hora": dados["location"]["localtime"],
            "altitude": altitude
        }

        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({"erro": "Erro no processamento", "detalhes": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
