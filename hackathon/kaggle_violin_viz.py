import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# import pandas as pd

target_list = ['glom', 'crypt']
target_root_path = rf"X:\temp\violin\hubmap/"
team_names = ['Tom', 'Gleb', 'Whats goin on', 'Deeplive.exe', 'Deepflash2']
team_files = {
    'Tom': "1-tom",
    'Gleb': "2-gleb",
    'Whats goin on': "3-wgo",
    'Deeplive.exe': "4-dl",
    'Deepflash2': "5-df2",
}

color_dict = {f'{team_names[0]}-glom': 'black',
              f'{team_names[0]}-crypt': 'grey',
              f'{team_names[1]}-glom': 'orangered',
              f'{team_names[1]}-crypt': 'orange',
              f'{team_names[2]}-glom': 'midnightblue',
              f'{team_names[2]}-crypt': 'royalblue',
              f'{team_names[3]}-glom': 'darkolivegreen',
              f'{team_names[3]}-crypt': 'mediumseagreen',
              f'{team_names[4]}-glom': 'purple',
              f'{team_names[4]}-crypt': 'violet',
              }

# hpa position info
# point_position_dict = {
#     'dice': {
#         f'{team_names[0]}-crypt': 0.5,
#         f'{team_names[0]}-glom': -0.5,
#         f'{team_names[1]}-crypt': 0.50,
#         f'{team_names[1]}-glom': -0.5,
#         f'{team_names[2]}-crypt': 0.50,
#         f'{team_names[2]}-glom': -0.5,
#         f'{team_names[3]}-crypt': 0.50,
#         f'{team_names[3]}-glom': -0.5,
#         f'{team_names[4]}-crypt': 0.50,
#         f'{team_names[4]}-glom': -0.5,
#     },
#     'recall': {
#         f'{team_names[0]}-crypt': 0.5,
#         f'{team_names[0]}-glom': -0.5,
#         f'{team_names[1]}-crypt': 0.50,
#         f'{team_names[1]}-glom': -0.5,
#         f'{team_names[2]}-crypt': 0.50,
#         f'{team_names[2]}-glom': -0.5,
#         f'{team_names[3]}-crypt': 0.50,
#         f'{team_names[3]}-glom': -0.5,
#         f'{team_names[4]}-crypt': 0.50,
#         f'{team_names[4]}-glom': -0.5,
#     },
#     'precision': {
#         f'{team_names[0]}-crypt': 0.50,
#         f'{team_names[0]}-glom': -1.25,
#         f'{team_names[1]}-crypt': 0.50,
#         f'{team_names[1]}-glom': -0.50,
#         f'{team_names[2]}-crypt': 0.50,
#         f'{team_names[2]}-glom': -0.50,
#         f'{team_names[3]}-crypt': 0.50,
#         f'{team_names[3]}-glom': -0.50,
#         f'{team_names[4]}-crypt': 0.50,
#         f'{team_names[4]}-glom': -0.50,
#     },
# }

# hubmap position info
point_position_dict = {
    'dice': {
        f'{team_names[0]}-crypt': 0.75,
        f'{team_names[0]}-glom': -1.05,
        f'{team_names[1]}-crypt': 0.80,
        f'{team_names[1]}-glom': -1.05,
        f'{team_names[2]}-crypt': 0.45,
        f'{team_names[2]}-glom': -1.05,
        f'{team_names[3]}-crypt': 0.80,
        f'{team_names[3]}-glom': -1.05,
        f'{team_names[4]}-crypt': 0.30,
        f'{team_names[4]}-glom': -1.05,
    },
    'recall': {
        f'{team_names[0]}-crypt': 0.75,
        f'{team_names[0]}-glom': -1.05,
        f'{team_names[1]}-crypt': 0.50,
        f'{team_names[1]}-glom': -1.00,
        f'{team_names[2]}-crypt': 0.30,
        f'{team_names[2]}-glom': -1.00,
        f'{team_names[3]}-crypt': 0.70,
        f'{team_names[3]}-glom': -1.00,
        f'{team_names[4]}-crypt': 0.35,
        f'{team_names[4]}-glom': -1.10,
    },
    'precision': {
        f'{team_names[0]}-crypt': 0.30,
        f'{team_names[0]}-glom': -0.80,
        f'{team_names[1]}-crypt': 0.30,
        f'{team_names[1]}-glom': -0.80,
        f'{team_names[2]}-crypt': 0.30,
        f'{team_names[2]}-glom': -0.80,
        f'{team_names[3]}-crypt': 0.30,
        f'{team_names[3]}-glom': -0.80,
        f'{team_names[4]}-crypt': 0.30,
        f'{team_names[4]}-glom': -0.80,
    },
}

