# App Renda Fixa - API Client

Guia completo de engenharia reversa de API e extração de dados de investimentos do site App Renda Fixa.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [O Cenário Prático](#o-cenário-prático)
- [Como Descobrir APIs Ocultas](#como-descobrir-apis-ocultas)
- [Reprodução no Postman](#reprodução-no-postman)
  - [Erros Comuns e Soluções](#erros-comuns-e-soluções)
- [Fundamentos Teóricos: API vs. Web Scraping](#fundamentos-teóricos-api-vs-web-scraping)
- [Segurança e Limites](#segurança-e-limites)
- [Instalação e Uso](#instalação-e-uso)
- [Estrutura dos Dados](#estrutura-dos-dados)
- [Exemplos de Uso](#exemplos-de-uso)

---

## Visão Geral

Este projeto demonstra como fazer **engenharia reversa de APIs** para extrair dados de investimentos (CDBs, taxas, prazos) do site **App Renda Fixa**. Diferente de web scraping tradicional, esta abordagem utiliza a API oculta do site, resultando em código mais simples, rápido e robusto.

**Endpoint descoberto:** `https://api2.apprendafixa.com.br/vn/get_featured_investments`

---

## O Cenário Prático

### O Objetivo

Extrair informações de investimentos (CDBs, taxas, prazos, corretoras) do site App Renda Fixa de forma automatizada.

### A Descoberta (Engenharia Reversa)

Ao inspecionar a rede (Network Tab) do navegador Chrome, identificamos que:

- O site **não renderiza os dados diretamente no HTML inicial**
- Os dados são buscados **dinamicamente** através de uma chamada de API (XHR/Fetch)
- O endpoint retorna JSON estruturado com todos os investimentos

**Endpoint identificado:**
- **URL:** `https://api2.apprendafixa.com.br/vn/get_featured_investments`
- **Método:** `POST`
- **Retorno:** JSON estruturado contendo lista de investimentos

---

## Como Descobrir APIs Ocultas

### Passo a Passo

1. Abra o **Developer Tools** (F12) no Chrome/Edge
2. Vá na aba **Network** (Rede)
3. Selecione o filtro **Fetch/XHR**
4. Navegue pelo site ou aplique um filtro na tela
5. Observe as requisições que aparecem
6. Clique nelas e olhe a aba **Preview** ou **Response**
7. Se vir um JSON com os dados que você quer, **achou a API!**

### Dicas

- Requisições com nomes descritivos como `get_investments`, `search`, `api`, etc., são bons candidatos
- Fique atento ao **método HTTP** (GET, POST, PUT, DELETE)
- Copie o **Request Payload** e os **Headers** para usar no seu código

---

## Reprodução no Postman

### Passo a Passo

1. **Importar a requisição:**
   - Abra o Postman
   - Copie a requisição do Network Tab (botão direito → Copy → Copy as cURL)
   - Importe no Postman (File → Import → Raw text)

2. **Ajustar o método:**
   - Certifique-se de que está usando **POST** (não GET)

3. **Configurar headers:**
   - Adicione `Content-Type: application/json`

4. **Configurar o body:**
   - Selecione **raw** e **JSON**
   - Cole o payload com sintaxe JSON válida


## ❓ Por que POST e não GET?

Durante a análise, você pode ter estranhado o fato de usarmos o método **POST** para buscar dados, já que, pela convenção do protocolo HTTP, o método **GET** é o padrão para leitura de informações e o **POST** para envio/criação.

**O motivo é a complexidade dos filtros.**

Esta API utiliza uma prática conhecida como **"Search via POST"** pelos seguintes motivos:

1.  **Limitação do GET (A "Carta Aberta"):**
    No método GET, todos os parâmetros precisam ser passados na URL (ex: `api.com?tipo=cdb&prazo=100`). Quando temos filtros complexos (listas de emissores, múltiplos indexadores, faixas de datas), a URL ficaria excessivamente longa, difícil de ler e poderia esbarrar no limite de caracteres dos navegadores/servidores.

2.  **Robustez do POST (O "Envelope Fechado"):**
    O método POST permite enviar os dados dentro do **Body (Corpo)** da requisição. Isso possibilita o envio de um objeto JSON estruturado, limpo e sem limite de tamanho, ideal para passar a configuração complexa que a API exige:

    ```json
    // No POST, podemos enviar estruturas complexas assim:
    {
      "tipo": ["cdb", "lci", "lca"],
      "indexador": ["ipca", "cdi"],
      "vencimento": { "min": 0, "max": 1800 }
    }
    ```

Em resumo: embora semanticamente seja uma "busca" (GET), tecnicamente o POST é mais eficiente para transportar o "pacote" de filtros que o site precisa.


### Erros Comuns e Soluções

#### Erro 1: 405 Method Not Allowed

**Causa:** O Postman estava tentando fazer uma requisição GET, mas o servidor exige POST.

**Solução:** Alterar o método no dropdown do Postman para **POST**.

#### Erro 2: 415 Unsupported Media Type

**Causa A (Header):** O servidor não sabia que estávamos enviando um JSON. Faltava o header `Content-Type: application/json`.

**Solução:** Adicionar o header `Content-Type: application/json`.

#### Erro 3: "JSON is not valid"

**Causa B (Sintaxe):** O JSON copiado do Chrome ("View Source" ou visualização simplificada) muitas vezes vem sem aspas nas chaves.

**Exemplo inválido:**
```json
{
  tipo: "cdb",
  idx: ["ipca"]
}
```

**Exemplo válido:**
```json
{
  "tipo": ["cdb"],
  "idx": ["ipca"]
}
```

**Solução:** Corrigir a sintaxe do JSON no Body (Raw), garantindo que todas as chaves e strings estejam entre aspas duplas.

### Payload Final (Exemplo)

Para filtrar CDBs indexados ao IPCA com prazo de 1800 dias:

```json
{
  "dc_ini": 1800,
  "dc_fim": 1800,
  "tipo": ["cdb"],
  "idx": ["ipca"],
  "corretora": [],
  "emissor": []
}
```

**Campos do payload:**
- `dc_ini`: Prazo mínimo em dias
- `dc_fim`: Prazo máximo em dias
- `tipo`: Array com tipos de investimento (ex: `["cdb"]`, `["lci", "lca"]`)
- `idx`: Array com índices (ex: `["ipca"]`, `["cdi"]`, `["pre"]`)
- `corretora`: Array com filtro de corretoras (vazio = todas)
- `emissor`: Array com filtro de emissores (vazio = todos)

---

## Fundamentos Teóricos: API vs. Web Scraping

### Consumir a API (O que fizemos)

**Analogia:** É como entrar no restaurante e pedir direto para a cozinha. Você recebe apenas a comida (os dados puros em JSON), sem o prato decorado.

**Vantagens:**
- ✅ Mais rápido
- ✅ Mais limpo
- ✅ Menos propenso a quebrar se o design do site mudar
- ✅ Dados já estruturados

**Ferramenta:** Python `requests`

**Quando usar:**
- Sempre verifique primeiro se existe uma API oculta
- É a "mina de ouro" para extração de dados
- Dados estruturados, fáceis de ler e processar

### Web Scraping (BeautifulSoup/Selenium)

**Analogia:** É como entrar no restaurante, esperar o prato chegar na mesa, e então separar a comida da decoração. Você baixa o HTML (o site visual) e tenta encontrar os dados no meio das tags `<div>`, `<span>`, etc.

**Desvantagens:**
- ❌ Mais lento
- ❌ Quebra facilmente se o HTML mudar
- ❌ Precisa processar HTML sujo
- ❌ Pode ser bloqueado por anti-bot

**Ferramentas:**
- **BeautifulSoup:** Para HTML estático
- **Selenium/Playwright:** Para simular navegador (JS dinâmico)

**Quando usar:**
- Apenas se o site for **estático** (SSR - Server Side Rendering)
- Quando os dados já vêm "colados" no HTML inicial
- Quando não há requisições XHR visíveis com os dados

---

## Segurança e Limites

### O "Muro" - Travas Comuns

As APIs nem sempre são abertas. Travas comuns incluem:

#### 1. Tokens de Autenticação
- O site pode exigir um token de autenticação que expira
- **Solução:** Extrair o token da sessão do navegador ou implementar autenticação

#### 2. User-Agent
- O site bloqueia requisições que se identificam como `python-requests`
- **Solução:** Copiar o User-Agent do navegador:
  ```python
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
  }
  ```

#### 3. Referer/Origin
- O site bloqueia chamadas que não vêm da URL original dele
- **Solução:** Adicionar headers de referência:
  ```python
  headers = {
      "Referer": "https://apprendafixa.com.br/",
      "Origin": "https://apprendafixa.com.br"
  }
  ```

#### 4. Rate Limiting
- Bloqueio se você fizer muitas requisições em pouco tempo
- **Solução:** Implementar delays entre requisições ou usar rate limiting

#### 5. WAF/Captcha (Cloudflare, etc.)
- Bloqueios avançados que exigem desafios visuais
- **Solução:** Bibliotecas simples como `requests` falham; use Selenium, Playwright ou serviços de quebra de captcha

---

## Instalação e Uso

### Pré-requisitos

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório ou navegue até o diretório:
   ```bash
   cd apprendafixa-api
   ```

2. Instale as dependências:
   ```bash
   uv sync
   ```

### Executando o Script

```bash
uv run python main.py
```

---

## Estrutura dos Dados

A API retorna uma **lista de dicionários**, onde cada dicionário representa um investimento.

### Exemplo de Estrutura

```json
{
  "_id": {"$oid": "6838b69e200f7a118efd06e7"},
  "emissor": "BANCO BMG",
  "corretora": "BMG Invest digital",
  "tipo": "CDB",
  "taxa": "IPCA +7.91%",
  "juros": 7.91,
  "idx": "IPCA",
  "vencimento": "1826 dias",
  "liquidez": "No vencimento",
  "preco": 50.0,
  "qtdMinima": 50.0,
  "rating": "B+",
  "agencia": "Fitch",
  "carencia": "1826 Dias dias",
  "tir": 15.0,
  "vir": 6.82,
  "dc": 1826,
  "du": 1254,
  ...
}
```

### Campos Principais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `emissor` | string | Nome do banco/instituição emissora |
| `corretora` | string | Nome da corretora |
| `tipo` | string | Tipo de investimento (CDB, LCI, LCA, etc.) |
| `taxa` | string | Taxa formatada (ex: "IPCA +7.91%") |
| `juros` | float | Valor numérico da taxa de juros |
| `idx` | string | Índice de referência (IPCA, CDI, PRE) |
| `vencimento` | string | Prazo de vencimento em dias |
| `liquidez` | string | Condições de liquidez |
| `preco` | float | Preço mínimo do investimento |
| `qtdMinima` | float | Quantidade mínima de investimento |
| `rating` | string | Rating de crédito |
| `agencia` | string | Agência de rating |
| `tir` | float | Taxa Interna de Retorno |
| `vir` | float | Valor Investido Recomendado |
| `dc` | int | Dias corridos |
| `du` | int | Dias úteis |

---

## Exemplos de Uso

### 1. Listar Todos os Investimentos

```python
import requests
import json

url = "https://api2.apprendafixa.com.br/vn/get_featured_investments"

payload = {
    "dc_ini": 1800,
    "dc_fim": 1800,
    "tipo": ["cdb"],
    "idx": ["ipca"],
    "corretora": [],
    "emissor": []
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    dados = response.json()
    print(f"Encontrados {len(dados)} investimentos.")
else:
    print("Erro:", response.status_code, response.text)
```

### 2. Iterar e Filtrar Investimentos

```python
# Iterar sobre todos os investimentos
for investimento in dados:
    print(f"{investimento['emissor']} - {investimento['taxa']}")

# Filtrar investimentos com altas taxas
altas_taxas = [inv for inv in dados if inv['juros'] > 7.0]
print(f"\nInvestimentos com taxa > 7%: {len(altas_taxas)}")

# Filtrar por corretora específica
inter = [inv for inv in dados if 'Inter' in inv['corretora']]
print(f"\nInvestimentos no Banco Inter: {len(inter)}")

# Filtrar por rating
ratings_altos = [inv for inv in dados if inv.get('rating', '').startswith('AAA')]
print(f"\nInvestimentos com rating AAA: {len(ratings_altos)}")
```

### 3. Ordenar Investimentos

```python
# Ordenar por taxa de juros (maior para menor)
investimentos_ordenados = sorted(dados, key=lambda x: x['juros'], reverse=True)

print("Top 5 investimentos com maior taxa:")
for i, inv in enumerate(investimentos_ordenados[:5], 1):
    print(f"{i}. {inv['emissor']} - {inv['taxa']} ({inv['corretora']})")
```

### 4. Exportar para CSV

```python
import csv

# Exportar para CSV
with open('investimentos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['emissor', 'corretora', 'tipo', 'taxa', 'juros', 'vencimento', 'rating']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for inv in dados:
        writer.writerow({k: inv.get(k, '') for k in fieldnames})

print("Dados exportados para investimentos.csv")
```

### 5. Análise Estatística

```python
import statistics

# Calcular estatísticas
taxas = [inv['juros'] for inv in dados]
media_taxa = statistics.mean(taxas)
mediana_taxa = statistics.median(taxas)
max_taxa = max(taxas)
min_taxa = min(taxas)

print(f"\n=== Estatísticas das Taxas ===")
print(f"Média: {media_taxa:.2f}%")
print(f"Mediana: {mediana_taxa:.2f}%")
print(f"Máxima: {max_taxa:.2f}%")
print(f"Mínima: {min_taxa:.2f}%")
```

---

## Notas Finais

### Boas Práticas

1. **Sempre verifique primeiro se existe API oculta** antes de recorrer ao scraping
2. **Respeite os limites** do servidor (rate limiting)
3. **Use headers apropriados** para evitar bloqueios
4. **Trate erros** adequadamente (timeouts, status codes, etc.)
5. **Cache resultados** quando possível para evitar requisições desnecessárias

### Contribuindo

Sinta-se à vontade para melhorar este projeto:
- Adicionar tratamento de erros mais robusto
- Implementar cache
- Adicionar mais exemplos de uso
- Melhorar a documentação

### Disclaimer

Este projeto é apenas para fins educacionais e demonstração de técnicas de engenharia reversa de APIs. Respeite os termos de uso do site App Renda Fixa e use os dados de forma responsável.

---

## Referências

- [Python Requests Documentation](https://requests.readthedocs.io/)
- [Chrome DevTools Network Tab](https://developer.chrome.com/docs/devtools/network/)
- [JSON Format Specification](https://www.json.org/)

---

**Última atualização:** Dezembro 2025

