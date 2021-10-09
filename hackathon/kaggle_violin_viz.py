import os
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

target_root_path = r"C:\Users\bunny\Desktop\glom"
team_names = ['1-tom', '2-gleb', '3-wgo', '4-dl', '5-df2']

color_dict = {'1-tom-glom': 'black',
              '1-tom-slide': 'grey',
              '2-gleb-glom': 'orangered',
              '2-gleb-slide': 'orange',
              '3-wgo-glom': 'midnightblue',
              '3-wgo-slide': 'royalblue',
              '4-dl-glom': 'darkolivegreen',
              '4-dl-slide': 'mediumseagreen',
              '5-df2-glom': 'purple',
              '5-df2-slide': 'violet',
              }

point_position_dict = {'1-tom-slide': 0.8,
                       '1-tom-glom': -1.1,
                       '2-gleb-slide': 0.8,
                       '2-gleb-glom': -1.1,
                       '3-wgo-slide': 0.8,
                       '3-wgo-glom': -1.1,
                       '4-dl-slide': 0.8,
                       '4-dl-glom': -1.1,
                       '5-df2-slide': 0.8,
                       '5-df2-glom': -1.1,
                       }

opacity_dict = {'glom': 0.7,
                'slide': 0.7}
legend_dict = {'glom': 'Glomeruli level',
               'slide': 'Slide level'}
slide_data_list = {
    'dice':
        {
            '1-tom': [0.943188165, 0.961079137, 0.953428156, 0.934357092, 0.933479359, 0.956694982, 0.967721166,
                      0.933724396,
                      0.96592582, 0.965591155],
            '2-gleb': [0.952393116, 0.959397398, 0.951393511, 0.928915237, 0.926595914, 0.944041508, 0.968221226,
                       0.931576114,
                       0.968755056, 0.968521052],
            '3-wgo': [0.953199401, 0.95804897, 0.953169426, 0.926983793, 0.927142513, 0.945892562, 0.9680104,
                      0.935391002,
                      0.969020473, 0.967366009],
            '4-dl': [0.947306437, 0.960884703, 0.954412276, 0.923693008, 0.933107576, 0.947617832, 0.96712454,
                     0.937107882,
                     0.965831476, 0.966191028],
            '5-df2': [0.941346549, 0.956528184, 0.952521864, 0.92435312, 0.929414823, 0.952783557, 0.962843223,
                      0.930907936,
                      0.961034402, 0.962762678]
        },
    'recall':
        {
            '1-tom': [0.970925027, 0.976576622, 0.957900326, 0.925077842, 0.940247264, 0.951788203, 0.98073709,
                      0.936513533,
                      0.986834767, 0.975264422],
            '2-gleb': [0.971597264, 0.967761765, 0.949523745, 0.919829879, 0.921580618, 0.919853279, 0.978042208,
                       0.929255096,
                       0.985338446, 0.976697462],
            '3-wgo': [0.970736419, 0.966151386, 0.955430145, 0.923189017, 0.929370667, 0.924454622, 0.9782275,
                      0.949752007,
                      0.984654408, 0.976339429],
            '4-dl': [0.97277197, 0.974315405, 0.952385169, 0.921179507, 0.940634557, 0.943403175, 0.980633463,
                     0.941371297,
                     0.985799959, 0.97687656],
            '5-df2': [0.978186874, 0.976401924, 0.964576081, 0.945606181, 0.945032876, 0.954610658, 0.986160451,
                      0.942748206,
                      0.990072082, 0.983927639]
        },
    'precision':
        {
            '1-tom': [0.916992031, 0.946065835, 0.94899755, 0.943824385, 0.926808189, 0.961652614, 0.9550462,
                      0.930951824,
                      0.945884522, 0.956107894],
            '2-gleb': [0.933933415, 0.951176379, 0.953270655, 0.938181862, 0.931666095, 0.969536187, 0.958595517,
                       0.933908756,
                       0.952720628, 0.960480402],
            '3-wgo': [0.936284775, 0.950081322, 0.950919381, 0.930809895, 0.924925018, 0.968348391, 0.958004519,
                      0.921457827,
                      0.953875237, 0.958556035],
            '4-dl': [0.923140181, 0.947819245, 0.956448031, 0.926220263, 0.925700102, 0.951870316, 0.953982751,
                     0.93288291,
                     0.9466559, 0.955736733],
            '5-df2': [0.907180457, 0.937447328, 0.94076521, 0.904034409, 0.914304599, 0.950963436, 0.940603173,
                      0.919361389,
                      0.933651474, 0.942489088]
        },
}

