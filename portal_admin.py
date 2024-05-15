import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Output, Input, callback, State, dcc
import json

dash.register_page(__name__, path='/portal_admin', name='Admin', icon="fas fa-solid fa-gear", order=5)


def create_card_action():
    return dbc.Card(
        [
            
            html.P("", className="form-title"),
            dcc.Input(id="dashboard-title", type="text", placeholder="Dashboard title", className="input-dashboard"),
            dcc.Input(id="dashboard-desc", type="text", placeholder="Dashboard description", className="input-dashboard"),
            dcc.Input(id="dashboard-image-url", type="text", placeholder="Dashboard image url", className="input-dashboard"),
            dcc.Input(id="dashboard-url", type="text", placeholder="Dashboard url", className="input-dashboard"),
            dbc.Button("Add dashboard", id="button-add-dashboard", className="button-class-1")
            
        ], className="card-dashboard-form"
    )


def layout():
    return dbc.Container(
        [ 
            create_card_action(),
            html.Div(id="hidden-div", style={"display":"none"}),
            dcc.Store(id="button-clicks-2", data=0),
        ] , className="page-main-container"
)

@callback(
    Output("button-clicks-2", "data"), 
    Input("button-add-dashboar", "n_clicks"),
)


@callback(
    Output('hidden-div', 'children'),
    Input('button-add-dashboard','n_clicks'),
    State('dashboard-title','value'), 
    State('dashboard-desc','value'), 
    State('dashboard-image-url','value'), 
    State('dashboard-url','value')
        )
def addDashboard(n_clicks, dashboardTitle, dashboardText, dashboardImage, dashboardUrl):
    if n_clicks is None:
        return dash.no_update
    
    else:
        current_data = pd.read_json('data/dashboards.json')
        new_row_data = {"dashboardTitle": dashboardTitle,"dashboardText":dashboardText, "dashboardImage": dashboardImage,"dashboardUrl":dashboardUrl}
        updated_data = pd.concat([current_data, pd.DataFrame(new_row_data, index=['dashboardTitle'])],axis=0, ignore_index=True)

        # Update Json file
        json_str = updated_data.to_json(orient="records", date_format="iso")
        parsed = json.loads(json_str)
        # print(new_row_data)
        
        with open('data/dashboards.json', 'w') as json_file:
            json_file.write(json.dumps(parsed, indent=4))

        # print('n_clicks',n_clicks)
        return None
