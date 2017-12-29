import numpy as np
import dash,pickle,requests
import dash_core_components as dcc
import dash_html_components as html

import tax

import logging

logging.basicConfig(filename='history.log',level=logging.DEBUG)

taxFunctions = {('scotland',2017) : tax.scotland_2017,
         ('scotland',2018) : tax.scotland_2018,
         ('ruk',2017) : tax.ruk_2017,
         ('ruk',2018) : tax.ruk_2018}

app = dash.Dash()
app.suppress_callback_exceptions=True
app.config.update(
    {'routes_pathname_prefix':'',
     'requests_pathname_prefix':''})
server = app.server

layout = html.Div([
    html.Div([
        html.P('Country'),
        dcc.Dropdown(id='country',
                     options = [{'label':'Scotland','value':'scotland'},
                                    {'label':'rUK','value':'ruk'}],   
                     value='scotland'),
                     
        html.P('Tax year'),
        dcc.Dropdown(id='year',
                         options=[{'label':'2017/18','value':2017},
                                  {'label':'2018/19','value':2018}],
                         value=2017),

        html.Div([
            html.P('Income (£)'),
            html.Div([
                dcc.Input(id='tax-input',type='number',value=20000,min=0),
                html.Button(id='submit-button',children='Submit')
            ])
        ])
    ],
    style={'width':'40%','display':'inline-block','vertical-align':'top'}),
        
    html.Div(id='taxfield',style={'width':'58%','display':'inline-block'})
    ],style={'width':'98%'})

app.layout = layout


@app.callback(
    dash.dependencies.Output('taxfield','children'),
    [dash.dependencies.Input('submit-button','n_clicks')],
    [dash.dependencies.State('tax-input','value'),
     dash.dependencies.State('country','value'),
     dash.dependencies.State('year','value')])
def update_tax(n_clicks,income,country,year):

    income = np.double(income)
    f = taxFunctions[(country,year)]
    currentIncomeTax = f(income)
    currentNI = tax.national_insurance(income)
    takehomePay = income - (currentIncomeTax+currentNI)

    dispString = html.Table([
        html.Tr([
            html.Td(
            'Income: £%.1f.'%income)
            ]),
        html.Tr([
            html.Td(
            'Income tax: £%.1f.'%currentIncomeTax)
            ]),
        html.Tr([
            html.Td(
            'Percentage paid in income tax: %.2f%%.'%(currentIncomeTax/income*100))
            ]),
            
        html.Tr([html.Td(html.Hr())]),

        html.Tr([
            html.Td(
                'National insurance: £%.1f.'%currentNI)
            ]),
            
        html.Tr([
            html.Td(
            'Percentage paid in NI: %.2f%%.'%(currentNI/income*100))
            ]),
            
        html.Tr([html.Td(html.Hr())]),

        html.Tr([
            html.Td(
                'Take-home pay: £%.1f.'%takehomePay)
            ]),
            
        html.Tr([
            html.Td(
                'Total paid in tax: £%.1f.'%(currentNI+currentIncomeTax)
                )
            ]),
            
        html.Tr([
            html.Td(
                'Percentage paid in tax: %.1f%%.'%((currentNI+currentIncomeTax)/income*100)
                )
            ])
    ],style={'padding':'25px'})
        
    logging.info('Income: %.2f'%income)
    return dispString
    
if __name__ == "__main__":

    app.run_server(debug=True)
