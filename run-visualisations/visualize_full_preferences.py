import pandas as pd
import plotly.graph_objects as go
from constants import MORAL_VALUES
from mock_results import single_preference_var, single_preferences_dict, total_preference_dict

colors = {
    "GPT-3.5": 'rgb(236,36,0)',
    "GPT-4": 'rgb(255, 191, 0)',
    "GPT-4o": 'rgb(255,140,0)',
    "Claude-2": "rgb(128, 0, 255)",
    "Claude-3": "rgb(102,102, 253)",
    "Claude-3.5": "rgb(0, 128, 255)",
    "Llama-3-70b": "rgb(50, 128, 50)",
    "Llama-3.1-405b": "rgb(0, 100, 0)",
    "Gemini-1.5-Flash": "rgb(88, 57, 39)",
}

def get_error_bars(single_pref_dict):
    pass

text_size = 30
def dot_plot_results(results_dict):
    fig = go.Figure()
    # colors = ["yellow", "gold", "crimson", "darkblue", "deeppink", "purple", "coral"]
    for model, prefs in results_dict.items():
        fig.add_trace(
            go.Scatter(
                x=prefs[0],
                y=[val.title() for val in MORAL_VALUES],
                marker=dict(size=13),
                mode="lines+markers",
                name=str(model),
                line=dict(shape='linear', color=colors[model]),
                error_x=dict(type='data',  # Set error bar type to data coordinates
                             array=prefs[1],
                             visible=True,
                             color=colors[model].replace('rgb(', 'rgba(').replace(')', f',{0.3})'),  # Set error bar color to a lighter gray
                             # thickness=20,  # Set error bar thickness to 1 pixel
                             # width=10,  # Set error bar line width for better visibility
                             symmetric=True,  # Set to false for asymmetric error bars
                             # errorbar = dict(shape='line')
                             copy_ystyle=False,
                             )
            )
        )

    fig.update_layout(
        # title="Single value preferences", #TODO: change
        plot_bgcolor='white',
        xaxis=dict(
            title="Answer matching behaviour, %",  # Set x-axis title
            titlefont=dict(
                size=text_size,  # Set the font size of the x-axis label
            ),
            showgrid=True,  # Show grid lines
        ),
        yaxis=dict(
            title="Moral Foundations",  # Set y-axis title
            titlefont=dict(
                size=text_size,  # Set the font size of the x-axis label
            ),
            showgrid=True,  # Show grid lines
            gridcolor='lightgrey'  # Set grid color to light grey
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=.54,
            xanchor="left",
            x=0.05,
            font=dict(size=20)
        )
    )
    fig.update_layout(xaxis_tickfont=dict(size=text_size), yaxis_tickfont=dict(size=text_size))
    fig.show()

if __name__ == "__main__":
    # single prefs
    new_dict = {}
    for model, pref in single_preferences_dict.items(): # i should be model name
         moral_values = []
         errors = []
         for moral_val, vals in pref.items():
             new = []
             for k, v in vals.items():
                 new += [k] * v
             new = pd.Series(new)
             bootstraped_vals = []
             for i in range(100):
                 shuffled = new.sample(n=len(new))
                 new_vals = shuffled.sample(n=300)
                 bootstraped_vals.append(new_vals.value_counts()["yes"]*100/300)
             stdev = float(pd.Series(bootstraped_vals).std()) *1.96
             values = int(vals["yes"]*100/1079)
             moral_values.append(values)
             errors.append(stdev)
         new_dict[model] = [moral_values, errors]
         # new_dict[model] = [int(vals["yes"]*100/1079) for k, vals in pref.items()]
    print(new_dict)
    dot_plot_results(new_dict)

    # new_dict = {}
    # for model, pref in total_preference_dict.items():  # i should be model name
    #     moral_values = []
    #     errors = []
    #     new = []
    #     for moral_val, vals in pref.items():
    #         new += [moral_val] * vals
    #     new = pd.Series(new)
    #     bootstraped_vals = {val: [] for val in MORAL_VALUES}
    #     for i in range(100):
    #         shuffled = new.sample(n=len(new))
    #         new_vals = shuffled.sample(n=300)
    #         for moral_val in MORAL_VALUES: # bootstarap std is over 100 examples not 6 values
    #             bootstraped_vals[moral_val].append(new_vals.value_counts()[moral_val] * 100 / 300)
    #     for moral_val in bootstraped_vals:
    #         stdev = float(pd.Series(bootstraped_vals[moral_val]).std())
    #         errors.append(stdev*1.96)
    #     values = [int(vals * 100 / 1079) for k, vals in pref.items()]
    #     moral_values.append(values)
    #     new_dict[model] = [values, errors]
    #     # new_dict[model] = [int(vals * 100 / 1079) for k, vals in pref.items()]
    # print(new_dict)
    # dot_plot_results(new_dict)

    # new_dict = {}
    # for model, pref in total_preference_dict.items():  # i should be model name
    #     new_dict[model] = [int(vals * 100 / 1079) for k, vals in pref.items()]
    # print(new_dict)
    # dot_plot_results(new_dict)

