import datetime
import requests


def cotar():
  hoje = datetime.date.today()
  cotacoes_compra = []

  # Cria a sequência de 365 dias voltando a partir de hoje
  for i in range(365):
    data_atual = hoje - datetime.timedelta(days=i)
    # A API do Banco Central exige o formato MM-DD-YYYY
    data_formatada = data_atual.strftime("%m-%d-%Y")

    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data_formatada}'&$format=json"
    )

    try:
      resposta = requests.get(url)
      if resposta.status_code == 200:
        dados = resposta.json()
        # Se for dia útil, a API retorna o valor da cotação
        if dados.get("value"):
          valor = dados["value"][0]["cotacaoCompra"]
          cotacoes_compra.append(float(valor))
    except Exception:
      # Ignora fins de semana ou feriados onde o mercado está fechado
      continue

  return cotacoes_compra