import os
import plotly.graph_objects as go

# import pandas as pd

data_sources = ['kidney', 'largeintestine']
data_index = 0

team_names = ['Tom', 'Gleb', 'Whats goin on', 'Deeplive.exe', 'Deepflash2']
team_files = {
    'Tom': "1-tom",
    'Gleb': "2-gleb",
    'Whats goin on': "3-wgo",
    'Deeplive.exe': "4-dl",
    'Deepflash2': "5-df2",
}

color_dict = {f'{team_names[0]}': 'black',
              f'{team_names[1]}': 'orangered',
              f'{team_names[2]}': 'midnightblue',
              f'{team_names[3]}': 'darkolivegreen',
              f'{team_names[4]}': 'purple',
              }

point_position_dict = {
    'dice': {
        f'{team_names[0]}-{0}': -0.75,
        f'{team_names[1]}-{0}': -0.75,
        f'{team_names[2]}-{0}': -0.75,
        f'{team_names[3]}-{0}': -0.75,
        f'{team_names[4]}-{0}': -1.25,
        f'{team_names[0]}-{1}': -1,
        f'{team_names[1]}-{1}': -1.05,
        f'{team_names[2]}-{1}': -0.9,
        f'{team_names[3]}-{1}': -0.75,
        f'{team_names[4]}-{1}': -1,
    },
    'recall': {
        f'{team_names[0]}': 0.50,
        f'{team_names[1]}': 0.80,
        f'{team_names[2]}': 0.30,
        f'{team_names[3]}': 0.50,
        f'{team_names[4]}': 0.25,
    },
    'precision': {
        f'{team_names[0]}': 0.50,
        f'{team_names[1]}': 0.40,
        f'{team_names[2]}': 0.30,
        f'{team_names[3]}': 0.50,
        f'{team_names[4]}': 1.05,
    },
}

data_types = ['dice',
              # 'recall',
              # 'precision'
              ]
data_list = {
    'dice': {},
}

file_path = f"violin_demo_data_{data_index}"
with open(file_path, 'r') as f:
    lines = f.read().splitlines()
    for i in range(len(team_names)):
        team = team_names[i]
        data_list['dice'][team] = [float(line.split('\t')[i + 1]) for line in lines if len(line) > 1]

# display box and scatter plot along with violin plot
# fig = pt.violin(n_data, y="distance", x="Age", color="Skin Type",
#                 box=True, hover_data=n_data.columns,
#                 points='all',
#                 )
fig = go.Figure()

# fig.add_trace(go.Violin(x=n_data['Region'][n_data['Skin Type'] == 'Sun-Exposed'],
#                         y=n_data['distance'][n_data['Skin Type'] == 'Sun-Exposed'],
#                         name='Sun-Exposed', legendgroup='Sun-Exposed',
#                         line_color='orange', points="outliers",
#                         box_visible=True, width=2,
#                         meanline_visible=True))
# fig.add_trace(go.Violin(x=n_data['Region'][n_data['Skin Type'] == 'Non-Sun-Exposed'],
#                         y=n_data['distance'][n_data['Skin Type'] == 'Non-Sun-Exposed'],
#                         name='Non-Sun-Exposed', legendgroup='Non-Sun-Exposed',
#                         line_color='blue', points="outliers",
#                         box_visible=True, width=2,
#                         meanline_visible=True))


# region_seq = [12, 5, 4, 2, 10, 7, 11, 3, 6, 8, 9, 1, ]
# for index in range(len(regions)):
#     next = region_seq[index] - 1
#     fig.add_trace(go.Violin(x=n_data['Age'][n_data['Region'] == str(regions[next])],
#                             y=n_data['distance'][n_data['Region'] == str(regions[next])],
#                             name=suns[next], legendgroup=suns[next],
#                             line_color=color_dict[suns[next]], points="outliers",
#                             box_visible=True, width=1,
#                             meanline_visible=True))
# for skin_type in ['Sun-Exposed', 'Non-Sun-Exposed']:
#     fig.add_trace(go.Violin(x=n_data['Age'][n_data['Skin Type'] == skin_type],
#                             y=n_data['distance'][n_data['Skin Type'] == skin_type],
#                             name=skin_type, legendgroup='All', legendgrouptitle_text="All",
#                             points="outliers", opacity=opacity_dict[skin_type], width=4,
#                             box_visible=True, line_color=color_dict[skin_type], meanline_visible=False),
#                   secondary_y=False, row=1, col=1, )

for data_type in data_types:
    for team in team_names:
        fig.add_trace(
            go.Violin(x=[team] * (len(data_list[data_type][team])),
                      y=data_list[data_type][team],
                      name=team,
                      points="all", opacity=0.8,
                      pointpos=point_position_dict[data_type][f'{team}-{data_index}'],
                      showlegend=True,
                      scalemode='width', scalegroup="all", width=0,  # level_type + data_type,
                      jitter=0.05, marker_opacity=0.85, marker_size=2.5,
                      line_width=1.5, spanmode='soft',
                      box_visible=True, box_fillcolor='white', box_width=0.05,
                      line_color=color_dict[f'{team}'], meanline_visible=True, ),
        )


title_text = f"HPA-{data_sources[data_index]}"
fig.update_layout(
    title={
        'text': title_text,
        'y':0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    # x1axis_title="Age",
    # yaxis_title="Dice",
    violingap=0, violingroupgap=0,
    violinmode='overlay',
    yaxis_zeroline=False,
    font=dict(
        family="Arial, Bahnschrift",
        size=14,  # 20 for paper
        # color="RebeccaPurple"
    ))
# sub plot title font size
for i in fig['layout']['annotations']:
    i['font'] = dict(size=16)  # 28 for paper

fig.update_yaxes(tickvals=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1.0])
fig.update_yaxes(tickfont=dict(size=14))  # 20 for paper

fig.write_html(os.path.join('./result', f"HPA-{data_sources[data_index]}.html"))
fig.write_image(os.path.join('./result', f"HPA-{data_sources[data_index]}.svg"), width=1440, height=1440)
fig.show()
