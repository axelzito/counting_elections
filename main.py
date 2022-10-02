import requests
import json
import pandas as pd

data = requests.get('https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json')
json_data = json.loads(data.content)

candidate = []
party = []
votes = []
votes_int = []
percentage = []
percentage_int = []

for percentual in json_data['cand']:

    if percentual['seq'] == '1' or percentual['seq'] == '2' or percentual['seq'] == '3' or percentual['seq'] == '4':
        candidate.append(percentual['nm'])
        votes.append("{:,}".format(int(percentual['vap'])))
        votes_int.append(int(percentual['vap']))
        percentage.append(percentual['pvap'] + '%')
        percentage_int.append(float(percentual['pvap'].replace(',', '').replace('%', ''))/100)

valid_votes = "{:,}".format(int(json_data['vv']))
total_percentage = json_data['psi'] + '%'

output_results = pd.DataFrame(list(zip(candidate, votes, percentage)),
                              columns=['Candidato', 'Votos', 'Porcentagem'])

print('\nVotos validos apurados: ', valid_votes,
      '\nPorcentagem de urnas apuradas: ', total_percentage, '\n')
print('Diferença de votos entre Lula e Bolsonaro: ', ("{:,}".format(votes_int[0] - votes_int[1])))
print('Diferença de porcentagem entre Lula e Bolsonaro: ', ("{0:.2f}".format(percentage_int[0] - percentage_int[1])) + '\n')
print(output_results)
