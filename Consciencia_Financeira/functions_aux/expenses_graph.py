import os
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('agg')

def expensesGraph(user_id, query_filter, filter_day = None, filter_month = None, filter_year = None):
    expenses_type = {}
    
    if user_id is None:
        return None

    for expense in query_filter:
        expenses_type[expenses_type] = expense[1] 

    types = list(expenses_type.keys())
    values = list(expenses_type.values())

    # Defina um esquema de cores e legendas
    colors = ['#8B0000', '#B22222', '#FF0000', '#DC143C', '#FF6347', '#FF4500', '#FF7F7F', '#F08080', '#FA8072', '#E9967A']
    label = dict(zip(types, colors))  # Associa cada tipo de despesa a uma cor

    # Gera a lista de cores para os tipos
    colors = [label.get(type, '#CCCCCC') for type in types]

    plt.figure(figsize=(8, 4))  # Ajuste o tamanho para deixar espaço para a legenda
    plt.bar(types, values, color=colors)
    plt.ylabel('Valor Total')
    
    # Adiciona o título ao gráfico com base nos filtros
    if filter_day == '' and filter_month != '' and filter_year != '':
        plt.title(f'Total de despesas por tipo do mês de: {filter_month} / {filter_year}')
    elif filter_day != '' and filter_month != '' and filter_year != '':
        plt.title(f'Total de despesas por tipo do dia {filter_day} / {filter_month} / {filter_year}')
    elif filter_day == '' and filter_month == '' and filter_year != '':
        plt.title(f'Total de despesas por tipo do ano de {filter_year}')
    plt.xticks([])  # Remove os rótulos do eixo x
    plt.tight_layout()

    # Adiciona a legenda ao lado do gráfico
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in label.values()]
    labels = label.keys()
    plt.legend(handles, labels, title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')

    file_path = os.path.join('static', 'expenses_graph.png')
    plt.savefig(file_path, bbox_inches='tight')  # Ajusta o layout para incluir a legenda
    plt.close('all')
    plt.clf()
    plt.cla()

    return file_path
