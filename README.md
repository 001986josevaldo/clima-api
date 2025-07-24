# ☁️ Clima por CEP - Back-end (API Flask)

Este é o back-end da aplicação **Clima por CEP**, responsável por receber o CEP enviado via GET, consultar a API do ViaCEP e retornar os dados de endereço (logradouro, cidade, UF, etc).

## 🔗 URL do back-end (hospedado no Railway)

👉 https://web-production-893a.up.railway.app/clima?cep=SEU_CEP_AQUI

## 🚀 Tecnologias utilizadas

- **Python 3.12**
- **Flask**
- **Flask-CORS**
- **Requests**
- **Gunicorn**
- **Railway** (para hospedagem gratuita)

## 📦 Endpoints

### `GET /clima?cep=XXXXX-XXX`

- Parâmetro: `cep` (obrigatório)
- Retorna:
```json
{
  "cep": "78735-816",
  "logradouro": "Rua Santa Luzia",
  "bairro": "Parque São Jorge",
  "cidade": "Rondonópolis",
  "uf": "MT",
  "ddd": "66",
  "ibge": "5107602",
  "siafi": "9151"
}