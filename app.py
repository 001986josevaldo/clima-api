from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# para executar
# python3.10 app.py

app = Flask(__name__)



@app.route('/clima')
def clima_por_cep():
    cep = request.args.get('cep')
    print("CEP recebido:", cep)

    if not cep:
        return jsonify({"erro": "CEP não informado"}), 400

    cep = cep.replace("-", "").strip()

    try:
        # Etapa 1: Buscar endereço no ViaCEP
        res_cep = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        print("Resposta do ViaCEP:", res_cep.text)

        if res_cep.status_code != 200:
            return jsonify({"erro": "Erro ao buscar CEP"}), 500

        endereco = res_cep.json()
        if "erro" in endereco:
            return jsonify({"erro": "CEP inválido"}), 400

        logradouro = endereco.get("logradouro", "")
        cidade = endereco.get("localidade", "")
        estado = endereco.get("uf", "")

        # Etapa 2: Obter coordenadas via LocationIQ
        query = f"{logradouro}, {cidade}, {estado}, Brasil"
        print("Query LocationIQ:", query)

        locationiq_token = os.getenv("LOCATIONIQ_KEY")
        if not locationiq_token:
            return jsonify({"erro": "LOCATIONIQ_KEY ausente nas variáveis de ambiente"}), 500

        res_geo = requests.get("https://us1.locationiq.com/v1/search.php", params={
            "key": locationiq_token,
            "q": query,
            "format": "json"
        })

        print("Resposta do LocationIQ:", res_geo.text)

        geo_data = res_geo.json()
        if not geo_data or not isinstance(geo_data, list):
            return jsonify({"erro": "Coordenadas não encontradas"}), 404

        local = geo_data[0]
        lat, lon = local["lat"], local["lon"]

        # Etapa 3: Altitude
        altitude = "indisponível"
        try:
            res_elev = requests.get("https://api.open-elevation.com/api/v1/lookup", params={
                "locations": f"{lat},{lon}"
            })
            if res_elev.status_code == 200:
                altitude = res_elev.json()["results"][0]["elevation"]
        except Exception as e:
            print(f"Erro ao obter altitude: {e}")

        print("Altitude:", altitude)

        # Etapa 4: Clima via WeatherAPI
        clima_url = "http://api.weatherapi.com/v1/current.json"
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return jsonify({"erro": "WEATHER_API_KEY ausente nas variáveis de ambiente"}), 500

        parametros = {
            "key": api_key,
            "q": f"{lat},{lon}",
            "lang": "pt"
        }

        resposta = requests.get(clima_url, params=parametros)
        if resposta.status_code != 200:
            return jsonify({"erro": "Erro na WeatherAPI"}), 500

        dados = resposta.json()
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
        print("Erro inesperado:", str(e))
        return jsonify({"erro": "Erro no processamento", "detalhes": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)