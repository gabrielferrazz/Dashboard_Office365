import pandas as pd # Pandas é uma biblioteca para manipulação e análise de dados.
import dash # Dash é uma biblioteca que permite criar aplicativos web interativos e analíticos em Python
from dash import html # 'html'- módulo específico da biblioteca Dash, que fornece componentes HTML.
from dash import dcc # 'dcc'- fornece componentes mais avançados e interativos, como gráficos interativos, botões, menus suspensos, caixas de seleção e muito mais. 
from dash.dependencies import Input, Output

# Leitura dos dados do arquivo Excel
df = pd.read_excel('dados.xlsx')
tipos_licenca = df.columns[1:]
centros_custo = df['Centro de Custo'].unique()

# Cores para a página
cor_de_fundo = '#F0F0F0'       # Cor de fundo mais clara
cor_principal = '#3366CC'      # Azul
cor_secundaria = '#FFA500'     # Laranja
cor_fonte = '#333333'          # Preto

# Estilos CSS personalizados
styles = {
    'font-family': 'Arial, sans-serif',
    'font-size': '20px',
    'margin': '5px',
    'padding': '10px',
    'color': cor_fonte,
    'border-radius': '10px',
    'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)',  # Adicionando sombra para destacar o dashboard
}

# Estilos CSS para o título
titulo_styles = {
    'text-align': 'center',
    'font-size': '50px',
    'font-family': 'Arial, sans-serif',
    'color': cor_principal,
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
    'color': cor_fonte,
}

# Inicialização do aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div(
    style={'background-color': cor_de_fundo, 'min-height': '100vh'},
    children=[
        html.H1("Dashboard de Licenças", style=titulo_styles),
        
        dcc.Dropdown(
            id='tipo-licenca-dropdown',
            options=[{'label': licenca, 'value': licenca} for licenca in tipos_licenca],
            value=tipos_licenca[0],
            style=styles
        ),

        dcc.Dropdown(
            id='centro-custo-dropdown',
            options=[{'label': centro, 'value': centro} for centro in centros_custo],
            value=centros_custo[0],
            style=styles
        ),

        html.Div(id='detalhes-licencas', style=styles)
    ]
)

# Callback para atualizar a tabela com base nas seleções do usuário
@app.callback(
    Output('detalhes-licencas', 'children'),
    [Input('tipo-licenca-dropdown', 'value'),
     Input('centro-custo-dropdown', 'value')]
)
def update_table(tipo_licenca, centro_custo):
    filtered_df = df[(df['Centro de Custo'] == centro_custo) & (df[tipo_licenca] > 0)]

    if filtered_df.empty:
        return html.Table([
            html.Thead(html.Tr([html.Th("Centro de Custo"), html.Th("Quantidade Usada", style={'text-align': 'center'})])),
            html.Tbody(html.Tr([html.Td(centro_custo), html.Td(0, style={'text-align': 'center'})]))
        ], style=styles)

    tabela = html.Table([
        html.Thead(
            html.Tr([html.Th("Centro de Custo"), html.Th("Quantidade Usada", style={'text-align': 'center'})])
        ),
        html.Tbody([
            html.Tr([html.Td(filtered_df.iloc[i]['Centro de Custo']), html.Td(filtered_df.iloc[i][tipo_licenca], style={'text-align': 'center'})]) 
            for i in range(filtered_df.shape[0])
        ])
    ], style=styles)

    return tabela

# Execução do aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)