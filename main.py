import requests
import json
import pandas as pd

data = requests.get('https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json')
json_data = json.loads(data.content)

candidate = []
party = []
votes = []
percentage = []
total = []

for percentual in json_data['cand']:

    if percentual['seq'] == '1' or percentual['seq'] == '2' or percentual['seq'] == '3' or percentual['seq'] == '4':
        candidate.append(percentual['nm'])
        votes.append(percentual['vap'])
        percentage.append(percentual['pvap'])

valid_votes = json_data['vv']
total_percentage = json_data['psi']

output_results = pd.DataFrame(list(zip(candidate, votes, percentage)),
                              columns=['Candidato', 'Votos', 'Porcentagem'])
print('\nVotos validos apurados: ', valid_votes, '\nPorcentagem de urnas apuradas: ', total_percentage, '%\n')
print(output_results)
