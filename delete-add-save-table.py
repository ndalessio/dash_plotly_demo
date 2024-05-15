import dash
import json
import pandas as pd
import dash_bootstrap_components as dbc
import dash_ag_grid as dag              
from dash import Dash, html, dcc, Input, Output, State, no_update, ctx, callback
               
# Delete using icon
# Add row by clicking add row button
# Edit by pencil in cell (not ready)

dash.register_page(__name__, path='/users', name='Users', icon="fas fa-solid fa-user me-2", order=3)

df = pd.read_json("data/users.json")

columnDefs = [
        {
        "headerName": "Name",  
        "field": "name", 
        "type": "rightAligned",     
        # "checkboxSelection": True, 
    },
    {
        "headerName": "Email",
        "field": "email",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter"
    },
    {
        "headerName": "Function",
        "field": "function",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {"values":["Viewer","Super User","Admin"]},
    },
    {
        "headerName": "",
        "cellRenderer": "DeleteButton",
        "lockPosition":'right',
        "maxWidth":35,
        "filter": False,
        'cellStyle': {'paddingRight': 0, 'paddingLeft': 0},
    },
]

defaultColDef = {
    "filter": True,
    "floatingFilter": True,
    "resizable": True,
    "sortable": True,
    "minWidth": 150,
    "editable": True,
    "cellRenderer": "EditButton"
}

table = dag.AgGrid(
    id="users-table",
    className="ag-theme-alpine-dark",
    rowData=df.to_dict("records"),
    columnDefs=columnDefs, #[{"field": i} for i in df.columns]
    defaultColDef=defaultColDef,
    columnSize="sizeToFit",
    dashGridOptions={
                "animateRows": False,
                "rowSelection":"multiple",
                "suppressClickEdit": True,
                "singleClickEdit": True,
                "stopEditingWhenCellsLoseFocus": True
                }
)

def layout():
    return dbc.Container([
        table,
        html.Span([
            dbc.Button(id="add-row-btn", children="Add row"),
            dbc.Button(id="save-btn", children="Save")
        ])
    ])

@callback(
    Output("users-table", "deleteSelectedRows"),
    Output("users-table", "rowData"),
    # Input("delete-row-btn", "n_clicks"),
    Input("add-row-btn", "n_clicks"),
    Input("save-btn", "n_clicks"),
    State("users-table", "rowData"),
    prevent_initial_call=True
)
def update_dash_table(n_dlt, n_add, n_save, data):
    if ctx.triggered_id == "add-row-btn":
        new_row = {
            "name":[""],
            "email":["@deloitte.com.au"],
            "function":[""]
        }
        df_new_row = pd.DataFrame(new_row)
        updated_table = pd.concat([pd.DataFrame(data), df_new_row])
        return False, updated_table.to_dict("records")
    
    elif ctx.triggered_id == "save-btn":
        updated_data = pd.DataFrame(data)
        with open('data/users.json', 'w') as outfile:
            outfile.write(updated_data.to_json(orient="records"))
        return False, no_update
