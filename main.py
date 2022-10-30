import json
import os
import time
from datetime import datetime
import pandas as pd
import requests

flag = 0
while True:
    if flag != 0:
        time.sleep(30)
        os.system('clear')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('Atualizado em: ', current_time)
    # data = requests.get('https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544
    # -r.json')

    data = requests.get('https://resultados.tse.jus.br/oficial/ele2022/545/dados-simplificados/br/br-c0001-e000545-r'
                        '.json')
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
            percentage_int.append(float(percentual['pvap'].replace(',', '').replace('%', '')) / 100)

    valid_votes = "{:,}".format(int(json_data['vv']))
    votes_to_win = "{:,}".format(int((int(json_data['vv']) / 2) + 1))
    votes_to_candidate_win = int((int(json_data['vv']) / 2) + 1) - votes_int[0]
    total_percentage = json_data['psi'] + '%'

    output_results = pd.DataFrame(list(zip(candidate, votes, percentage)),
                                  columns=['Candidato', 'Votos', 'Porcentagem'])

    print('\nVotos validos apurados: ', valid_votes,
          '\nPorcentagem de urnas apuradas: ', total_percentage, '\n')
    print('Diferença de votos entre ' + candidate[0] + ' e ' + candidate[1] + ': ', ("{:,}".format(votes_int[0] - votes_int[1])))
    print('Diferença de porcentagem entre ' + candidate[0] + ' e ' + candidate[1] + ': ',
          ("{0:.2f}".format(percentage_int[0] - percentage_int[1])) + '\n')
    print('Votos necessários para vencer: ', votes_to_win)
    print('Votos necessários para primeiro colocado vencer: ', "{:,}".format(votes_to_candidate_win), '\n')
    print(output_results)
    total_percentage_int = float(json_data['psi'].replace(',', '').replace('%', '')) / 100
    if total_percentage_int > 99.98:
        break
    print('\nPor favor espere 30 segundos ate atualizar!')
    flag = 1
