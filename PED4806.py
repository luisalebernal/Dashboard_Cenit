import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from datetime import datetime
import dash_daq as daq
# Importar hojas de trabajo de google drive     https://bit.ly/3uQfOvs
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import time
import mysql.connector
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.css.append_css({'external_url': '/static/reset.css'})
app.server.static_folder = 'static'
server = app.server

app.layout = dbc.Container([
    dcc.Store(id='store-data-general', storage_type='memory'),  # 'local' or 'session'
    dcc.Store(id='store-data-producto', storage_type='memory'),  # 'local' or 'session'

    dcc.Interval(
        id='my_interval',
        disabled=False,
        interval=1 * 1000,
        n_intervals=0,
        max_intervals=1
    ),
    dbc.Row([
        dbc.Col([dbc.CardImg(
            src="/assets/Logo.jpg",

            style={"width": "6rem",
                   'text-align': 'right'},
        ),

        ], align='right', width=2),
        dbc.Col(html.H5(
            '"Cualquier tecnología lo suficientemente avanzada, es indistinguible de la magia." - Arthur C. Clarke '),
                style={'color': "green", 'font-family': "Franklin Gothic"}, width=7),
    ]),
    dbc.Row([
        dbc.Col(html.H1(
            "Resumen de Producción - PED4806 - Cenit",
            style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"}), width=12, )
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Accordion([
                dbc.AccordionItem([
                    html.H5([
                                'El siguiente tablero interactivo presenta el estado de producción de los 50 módulos los cuales son fabricados para el cliente Cenit. '])

                ], title="Introducción"),
            ], start_collapsed=True, style={'textAlign': 'left', 'color': '#082255', 'font-family': "Franklin Gothic"}),

        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
    ]),
    dbc.Row([
        dbc.Col([
            # html.H5('Última actualización: ' + str(ultAct), style={'textAlign': 'right'})
        ])
    ]),
    dbc.Row([
        dbc.Tabs([
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # OT y PED
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Número OT:",
                                            id="numero-ot-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el número de la orden de trabajo (OT).",
                                            target="numero-ot-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='numero-ot', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "PED:",
                                            id="ped-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el código del pedido.",
                                            target="ped-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='ped', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Cliente y Producto
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Cliente:",
                                            id="cliente-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el nombre del cliente a quien se le hace el pedido.",
                                            target="cliente-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='cliente', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Producto:",
                                            id="producto-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el producto que se está fabricando.",
                                            target="producto-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='producto', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Unidad y Cantidad
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Unidad:",
                                            id="unidad-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra la unidad del producto.",
                                            target="unidad-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='unidad', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Cantidad:",
                                            id="cantidad-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra la cantidad del producto.",
                                            target="cantidad-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='cantidad', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Material y fecha de expedición
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Material:",
                                            id="material-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el material del producto.",
                                            target="material-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='material', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Fecha de Expedición:",
                                            id="fecha-expedicion-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra la fecha en la que se originó el pedido.",
                                            target="fecha-expedicion-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='fecha-expedicion', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                            ])
                        ]),

                    ]),

                ]),
            ], label="Datos Generales del Pedido", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # Fechas
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Fecha:",
                                            id="fecha-target",
                                            color="info",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra la fecha actual.",
                                            target="fecha-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='fecha', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Unidades procesadas y prct de unidades procesadas
                                dbc.Row([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Unidades Procesadas:",
                                                id="unidades-procesadas-target",
                                                color="success",
                                                style={'font-family': "Franklin Gothic"},
                                                className="me-1",
                                                n_clicks=0,
                                            ),
                                            dbc.Popover(
                                                "Muestra el número de unidades procesadas terminadas.",
                                                target="unidades-procesadas-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),
                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            html.Div(id='unidades-procesadas', style={'font-family': "Franklin Gothic"})
                                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),

                                        dbc.Col([
                                            dbc.Button(
                                                "% Unidades Procesadas:",
                                                id="prct-unidades-procesadas-target",
                                                color="success",
                                                style={'font-family': "Franklin Gothic"},
                                                className="me-1",
                                                n_clicks=0,
                                            ),
                                            dbc.Popover(
                                                "Muestra el porcentaje de unidades procesadas terminadas.",
                                                target="prct-unidades-procesadas-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),
                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            html.Div(id='prct-unidades-procesadas', style={'font-family': "Franklin Gothic"})
                                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                        dbc.Col([
                                            daq.GraduatedBar(
                                                id='unidades-procesadas-barra',
                                                color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6],
                                                                  "green": [6.6, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0
                                                # value=10
                                            )
                                        ]),
                                    ]),
                                ]),
                                # Unidades despachadas y prct de unidades despachadas
                                dbc.Row([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Unidades Despachadas:",
                                                id="unidades-despachadas-target",
                                                color="primary",
                                                style={'font-family': "Franklin Gothic"},
                                                className="me-1",
                                                n_clicks=0,
                                            ),
                                            dbc.Popover(
                                                "Muestra el número de unidades despachadas.",
                                                target="unidades-despachadas-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),
                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            html.Div(id='unidades-despachadas', style={'font-family': "Franklin Gothic"})
                                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                        dbc.Col([
                                            dbc.Button(
                                                "% Unidades despachadas:",
                                                id="prct-unidades-despachadas-target",
                                                color="primary",
                                                style={'font-family': "Franklin Gothic"},
                                                className="me-1",
                                                n_clicks=0,
                                            ),
                                            dbc.Popover(
                                                "Muestra el porcentaje de unidades despachadas.",
                                                target="prct-unidades-despachadas-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),
                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            html.Div(id='prct-unidades-despachadas',
                                                     style={'font-family': "Franklin Gothic"})
                                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                        dbc.Col([
                                            daq.GraduatedBar(
                                                id='unidades-despachadas-barra',
                                                color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6],
                                                                  "green": [6.6, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0
                                                # value=10
                                            )
                                        ]),
                                    ]),
                                ]),
                                # Fecha límite de entrega y días faltantes
                                dbc.Row([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(
                                                "Fecha Límite:",
                                                id="fecha-limite-target",
                                                color="success",
                                                style={'font-family': "Franklin Gothic"},
                                                className="me-1",
                                                n_clicks=0,
                                            ),
                                            dbc.Popover(
                                                "Muestra la fecha límite de entrega del pedido.",
                                                target="fecha-limite-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),
                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            html.Div(id='fecha-limite',
                                                     style={'font-family': "Franklin Gothic"})
                                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                        dbc.Col([
                                            dbc.Button(
                                                "Días restantes:",
                                                id="dias-restantes-target",
                                                color="success",
                                                style={'font-family': "Franklin Gothic"},
                                                className="me-1",
                                                n_clicks=0,
                                            ),
                                            dbc.Popover(
                                                "Muestra los días calendario restantes para cumplir la fecha de entrega.",
                                                target="dias-restantes-target",
                                                body=True,
                                                trigger="hover",
                                                style={'font-family': "Franklin Gothic"}
                                            ),
                                        ], width=2, align='center', className="d-grid gap-2"),
                                        dbc.Col([
                                            html.Div(id='dias-restantes',
                                                     style={'font-family': "Franklin Gothic"})
                                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                        dbc.Col([
                                            daq.GraduatedBar(
                                                id='dias-restantes-barra',
                                                color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6],
                                                                  "green": [6.6, 10]}},
                                                showCurrentValue=False,
                                                step=0.2,
                                                value=0
                                                # value=10
                                            )
                                        ]),
                                    ]),
                                ]),
                                # Figura de barras
                                dbc.Row(dbc.Col(
                                    dbc.Spinner(children=[dcc.Graph(id="fig-barras")], size="lg",
                                                color="primary", type="border", fullscreen=True, ),
                                    width={'size': 12, 'offset': 0}),
                                ),

                                # Figura de dispersión
                                dbc.Row(dbc.Col(
                                    dbc.Spinner(children=[dcc.Graph(id="fig-scatter")], size="lg",
                                                color="primary", type="border", fullscreen=True, ),
                                    width={'size': 12, 'offset': 0}),
                                ),
                                # Figura de destino
                                dbc.Row(dbc.Col(
                                    dbc.Spinner(children=[dcc.Graph(id="fig-barras-destino")], size="lg",
                                                color="primary", type="border", fullscreen=True, ),
                                    width={'size': 12, 'offset': 0}),
                                ),
                            ])
                        ]),
                    ])
                ]),
            ], label="Resumen Principal", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # Código de trazabilidad
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Seleccionar Código de Trazabilidad:",
                                            id="selec-codigo-target",
                                            color="info",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Es el código de trazabilidad único para cada módulo",
                                            target="selec-codigo-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        dcc.Dropdown(id='codigo',
                                                     options=[],
                                                     style={'font-family': "Franklin Gothic"}
                                                     )
                                    ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                                ]),
                                # Lote de material y fecha de producción
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Lote:",
                                            id="lote-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el lote del material.",
                                            target="lote-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='lote', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Fecha de Producción:",
                                            id="fecha-produccion-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra la fecha en la que el módulo fue producido.",
                                            target="fecha-produccion-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='fecha-produccion', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Fecha de inspección y consecutivo prueba de calidad
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Fecha de Inspección:",
                                            id="fecha-inspeccion-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra la fecha en la que el módulo fue inspeccionado.",
                                            target="fecha-inspeccion-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='fecha-inspeccion', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Prueba de Calidad:",
                                            id="prueba-calidad-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el consecutivo de la prueba de calidad del módulo.",
                                            target="prueba-calidad-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='prueba-calidad', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Prueba de tensión y prueba de pelado
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Prueba de Tensión:",
                                            id="prueba-tension-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el valor promedio de la prueba de tensión.",
                                            target="prueba-tension-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='prueba-tension', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Prueba de Pelado:",
                                            id="prueba-pelado-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el valor promedio de la prueba de pelado.",
                                            target="prueba-pelado-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='prueba-pelado', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Dimensiones finales y cantidad de argollas
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "Dimensiones:",
                                            id="dimensiones-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra las dimensiones finales del módulo.",
                                            target="dimensiones-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='dimensiones', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Argollas:",
                                            id="argollas-target",
                                            color="primary",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra la cantidad de argollas que posee el módulo.",
                                            target="argollas-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='argollas', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                                # Despachado y destino
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button(
                                            "¿Despachado?:",
                                            id="despachado-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra si el módulo ha sido despachado.",
                                            target="despachado-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='despachado', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                    dbc.Col([
                                        dbc.Button(
                                            "Destino:",
                                            id="destino-target",
                                            color="success",
                                            style={'font-family': "Franklin Gothic"},
                                            className="me-1",
                                            n_clicks=0,
                                        ),
                                        dbc.Popover(
                                            "Muestra el destino de entrega del módulo.",
                                            target="destino-target",
                                            body=True,
                                            trigger="hover",
                                            style={'font-family': "Franklin Gothic"}
                                        ),
                                    ], width=2, align='center', className="d-grid gap-2"),
                                    dbc.Col([
                                        html.Div(id='destino', style={'font-family': "Franklin Gothic"})
                                    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                                ]),
                            ])
                        ]),
                    ])
                ]),
            ], label="Resumen por Producto", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),

        ]),
    ]),

])


