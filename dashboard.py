# Pandas é uma biblioteca para manipulação e análise de dados.
import pandas as pd
import dash  # Dash é uma biblioteca que permite criar aplicativos web interativos e analíticos em Python
# 'html'- módulo específico da biblioteca Dash, que fornece componentes HTML.
from dash import html
# 'dcc'- fornece componentes mais avançados e interativos, como gráficos interativos, botões, menus suspensos, caixas de seleção e muito mais.
from dash import dcc
from dash.dependencies import Input, Output

# Leitura dos dados do arquivo Excel
df = pd.read_excel('dados.xlsx')
tipos_licenca = df.columns[1:]
centros_custo = df['Centro de Custo'].unique()

# Cores para a página
cor_de_fundo = '#E6E6FA'       # Cor de fundo Azul claro
cor_principal_amarelo = '#7B68EE'      # Azul
cor_principal_branco = '#000000'      # Preto
cor_secundaria = '#7B68EE'     # Azul
cor_fonte = '#000000'          # Preto
cor_rodape = '#000000'         # Preto

# Estilos CSS personalizados
styles = {
    'font-family': 'Arial, sans-serif',
    'font-size': '20px',
    'margin': '5px',
    'padding': '10px',
    'color': cor_rodape,
    'border-radius': '10px',
    # Adicionando sombra para destacar o dashboard
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
}

# Estilos CSS personalizados
styles_resultados = {
    'font-family': 'Arial, sans-serif',
    'font-size': '20px',
    'margin': '5px',
    'padding': '10px',
    'color': cor_fonte,
    'border-radius': '10px',
    # Adicionando sombra para destacar o dashboard
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
}

# Estilos CSS para o título amarelo
titulo_styles_amarelo = {
    'text-align': 'center',
    'font-size': '45px',
    'font-family': 'Arial, sans-serif',
    'color': cor_principal_amarelo,
    'margin-top': '30px',  # Adicionando espaço entre o título e os dropdowns
}

# Estilos CSS para o título branco
titulo_styles_branco = {
    'text-align': 'center',
    'font-size': '45px',
    'font-family': 'Arial, sans-serif',
    'color': cor_principal_branco,
    'margin-top': '30px',  # Adicionando espaço entre o título e os dropdowns
}

# Estilos CSS para o rodapé
rodape_styles = {
    'position': 'absolute',
    'bottom': '20px',
    'left': '50%',
    'transform': 'translateX(-50%)',
    'font-size': '18px',
    'font-family': 'Arial, sans-serif',
    'color': cor_rodape,
}

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div(
    style={'background-color': cor_de_fundo, 'min-height': '100vh'},
    children=[
        html.Div(
            style={'display': 'flex', 'justify-content': 'center',
                   'align-items': 'center'},
            children=[
                html.H1("Ferra'z", style=titulo_styles_amarelo,),
                html.H1(".", style=titulo_styles_amarelo,),
                html.H1("Dash.365", style=titulo_styles_branco,),
            ]
        ),

        dcc.Dropdown(
            id='tipo-licenca-dropdown',
            options=[{'label': licenca, 'value': licenca}
                     for licenca in tipos_licenca],
            value=tipos_licenca[0],
            style=styles
        ),

        dcc.Dropdown(
            id='centro-custo-dropdown',
            options=[{'label': centro, 'value': centro}
                     for centro in centros_custo],
            value=centros_custo[0],
            style=styles
        ),

        html.Div(id='detalhes-licencas', style=styles),
    ]
)

# Callback para atualizar a tabela com base nas seleções do usuário


@app.callback(
    Output('detalhes-licencas', 'children'),
    [Input('tipo-licenca-dropdown', 'value'),
     Input('centro-custo-dropdown', 'value')]
)
def update_table(tipo_licenca, centro_custo):
    filtered_df = df[(df['Centro de Custo'] == centro_custo)
                     & (df[tipo_licenca] > 0)]

    if filtered_df.empty:
        return html.Table([
            html.Thead(html.Tr([html.Th("Centro de Custo"), html.Th(
                "Quantidade Usada", style={'text-align': 'center'})])),
            html.Tbody(
                html.Tr([html.Td(centro_custo), html.Td(0, style={'text-align': 'center'})]))
        ], style=styles_resultados)

    tabela = html.Table([
        html.Thead(
            html.Tr([html.Th("Centro de Custo"), html.Th(
                "Quantidade Usada", style={'text-align': 'center'})])
        ),
        html.Tbody([
            html.Tr([html.Td(filtered_df.iloc[i]['Centro de Custo']), html.Td(
                filtered_df.iloc[i][tipo_licenca], style={'text-align': 'center'})])
            for i in range(filtered_df.shape[0])
        ])
    ], style=styles_resultados)

    return tabela


# Execução do aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)
