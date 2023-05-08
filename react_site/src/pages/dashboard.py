import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import os

import pandas as pd
import plotly.express as px

from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash

app = Dash(__name__)

athlete_Event_Results = pd.read_csv('Dataset/Olympic_Athlete_Event_Results.csv', sep=',')
athlete_Event_Results = athlete_Event_Results.replace(["na"], None)

athlete_results = athlete_Event_Results[athlete_Event_Results["edition"].str.contains("Winter") == False]   # apenas jogos de verao


athlete_results = athlete_results[athlete_results["country_noc"].str.contains("MIX")==False] # Impossivel dividir
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("EUN")==False] # Impossivel dividir
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("IOA")==False] # Impossivel dividir
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("BOH")==False]    # Eslováquia + Republica Checa
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("ANZ")==False]    # Australia + Nova Zelandia + Nova Guine + partes da Indonesia
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("TCH")==False]    # Eslováquia + Republica Checa
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("YUG")==False] # Bosnia + Croacia + Macedonia + Montenegro + Eslovenia + Servia
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("URS")==False] # Russia + Letonia + Lituania + Estonia + Georgia + Armenia + Azerbaijao + Bielorrussia + Cazaquistao + Moldavia + Quirguistao + Tajiquistao + Turquemenistao + Ucrania + Usbequistao
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("UAR")==False]  # Egypt + Syria + Faixa de Gaza
athlete_results = athlete_results[athlete_results["country_noc"].str.contains("WIF")==False] # Antigua + Barbados + Cayman Islands + Dominica + Grenada + Jamaica + Montserrat + St Christopher-Nevis-Anguilla + Saint Lucia	+ St Vincent and the Grenadines	+ Trinidad and Tobago + Turks and Caicos Islands	

athlete_results['country_noc'] = athlete_results['country_noc'].replace(['FRG'], 'GER')
athlete_results['country_noc'] = athlete_results['country_noc'].replace(['GDR'], 'GER')

athlete_results['country_noc'] = athlete_results['country_noc'].replace(['HKG'], 'CHN')

athlete_results['country_noc'] = athlete_results['country_noc'].replace(['ROC'], 'RUS')



athlete_results = athlete_results.reset_index()

athlete_results = athlete_results.drop(columns=['result_id','athlete','athlete_id','pos', 'index'])

athlete_results['edition'] = athlete_results['edition'].str.split().str[0].astype(int)

repeat = []
i=0
while(i < len(athlete_results)):
    if athlete_results.loc[i, 'isTeamSport'] == True:
        auxi = i + 1 
        p = athlete_results.loc[i, 'country_noc']
        e = athlete_results.loc[i, 'event']
        a = athlete_results.loc[i, 'edition_id']
        while((athlete_results.loc[auxi, 'country_noc'] == p) and (athlete_results.loc[auxi, 'event'] == e) and (athlete_results.loc[auxi, 'edition_id'] == a)):
            repeat.append(auxi)
            auxi += 1
        i = auxi-1
    i+=1

athlete_results.drop(repeat, inplace=True)

athlete_aux = athlete_results.copy()

athlete_results['medal'] = athlete_results['medal'].replace([None], 0)
athlete_results['medal'] = athlete_results['medal'].replace(['Gold'], 1)
athlete_results['medal'] = athlete_results['medal'].replace(['Silver'], 1)
athlete_results['medal'] = athlete_results['medal'].replace(['Bronze'], 1)

athlete_results = athlete_results.drop(columns=['edition_id','sport','event','isTeamSport'])

medals = pd.DataFrame(athlete_results.groupby(['country_noc']).sum()).reset_index().sort_values(by=['medal'], ascending=False).head(10)

athlete_aux = athlete_aux[athlete_aux['country_noc'].isin(medals['country_noc'])]

medals = pd.DataFrame(athlete_aux.groupby(['country_noc' , 'medal']).count()).reset_index()
medals.drop(columns=['edition_id','sport','event','isTeamSport'], inplace=True)
medals.rename(columns={'edition': 'count', 'country_noc': 'country'}, inplace=True)

colors = ['#D6AF36', '#A7A7AD', '#A77044']
colors = {
    'background': '#EEF1FA'
}
text = {
    'font_family': 'Cabin'
}

fig = px.bar(medals, x="country", y="count", color='medal', 
             color_discrete_map={
                'Gold': '#D6AF36',
                'Silver': '#A7A7AD',
                'Bronze': '#A77044'}, width=300, height=600).update_xaxes(categoryorder="total descending").update_layout(font_family= 'Cabin', margin={'t':5, 'b':5, 'r': 3, 'l': 3})


dash.register_page(__name__, path='/dashboard')

layout = html.Div(
    [
	    
        html.Div([
                ], 
                    style = {'position': 'absolute', 'width': '72vw','height': '88vh', 'left': '26vw', 'top': '11vh', 'background': '#EEF1FA', 'borderRadius': '14vh 0vh 0vh 14vh'}),
		html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                dcc.Link(
                                    f"{'By country'}", href=page["relative_path"]
                                ), style={'position': 'absolute', 'width': '10vw', 'height':'6.5vh', 'left': '2vw', 'top':'-0.9vh',
                                        'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontWeight': '500', 'fontSize': '2.6vh',
                                        'lineHeight': '1.89vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing': '0.05em'}
                            )
                            for page in dash.page_registry.values()
                            if page["path"] == "/by_country"
                        ], style= {'position': 'absolute', 'width': '10vw', 'height': '5vh', 'left': '70vw', 'top': '3vh',
                                    'background': '#FFFFFF', 'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'borderRadius': '7px'}
				    ), 
				    #html.Img(src='/assets/round-chevron-right.svg')    
                      
                ]
        ),
	
        html.Div([
                html.H1('Jogos Olímpicos à Lupa', style={'position': 'absolute', 'width': '30vw', 'height': '3.22vh', 'left': '4vw', 'top': '1vh',
                            'fontFamily': 'Cabin', 'fontStyle': 'normal', 'fontSize': '3vh', 'lineHeight': '2.44vh', 'display': 'flex', 'alignItems': 'center', 'textAlign': 'center', 'letterSpacing':' 0.05em'}),
                html.Div(children = [
                    html.H4('Top 10 Medals by Country'),
                    dcc.Graph(id="graph", figure=fig),    
                ], style={'fontFamily': 'Cabin', 'fontStyle': 'normal', 'color': '#000000', 'backgroundColor': '#F6F7FB', 'position': 'absolute',
                        'width': '18vw', 'height': '87vh', 'left': '3.5vw', 'top': '11vh', 'background': '#FFFFFF', 'boxShadow': '0px 4px 20px rgba(0, 0, 0, 0.15)', 'borderRadius': '12px'})
            ]),
                    
        html.Div(
            style={
                'backgroundColor': '#F6F7FB',
                'height': '98vh'}
		)
    ]
)