@app.callback(
    Output(component_id='store-data-general', component_property='data'),
    Output(component_id='store-data-producto', component_property='data'),
    Output(component_id='codigo', component_property='options'),
    Output(component_id='codigo', component_property='value'),


    Input('my_interval', 'n_intervals'),
)
def dropdownTiempoReal(value_intervals):
    names = ["OT", "Pedido", "Cliente", "Producto", "Unidad", "Cantidad", "Material", "", "", "",
             "Item", "Codigo", "Lote", "Fecha produccion", "Fecha inspeccion", "Consecutivo",
             "Tension", "Pelado", "Dimension", "Argollas", "Despachado", "Destino", ]

    # Extraer datos de google sheets
    SERVICE_ACCOUNT_FILE = 'keys-ped4806.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    # SAMPLE_SPREADSHEET_ID = '1hT5gjZ8QES6GtPmnoxhmR3NG8xyzf0kFUfd7sunzV70'
    SAMPLE_SPREADSHEET_ID = '1cLcGswxxo6MxuivVL3TDMT6m-ZuO487Gl15SJNPYT7w'

    SAMPLE_RANGE_COMBINADO = "PED"

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_COMBINADO = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                           range=SAMPLE_RANGE_COMBINADO).execute()

    df = result_COMBINADO.get('values', [])
    df = pd.DataFrame(df, columns=names)
    df.drop([0], inplace=True)
    df = df.rename(index=lambda x: x - 1)

    dfGeneral = df.iloc[:, [0, 1, 2, 3, 4, 5, 6]]
    dfProducto = df.iloc[:, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]]

    dfGeneral = dfGeneral.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfProducto = dfProducto.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")

    codInicialVec = dfProducto["Codigo"]
    codInicial = codInicialVec.iloc[-1]

    return dfGeneral.to_dict('records'), dfProducto.to_dict('records'), codInicialVec, codInicial \