data_types = ['dice', 'recall', 'precision']
glom_data_list = {
    'dice': {},
    'recall': {},
    'precision': {},
}
for team in team_names:
    file_path = target_root_path + rf"\{team}.txt"
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        glom_data_list['dice'][team] = [float(line.split(',')[0]) for line in lines if len(line) > 1]
        glom_data_list['recall'][team] = [float(line.split(',')[1]) for line in lines if len(line) > 1]
        glom_data_list['precision'][team] = [float(line.split(',')[2]) for line in lines if len(line) > 1]
    # matching_data_list[team] = []

print(glom_data_list)

# display box and scatter plot along with violin plot
# fig = pt.violin(n_data, y="distance", x="Age", color="Skin Type",
#                 box=True, hover_data=n_data.columns,
#                 points='all',
#                 )
# fig = go.Figure()

fig = make_subplots(
    rows=3, cols=1,
    row_heights=[0.5, 0.25, 0.25],
    # specs=[[{"type": "Scatter3d", "colspan": 4}, None, None, None],
    #        [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}]],
    shared_xaxes=True,
    vertical_spacing=0.02,
    # subplot_titles=[f'All', 'CD68 / Macrophage', 'T-Helper', 'T-Regulatory'],
    subplot_titles=[f'Dice coefficient', 'Recall', 'Precision', ],
    specs=[[{"secondary_y": False}],
           [{"secondary_y": False}],
           [{"secondary_y": False}], ]
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
        for level_type in ['glom', 'slide']:
            fig.add_trace(
                go.Violin(x=[team] * (len(glom_data_list[data_type][team])
                                      if level_type == 'glom' else len(slide_data_list[data_type][team])),
                          y=(glom_data_list[data_type][team]
                             if level_type == 'glom' else slide_data_list[data_type][team]),
                          name=team,
                          points="all", opacity=opacity_dict[level_type],
                          pointpos=point_position_dict[f'{team}-{level_type}'],
                          side=('positive' if level_type == 'slide' else 'negative'),
                          legendgroup=level_type, showlegend=True if data_type == 'dice' else False,
                          scalegroup='', scalemode='width',
                          jitter=0.05, marker_opacity=0.5, marker_size=2, line_width=2,
                          legendgrouptitle_text=legend_dict[level_type],
                          box_visible=True, box_fillcolor='white',
                          line_color=color_dict[f'{team}-{level_type}'], meanline_visible=True, ),
                secondary_y=False, row=data_types.index(data_type) + 1, col=1
            )

# fig.update_traces(# meanline_visible=False,
#                   scalemode='count')  # scale violin plot area with total count
fig.update_layout(
    title="Kidney - dice/recall/precision data  [glom level (~2000 matching gloms) \n/ slide level (10 slides)]",
    # x1axis_title="Age",
    # yaxis_title="Dice",
    violingap=0.3, violingroupgap=0,
    violinmode='overlay',
    yaxis_zeroline=False)
# fig.update_yaxes(title_text="glom level (~2000 gloms) \n/ slide level (10 slides)", )
fig.update_yaxes(title_text="Dice", row=1, col=1)
fig.update_yaxes(title_text="Recall", row=2, col=1)
fig.update_yaxes(title_text="Precision", row=3, col=1)


fig.write_html(os.path.join(target_root_path, f"result.html"))
fig.show()
