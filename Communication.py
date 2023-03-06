import pandas as pd
import plotly.express as px


def language_pergen(surveys, student=None, gender=None):

    questions_2022 = ['Q12_1', 'Q12_2', 'Q12_3', 'Q12_4', 'Q12_5', 'Q12_6', 'Q12_7', 'Q12_8', 'Q12_9', 'Q12_10',
                      'Q12_11', 'Q12_12', 'Q12_13', 'Q12_14', 'Q12_15']
    questions_2021 = ['Q7_Part_1', 'Q7_Part_2', 'Q7_Part_3', 'Q7_Part_4', 'Q7_Part_5',
                      'Q7_Part_6', 'Q7_Part_7', 'Q7_Part_8', 'Q7_Part_9', 'Q7_Part_10', 'Q7_Part_11', 'Q7_Part_12',
                      'Q7_OTHER']

    questions_2020 = ['Q7_Part_1', 'Q7_Part_2', 'Q7_Part_3', 'Q7_Part_4', 'Q7_Part_5',
                      'Q7_Part_6', 'Q7_Part_7', 'Q7_Part_8', 'Q7_Part_9', 'Q7_Part_10', 'Q7_Part_11', 'Q7_Part_12',
                      'Q7_OTHER']
    questions_2019 = ['Q18_Part_1', 'Q18_Part_2', 'Q18_Part_3', 'Q18_Part_4', 'Q18_Part_5',
                      'Q18_Part_6', 'Q18_Part_7', 'Q18_Part_8', 'Q18_Part_9', 'Q18_Part_10', 'Q18_Part_11',
                      'Q18_Part_12']
    questions_2018 = ['Q16_Part_1', 'Q16_Part_2', 'Q16_Part_3', 'Q16_Part_4', 'Q16_Part_5',
                      'Q16_Part_6', 'Q16_Part_7', 'Q16_Part_8', 'Q16_Part_9', 'Q16_Part_10', 'Q16_Part_11',
                      'Q16_Part_12', 'Q16_Part_13', 'Q16_Part_14', 'Q16_Part_15', 'Q16_Part_16', 'Q16_Part_17',
                      'Q16_Part_18']

    track_list = ['Python', 'R', 'SQL', 'Java', 'Javascript', 'Bash', 'MATLAB', 'C/C++']

    df_list = []
    for survey, questions in zip(surveys,
                                 [questions_2018, questions_2019, questions_2020, questions_2021, questions_2022]):
        year = int(survey['Year'].unique())
        option_list = []
        for col in questions:
            option_list.extend([i for i in survey.loc[:, col].unique() if pd.notnull(i) is True])

        if student is None:
            df = survey.loc[:, questions].notna().astype(int)
        else:
            df = survey.loc[(survey['Student'] == student) & (survey['Gender'] == gender), questions].notna().astype(
                int)

        df.columns = option_list
        df['Total'] = df.sum(axis=1)
        pop_ans = len(df.loc[df['Total'] != 0])

        if year == 2018:
            df = df.rename(columns={'Javascript/Typescript': 'Javascript'})

        else:
            df['C/C++'] = df['C'] + df['C++']

        other_cols = list(set(df.columns) - set(track_list))
        df = df.drop(columns=other_cols + ['Total'])
        df = df.sum(axis=0).to_frame().reset_index().rename(columns={'index': 'language', 0: 'count'})
        df['%'] = df['count'] / pop_ans * 100
        df['Year'] = year
        df['Gender'] = gender
        df = df.sort_values('count')
        df_list.append(df)
        del df

    return pd.concat(df_list).reset_index(drop=True)


def plot_language_pergen(df, scope):
    fig = px.bar(
        df,
        x='%',
        range_x=[0, 100],
        y='language',
        color='Gender',
        barmode='group',
        animation_frame='Year',
        animation_group='language',
        color_discrete_sequence=["#083F80", "#CC0C95"]
    )
    fig['data'][0].hovertemplate = 'Year: 2018<br>language: %{y}<br>% Speaking: %{x:.2f}<br><extra></extra>'
    fig['data'][1].hovertemplate = 'Year: 2018<br>language: %{y}<br>% Speaking: %{x:.2f}<br><extra></extra>'

    fig.update_layout(margin=dict(t=110, l=25, r=25, b=25),
                      plot_bgcolor='white', bargap=0.4,
                      font={'family': "Old Standard TT"},

                      title={'text': scope + ' Communication' + '<br><sup><sup>' + 'Gender preferences' + '</sup>',
                             'font': {'family': "Old Standard TT", 'size': 40, 'color': "#977C39"}},
                      height=500,
                      width=600
                      )

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1500
    fig.layout.sliders[0]["transition"]["duration"] = 2000
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F4F1E0')

    for i in range(5):
        fig.frames[i].data[0].hovertemplate = 'Year: 2018<br>language: %{y}<br>% Speaking: %{x:.2f}<br><extra></extra>'
        fig.frames[i].data[1].hovertemplate = 'Year: 2018<br>language: %{y}<br>% Speaking: %{x:.2f}<br><extra></extra>'

    return fig


def plot_language_global(df):
    fig = px.bar(
        df,
        x='%',
        range_x=[0, 100],
        y='language',
        animation_frame='Year',
        animation_group='language',
        color_discrete_sequence=['#A39A36']
    )
    fig['data'][0].hovertemplate = 'Year: 2018<br>language: %{y}<br>% Speaking: %{x:.2f}<br><extra></extra>'

    fig.update_layout(margin=dict(t=110, l=25, r=25, b=25),
                      plot_bgcolor='white', bargap=0.4,
                      font={'family': "Old Standard TT"},

                      title={'text': 'Global Communication' + '<br><sup><sup>' + 'the R decline' + '</sup>',
                             'font': {'family': "Old Standard TT", 'size': 40, 'color': "#CB2416"}},
                      height=500,
                      width=600
                      )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F4F1E0')

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1500
    fig.layout.sliders[0]["transition"]["duration"] = 2000

    fig.frames[0].data[0].marker.color = ['#A39A36'] * 5 + ['#FF8038'] + ['#A39A36'] * 2
    fig.frames[1].data[0].marker.color = ['#A39A36'] * 5 + ['#FF8038'] + ['#A39A36'] * 2
    fig.frames[2].data[0].marker.color = ['#A39A36'] * 4 + ['#FF8038'] + ['#A39A36'] * 3
    fig.frames[3].data[0].marker.color = ['#A39A36'] * 4 + ['#FF8038'] + ['#A39A36'] * 3
    fig.frames[4].data[0].marker.color = ['#A39A36'] * 4 + ['#FF8038'] + ['#A39A36'] * 3

    for i in range(5):
        fig.frames[i].data[0].hovertemplate = 'Year: 2018<br>language: %{y}<br>% Speaking: %{x:.2f}<br><extra></extra>'

    return fig