@app.callback(
    Output(component_id='numero-ot', component_property='children'),
    Output(component_id='ped', component_property='children'),
    Output(component_id='cliente', component_property='children'),
    Output(component_id='producto', component_property='children'),
    Output(component_id='unidad', component_property='children'),
    Output(component_id='cantidad', component_property='children'),
    Output(component_id='material', component_property='children'),
    Output(component_id='fecha', component_property='children'),
    Output(component_id='unidades-procesadas', component_property='children'),
    Output(component_id='prct-unidades-procesadas', component_property='children'),
    Output(component_id='unidades-despachadas', component_property='children'),
    Output(component_id='prct-unidades-despachadas', component_property='children'),
    Output(component_id='fecha-limite', component_property='children'),
    Output(component_id='dias-restantes', component_property='children'),

    Output(component_id='lote', component_property='children'),
    Output(component_id='fecha-produccion', component_property='children'),
    Output(component_id='fecha-inspeccion', component_property='children'),
    Output(component_id='prueba-calidad', component_property='children'),
    Output(component_id='prueba-tension', component_property='children'),
    Output(component_id='prueba-pelado', component_property='children'),
    Output(component_id='dimensiones', component_property='children'),
    Output(component_id='argollas', component_property='children'),
    Output(component_id='despachado', component_property='children'),
    Output(component_id='destino', component_property='children'),
    Output(component_id='fig-barras', component_property='figure'),
    Output(component_id='fig-scatter', component_property='figure'),
    Output(component_id='unidades-procesadas-barra', component_property="value"),
    Output(component_id='unidades-despachadas-barra', component_property="value"),
    Output(component_id='dias-restantes-barra', component_property="value"),
    Output(component_id='fecha-expedicion', component_property='children'),
    Output(component_id='fig-barras-destino', component_property='figure'),

    Input('my_interval', 'n_intervals'),
    Input('codigo', 'value'),
    Input(component_id='store-data-general', component_property='data'),
    Input(component_id='store-data-producto', component_property='data'),

)

