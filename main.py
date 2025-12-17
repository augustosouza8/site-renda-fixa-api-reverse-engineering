import requests
import json

url = "https://api2.apprendafixa.com.br/vn/get_featured_investments"

payload = json.dumps({
  "dc_ini": 1800,
  "dc_fim": 1800,
  "tipo": [
    "cdb"
  ],
  "idx": [
    "ipca"
  ],
  "corretora": [],
  "emissor": []
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

# Parse do JSON para dicionário/listas Python
dados = response.json()

# Informações sobre a estrutura dos dados
print(f"Tipo dos dados: {type(dados)}")
print(f"Quantidade de investimentos: {len(dados)}")

# Exibir o primeiro investimento como exemplo formatado
if dados:
    print("\n=== Primeiro investimento (exemplo) ===")
    print(json.dumps(dados[0], indent=2, ensure_ascii=False))

# Dados completos disponíveis como lista de dicionários
# Agora você pode trabalhar facilmente com: dados[0], dados[1], etc.
# ou iterar: for investimento in dados: ...


# Iterar sobre todos os investimentos
for investimento in dados:
    print(investimento['emissor'], investimento['taxa'])

# Filtrar investimentos
altas_taxas = [inv for inv in dados if inv['juros'] > 7.0]

# E muito mais!
