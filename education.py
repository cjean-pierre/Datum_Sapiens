import plotly.express as px
import pandas as pd


def plot_education_pergen(df, title, subtitle):

    df_s = df.loc[(df['Student'] == 'Yes') & (df['Gender'].isin(['Man', 'Woman']))].copy()
    df_s['Gender'] = df_s['Gender'].str.replace('Man', 'Man Student')
    df_s['Gender'] = df_s['Gender'].str.replace('Woman', 'Woman Student')
    df_w = df.loc[(df['Student'] == 'No') & (df['Gender'].isin(['Man', 'Woman']))].copy()
    df_w['Gender'] = df_w['Gender'].str.replace('Man', 'Man Worker')
    df_w['Gender'] = df_w['Gender'].str.replace('Woman', 'Woman Worker')

    cols = ["#977C39", "#6E6135", "#BAB191", "#EDE2B9",
            "#FAF5DC", "#F4F1E0"]

    fig = px.histogram(pd.concat([df_s, df_w]), y="Gender",
                       barnorm='percent', color='Education',
                       category_orders=dict(
                           Education=['Doctoral degree', 'Master’s degree', 'Bachelor’s degree', 'No degree',
                                      'Professional Education'],
                           Gender=['Man Student', 'Woman Student', 'Man Worker', 'Woman Worker']), orientation='h',
                       animation_frame='Year',
                       color_discrete_sequence=cols,

                       )
    del df_w, df_s

    fig.update_layout(margin=dict(t=110, l=25, r=25, b=25),
                      plot_bgcolor='white', bargap=0.4,
                      font={'family': "Old Standard TT"},

                      title={
                          'text': title + '<br>' + '<sup><sup>' + subtitle + '</sup>',
                          'font': {'family': "Old Standard TT", 'size': 40, 'color': "#CB2416"}},
                      height=500,
                      width=800,
                      xaxis_title="Percentage",
                      yaxis_title=""
                      )

    fig['data'][0].hovertemplate = '2018 %{y}<br> Doctoral degree<br>Percentage : %{x:.2f}%<br><extra></extra>'
    fig['data'][1].hovertemplate = '2018 %{y}<br> Master’s degree<br>Percentage : %{x:.2f}%<br><extra></extra>'
    fig['data'][2].hovertemplate = '2018 %{y}<br> Bachelor’s degree<br>Percentage : %{x:.2f}%<br><extra></extra>'
    fig['data'][3].hovertemplate = '2018 %{y}<br> No degree<br>Percentage=%{x:.2f}%<br><extra></extra>'
    fig['data'][4].hovertemplate = '2018 %{y}<br> Professional Education<br>Percentage : %{x:.2f}%<br><extra></extra>'

    for i, year in enumerate([2018, 2019, 2020, 2021, 2022]):
        fig['frames'][i]['data'][0].hovertemplate = str(
            year) + ' %{y}<br> Doctoral degree<br>Percentage : %{x:.2f}%<br><extra></extra>'
        fig['frames'][i]['data'][1].hovertemplate = str(
            year) + ' %{y}<br> Master’s degree<br>Percentage : %{x:.2f}%<br><extra></extra>'
        fig['frames'][i]['data'][2].hovertemplate = str(
            year) + ' %{y}<br> Bachelor’s degree<br>Percentage : %{x:.2f}%<br><extra></extra>'
        fig['frames'][i]['data'][3].hovertemplate = str(
            year) + ' %{y}<br> No degree<br>Percentage=%{x:.2f}%<br><extra></extra>'
        fig['frames'][i]['data'][4].hovertemplate = str(
            year) + ' %{y}<br> Professional Education<br>Percentage : %{x:.2f}%<br><extra></extra>'

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000
    fig.layout.sliders[0]["transition"]["duration"] = 700

    return fig


def plot_ed_peryear(df, title, subtitle):

    df = (df.groupby(['Year'])['Education'].value_counts(normalize=True) * 100).to_frame().rename(
        columns={'Education': '%_value'}).reset_index()
    df['%'] = df['%_value']
    df.loc[df['Education'].isin(['Master’s degree', 'Doctoral degree']), '%'] = -df.loc[
        df['Education'].isin(['Master’s degree', 'Doctoral degree']), '%']
    df['Year'] = df['Year'].map(lambda x: str(x))

    cols = ["#977C39", "#6E6135", "#BAB191", "#EDE2B9",
            "#FAF5DC", "#F4F1E0"]

    fig = px.bar(df, y='Year', x='%', color='Education', orientation='h',
                 category_orders=dict(Education=['Master’s degree', 'Doctoral degree', 'Bachelor’s degree', 'No degree',
                                                 'Professional Education'],
                                      Year=['2018', '2019', '2020', '2021', '2022']),
                 custom_data=['%_value'],
                 color_discrete_sequence=cols)
    del df
    fig.update_layout(margin=dict(t=110, l=25, r=25, b=25),
                      plot_bgcolor='white', bargap=0.4,
                      font={'family': "Old Standard TT"},

                      title={
                          'text': title + '<br>' + '<sup><sup>' + subtitle + '</sup>',
                          'font': {'family': "Old Standard TT", 'size': 40, 'color': "#CB2416"}},
                      height=400,
                      width=800,
                      xaxis_title="Percentage per Education Level",
                      yaxis_title=""
                      )
    fig['data'][0].hovertemplate = 'Year %{y} :<br> %{customdata:.2f} % Master’s degrees<br><extra></extra>'
    fig['data'][1].hovertemplate = 'Year %{y} :<br> %{customdata:.2f} % Doctoral degrees<br><extra></extra>'
    fig['data'][2].hovertemplate = 'Year %{y} :<br> %{customdata:.2f} % Bachelor’s degrees<br><extra></extra>'
    fig['data'][3].hovertemplate = 'Year %{y} :<br> %{customdata:.2f} % had no degree<br><extra></extra>'
    fig['data'][4].hovertemplate = 'Year %{y} :<br> %{customdata:.2f} % had Professional Education<br><extra></extra>'

    fig.update_xaxes(visible=True, tickfont={'color': 'white'})

    return fig