def PED4860(value_intervals, value_codigo, data1, data2):
    data1 = pd.DataFrame(data1)
    data2 = pd.DataFrame(data2)

    dfGeneral = data1
    dfProducto = data2


    ############################# Módulo 1 ###################################

    # Extrae numero ot, ped, cliente, producto, unidad, cantidad y material

    ot = dfGeneral["OT"]
    ot = ot.iloc[0]

    ped = dfGeneral["Pedido"]
    ped = ped.iloc[0]

    cliente = dfGeneral["Cliente"]
    cliente = cliente.iloc[0]

    producto = dfGeneral["Producto"]
    producto = producto.iloc[0]

    unidad = dfGeneral["Unidad"]
    unidad = unidad.iloc[0]

    cantidad = dfGeneral["Cantidad"]
    cantidad = cantidad.iloc[0]

    material = dfGeneral["Material"]
    material = material.iloc[0]

    fechaExpe = "28/10/2022"

    ############################# Módulo 2  ###################################

    # Fecha de hoy
    fechaHoy = datetime.now().strftime('%d/%m/%Y')

    # Unidades procesadas
    uniProces = len(dfProducto["Fecha produccion"])
    uniProcesBarra = (uniProces / 50) * 10
    prctUniProces = str(round(uniProces/50*100, 2)) + "%"

    # Unidades despachadas
    def normalize(s): # función que cambia de tildes a sin tildes
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s
    uniDespa = dfProducto["Despachado"]
    uniDespa = uniDespa.apply(lambda x: normalize(x.lower().strip()).capitalize())
    dfProducto["Despachado"] = uniDespa
    uniDespa = uniDespa[uniDespa == "Si"].count()
    uniDespaBarra = (uniDespa / 50) * 10


    prctUniDespa = str(round(uniDespa/50*100, 2)) + "%"

    # Fecha límite
    fechaLimite = "15/12/2022"

    # Días restantes
    diasrest = datetime.strptime(str(fechaLimite), '%d/%m/%Y') - datetime.now()
    diasrestBarra = (1 - diasrest.days / 48) * 10
    diasrest = str(diasrest.days) + " días"

    # Figura de barras
    x_barras = ["Procesado"]
    x2_barras = ["Despachado"]

    fig_barras = go.Figure(data=[
        go.Bar(name='Procesados', x=x_barras, y=[uniProces]),
        go.Bar(name='Despachados', x=x2_barras, y=[uniDespa])
    ])

    fig_barras.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
        barmode='group',
        title="Estado de Productos",
        xaxis_title="Estado",
        yaxis_title="Cantidad"
        )

    # Figura de dispersión
    # fechaHorasCort = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaHorasCort))
    fechaScatter = dfProducto["Fecha produccion"]
    fechaScatter = fechaScatter.apply(lambda x: datetime.strptime(x, "%d/%m/%Y"))

    unosProd = dfProducto["Fecha produccion"] != None
    unosProd = unosProd.apply(lambda x: 1 if x == True else 0)
    dfProducto["Cantidad producida"] = unosProd.cumsum()
    unosProd = dfProducto["Cantidad producida"]

    unosDespa = dfProducto["Despachado"] == "Si"
    unosDespa = unosDespa.apply(lambda x: 1 if x == True else 0)
    dfProducto["Cantidad despachada sencilla"] = unosDespa
    dfProducto["Cantidad despachada"] = unosDespa.cumsum()
    unosDespa = dfProducto["Cantidad despachada"]
    unosDespaSenci = dfProducto["Cantidad despachada sencilla"]

    print(unosDespaSenci)

    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(x=fechaScatter, y=unosProd, name="Producido", text=unosProd,
                                      mode='lines+markers+text', textposition='bottom right',))
    fig_scatter.add_trace(go.Scatter(x=fechaScatter, y=unosDespa, name="Despachado", text=unosDespa,
                                      mode='lines+markers+text', textposition='bottom right',))

    fig_scatter.update_layout(title="Estado de Productos", xaxis_title="Fecha",
                        yaxis_title="Cantidad")
    fig_scatter.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.7,
        xanchor="center",
        x=0.5
    ))

    fig_scatter.update_layout(
        font_family="Franklin Gothic",
        #font_color="blue",
        title_font_family="Franklin Gothic",
        #title_font_color="red",
        #legend_title_font_color="green"
    )
    fig_scatter.update_xaxes(title_font_family="Franklin Gothic")

    # Figura de barras de locaciones enviadas
    fig_locacion = px.bar(dfProducto, x='Destino', y='Cantidad despachada sencilla')

    fig_locacion.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
        # barmode='group',
        title="Destino de Productos Despachados",
        xaxis_title="Destino",
        yaxis_title="Cantidad Despachada"
        )


    ############################# Módulo 3  ###################################

    llaves = ["Lote", "Fecha produccion", "Fecha inspeccion", "Consecutivo",
         "Tension", "Pelado", "Dimension", "Argollas", "Despachado", "Destino",]

    variables, i = [0] * 10, 0

    for llave, variable in zip(llaves, variables):
        variable = dfProducto[dfProducto["Codigo"] == value_codigo]
        variable = variable[llave].iloc[0]
        variables[i] = variable
        i = i + 1

    lote, fechaProd, fechaInsp, consec, tension, pelado, dimension, argollas, despachado, destion = variables[0], \
        variables[1], variables[2], variables[3], variables[4], variables[5], variables[6], variables[7], \
        variables[8], variables[9],

    despachado = normalize(despachado.lower().strip()).capitalize()
    if despachado == "Si": despachado = "Sí"


    return ot, ped, cliente, producto, unidad, cantidad, material, fechaHoy,uniProces, prctUniProces, \
           uniDespa, prctUniDespa, fechaLimite, diasrest, lote, fechaProd, fechaInsp, consec, tension, \
           pelado, dimension, argollas, despachado, destion, fig_barras, fig_scatter, uniProcesBarra, \
           uniDespaBarra, diasrestBarra, fechaExpe, fig_locacion



if __name__ == '__main__':
    app.run_server()



