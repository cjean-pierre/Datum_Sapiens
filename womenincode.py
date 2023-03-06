from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plot_women_incode(df, col, title, yrange):

    df_wall = round((df[(df['Student'] == 'No')].groupby(['Year'])['Gender'].value_counts(normalize=True)*100),
                    2).to_frame().rename(columns={'Gender': '% in pop'}).reset_index()
    df_sall = round((df[(df['Student'] == 'Yes')].groupby(['Year'])['Gender'].value_counts(normalize=True)*100),
                    2).to_frame().rename(columns={'Gender': '% in pop'}).reset_index()
    df_wall = df_wall.loc[df_wall['Gender'] == 'Woman']
    df_sall = df_sall.loc[df_sall['Gender'] == 'Woman']

    if col == 'Code_exp':
        mask = 'I have never written code'
        name = '% in code illiterate'
    elif col == 'Ml_exp':
        mask = 'I do not use machine learning methods'
        name = '% in no ML usage'

    df_nos = df.loc[(df[col] == mask) & (df['Student'] == 'Yes')]
    df_now = df.loc[(df[col] == mask) & (df['Student'] == 'No')]
    dw = round((df_now.groupby(['Year'])['Gender'].value_counts(normalize=True)*100), 2).to_frame().rename(
         columns={'Gender': name}).reset_index()
    ds = round((df_nos.groupby(['Year'])['Gender'].value_counts(normalize=True)*100), 2).to_frame().rename(
         columns={'Gender': name}).reset_index()

    dw = dw.loc[dw['Gender'] == 'Woman']
    ds = ds.loc[ds['Gender'] == 'Woman']

    fig = make_subplots(1, 2, horizontal_spacing=0.02, subplot_titles=("Female Students", "Female Workers"))

    fig.add_trace(go.Scatter(x=dw.loc[:, 'Year'], y=dw.loc[:, name],
                             mode='lines+markers',
                             name=name,
                             line={'color': '#977C39'},
                             showlegend=True,
                             ), 1, 2)
    fig.add_trace(go.Scatter(x=ds.loc[:, 'Year'], y=ds.loc[:, name],
                             mode='lines+markers',
                             name=name,
                             line={'color': '#CB2416'},
                             showlegend=True,

                             ), 1, 1)
    fig.add_trace(go.Scatter(x=df_wall.loc[:, 'Year'], y=df_wall.loc[:, '% in pop'],
                             mode='lines+markers',
                             name='% in population',
                             line={'color': 'lightgrey'},
                             showlegend=True
                             ), 1, 2)
    fig.add_trace(go.Scatter(x=df_sall.loc[:, 'Year'], y=df_sall.loc[:, '% in pop'],
                             mode='lines+markers',
                             name='% in population',
                             line={'color': 'lightgrey'},
                             showlegend=False
                             ), 1, 1)

    fig.update_yaxes(matches='y')
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(color='white', row=1, col=1)
    fig.update_layout(yaxis_range=yrange)
    fig.update_layout(margin=dict(t=110, l=25, r=25, b=25),
                      plot_bgcolor='white',
                      font={'family': "Old Standard TT"},

                      title={'text':  title + '<br>',
                             'font': {'family': "Old Standard TT", 'size': 40, 'color': "#CB2416"}},
                      height=500,
                      width=800
                      )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F4F1E0')
    fig.update_layout(hovermode="x unified")

    return fig


def unemployment_pergen(df, title, subtitle1, subtitle2):
    # percentage of women in pop
    df_wall = round((df[(df['Student'] == 'No')].groupby(['Year'])['Gender'].value_counts(normalize=True) * 100),
                    2).to_frame().rename(columns={'Gender': '% in pop'}).reset_index()
    df_wall = df_wall.loc[df_wall['Gender'] == 'Woman']
    # percentage of women in unemployed
    df_un = df.loc[(df['Jobs'] == 'Not employed') & (df['Student'] == 'No')]
    df_un = round((df_un.groupby(['Year'])['Gender'].value_counts(normalize=True) * 100), 2).to_frame().rename(
        columns={'Gender': '% in not employed'}).reset_index()
    df_un = df_un.loc[df_un['Gender'] == 'Woman']

    # unemployment rate
    global_un = round(
        (df.loc[(df['Student'] == 'No'), ['Year', 'Jobs']].groupby('Year')['Jobs'].value_counts(normalize=True) * 100),
        2).to_frame().rename(
        columns={'Jobs': 'unemployment rate'}).reset_index()
    global_un = global_un.loc[global_un['Jobs'] == 'Not employed']
    un_gen = round((df.loc[(df['Student'] == 'No'), ['Year', 'Gender', 'Jobs']].groupby(['Year', 'Gender'])[
                        'Jobs'].value_counts(normalize=True) * 100), 2).to_frame().rename(
        columns={'Jobs': 'unemployment rate'}).reset_index()
    un_gen = un_gen.loc[un_gen['Jobs'] == 'Not employed']
    un_genm = un_gen.loc[un_gen['Gender'] == 'Man']
    un_genw = un_gen.loc[un_gen['Gender'] == 'Woman']

    # plot figure
    fig = make_subplots(1, 2, horizontal_spacing=0.02, subplot_titles=(subtitle1, subtitle2))

    fig.add_trace(go.Scatter(x=un_genm.loc[:, 'Year'], y=un_genm.loc[:, 'unemployment rate'],
                             mode='lines+markers',
                             name='Men',
                             line={'color': "#083F80"},
                             showlegend=True,

                             ), 1, 1)
    fig.add_trace(go.Scatter(x=un_genw.loc[:, 'Year'], y=un_genw.loc[:, 'unemployment rate'],
                             mode='lines+markers',
                             name='Woman',
                             line={'color': "#CC0C95"},
                             showlegend=True,

                             ), 1, 1)
    fig.add_trace(go.Scatter(x=global_un.loc[:, 'Year'], y=global_un.loc[:, 'unemployment rate'],
                             mode='lines+markers',
                             name='Global',
                             line={'color': 'lightgrey'},
                             showlegend=True,
                             ), 1, 1)
    fig.add_trace(go.Scatter(x=df_un.loc[:, 'Year'], y=df_un.loc[:, '% in not employed'],
                             mode='lines+markers',
                             name='% in not employed',
                             line={'color': "#CC0C95"},
                             showlegend=False
                             ), 1, 2)
    fig.add_trace(go.Scatter(x=df_wall.loc[:, 'Year'], y=df_wall.loc[:, '% in pop'],
                             mode='lines+markers',
                             name='% in population',
                             line={'color': 'lightgrey'},
                             showlegend=False,
                             ), 1, 2)

    fig.update_layout(yaxis_range=[0, 30])
    fig.update_layout(margin=dict(t=110, l=25, r=25, b=25),
                      plot_bgcolor='white',
                      font={'family': "Old Standard TT"},

                      title={'text': title + '<br>',
                             'font': {'family': "Old Standard TT", 'size': 40, 'color': "#CB2416"}},
                      height=500,
                      width=800
                      )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F4F1E0')
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(matches='y')
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(color='white', row=1, col=1)

    return fig





