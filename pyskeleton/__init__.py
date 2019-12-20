from flask import Flask, render_template, request
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.iris import flowers

app = Flask(__name__)

feature_names = flowers.columns[0:-1].values.tolist()

# Create the main plot
def create_figure(current_feature_name_one, current_feature_name_two):
	colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
	colors = [colormap[x] for x in flowers['species']]

	p = figure(title = "Iris Morphology")
	p.xaxis.axis_label = current_feature_name_one
	p.yaxis.axis_label = current_feature_name_two

	p.circle(flowers[current_feature_name_one], flowers[current_feature_name_two],
		 color=colors, fill_alpha=0.2, size=10)
	return p

# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_name_one = request.args.get("feature_name_one")
	current_feature_name_two = request.args.get("feature_name_two")
	if current_feature_name_one == None:
		current_feature_name_one = feature_names[0]
	if current_feature_name_two == None:
		current_feature_name_two = feature_names[0]

	# Create the plot
	plot = create_figure(current_feature_name_one,current_feature_name_two)

	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("index.html", script=script, div=div,
		feature_names=feature_names,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)