opacity_dict = {'glom': 0.8,
                'crypt': 0.8}
legend_dict = {'glom': 'Glomerulus-level',
               'crypt': 'Crypt-level'}
location_dict = {'dice': [1, 1],
                 'recall': [1, 2],
                 'precision': [2, 2],
                 }

data_types = ['dice', 'recall', 'precision']
glom_data_list = {
    'dice': {},
    'recall': {},
    'precision': {},
}
crypt_data_list = {
    'dice': {},
    'recall': {},
    'precision': {},
}

for target, data_list in zip(target_list, [glom_data_list, crypt_data_list]):
    for team in team_names:
        file_path = target_root_path + rf"{target}\{team_files[team]}.txt"
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            data_list['dice'][team] = [float(line.split(',')[0]) for line in lines if len(line) > 1]
            data_list['recall'][team] = [float(line.split(',')[1]) for line in lines if len(line) > 1]
            data_list['precision'][team] = [float(line.split(',')[2]) for line in lines if len(line) > 1]

# display box and scatter plot along with violin plot
# fig = pt.violin(n_data, y="distance", x="Age", color="Skin Type",
#                 box=True, hover_data=n_data.columns,
#                 points='all',
#                 )
# fig = go.Figure()

fig = make_subplots(
    rows=2, cols=2,
    row_heights=[0.5, 0.5],
    # specs=[[{"type": "Scatter3d", "colspan": 4}, None, None, None],
    #        [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}]],
    shared_xaxes=True,
    vertical_spacing=0.04,
    horizontal_spacing=0.04,
    # subplot_titles=[f'All', 'CD68 / Macrophage', 'T-Helper', 'T-Regulatory'],
    subplot_titles=[f'Dice coefficient', 'Recall', 'Precision', ],
    specs=[[{"secondary_y": False, "rowspan": 2}, {"secondary_y": False}],
           [None, {"secondary_y": False}], ],
)

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
        for level_type in ['glom', 'crypt']:
            fig.add_trace(
                go.Violin(x=[team] * (len(glom_data_list[data_type][team])
                                      if level_type == 'glom' else len(crypt_data_list[data_type][team])),
                          y=(glom_data_list[data_type][team]
                             if level_type == 'glom' else crypt_data_list[data_type][team]),
                          name=team,
                          points="all", opacity=opacity_dict[level_type],
                          pointpos=point_position_dict[data_type][f'{team}-{level_type}'],
                          side=('positive' if level_type == 'crypt' else 'negative'),
                          legendgroup=level_type, showlegend=True if data_type == 'dice' else False,
                          scalemode='width', scalegroup="all", width=0,  # level_type + data_type,
                          jitter=0.05, marker_opacity=0.85, marker_size=1 if level_type == 'glom' else 2.5,
                          line_width=1.5, spanmode='soft',
                          legendgrouptitle_text=legend_dict[level_type],
                          box_visible=True, box_fillcolor='white',
                          line_color=color_dict[f'{team}-{level_type}'], meanline_visible=True, ),
                secondary_y=False, row=location_dict[data_type][0], col=location_dict[data_type][1],
            )

# fig.update_traces(# meanline_visible=False,
#                   scalemode='count')  # scale violin plot area with total count
sub_title_text = "[Glomerulus-level (~2000 matching gloms) \n/ Crypt-level (~160 matching crypts)]"
title_text = f"Kidney/Colon - dice/recall/precision <br><sup>{sub_title_text}</sup>"
fig.update_layout(
    title={
        # 'text': title_text,
        'text': "",
        # 'y':0.9,
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
        size=20,  # 20 for paper / 16 for web
        # color="RebeccaPurple"
    ))
fig.update_layout(legend=dict(
    yanchor="top",
    y=-0.025,
    xanchor="center",
    x=0.5,
    orientation="h",
    font=dict(size=16) # 16 for paper / 12 for web
))
# sub plot title font size
for i in fig['layout']['annotations']:
    i['font'] = dict(size=24)  # 28 for paper / 16 for web

fig.update_yaxes(tickvals=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0], col=1)
fig.update_yaxes(tickfont=dict(size=20), col=2)  # 20 for paper / 14 for web
fig.update_yaxes(tickvals=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0], col=2)
fig.update_yaxes(tickfont=dict(size=18), col=2)  # 16 for paper / 12 for web

fig.write_html(os.path.join(target_root_path, f"kaggle_violin.html"))
fig.write_image(os.path.join(target_root_path, f"kaggle_violin.svg"), width=2000, height=1500)
fig.show()
