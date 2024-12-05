from django.shortcuts import render
from itertools import combinations
import requests

def gerar(quantidade, dezenas):
    # Converte as dezenas em inteiros
    numeros = list(map(int, dezenas.split(',')))

    # Gera as combinações
    combinacoes_resultado = list(combinations(numeros, quantidade))
    
    # Formata cada número nas combinações para ter dois dígitos
    combinacoes_formatadas = [
        tuple(str(num).zfill(2) for num in combinacao)  # Aplica zfill(2) em cada número da combinação
        for combinacao in combinacoes_resultado
    ]
    
    return combinacoes_formatadas

def buscar_resultados_megasena():
    url = "https://loteriascaixa-api.herokuapp.com/api/megasena"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.exceptions.RequestException:
        return []
    
def gerar_combinacoes(request):
    combinacoes_resultado = []
    combinacoes_sorteadas = []
    
    quantidade = None
    dezenas = ''
    data=None
    concurso=''
    resultados_megasena = buscar_resultados_megasena()
    
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade'))
        dezenas = request.POST.get('dezenas').zfill(2)
        print(dezenas)
    if dezenas:
        combinacoes_resultado = gerar(6, dezenas)
        
        # Dicionário para armazenar as datas dos sorteios para cada combinação
        combinacoes_datas = {}

        for combinacao in combinacoes_resultado:
            # Converte a combinação para um conjunto de strings
            teste = set(map(str, combinacao))
            teste_ordenadas = sorted(teste)
            print(f'Combinacao: {teste_ordenadas}')
            
            # Inicializa a lista de datas para essa combinação
            combinacoes_datas[tuple(teste_ordenadas)] = []

            for r in resultados_megasena:
                # Converte as dezenas sorteadas para um conjunto de strings
                dezenas_sorteadas = set(r["dezenas"])
                data = r["data"]
                concurso = r["concurso"]
                dezenas_ordenadas = sorted(dezenas_sorteadas)
                
                # Verifica se todos os elementos da combinação estão nas dezenas sorteadas
                #if teste == teste.intersection(dezenas_sorteadas):
                intersecao = teste.intersection(dezenas_sorteadas)
                if len(intersecao) >= quantidade:    
                    print(f'Combinação encontrada! Dezenas sorteadas: {dezenas_ordenadas} na data: {data}, sorteio: {concurso}')
                    print(f'Números em comum: {sorted(intersecao)}')
                    
        combinacoes_sorteadas = [
            combinacao
            for combinacao in combinacoes_resultado
            if any(
                len(set(map(str, combinacao)).intersection(set(r["dezenas"]))) >= quantidade
                for r in resultados_megasena
                
            )
        ]

    context = {
        'quantidade': quantidade,
        'dezenas': dezenas,
        'combinacoes_resultado': combinacoes_resultado,
        'combinacoes_sorteadas': combinacoes_sorteadas,
        'intervalo_quantidades': range(1, 11),
        'data': data,
        'concurso': concurso,
    }
    
    return render(request, 'megasena/combinacoes.html', context)
