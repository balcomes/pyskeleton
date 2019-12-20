from flask import Flask, render_template, request
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.iris import flowers

app = Flask(__name__)

feature_names = flowers.columns[0:-1].values.tolist()

# Create the main plot
def create_figure(current_feature_name):
	colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
	colors = [colormap[x] for x in flowers['species']]

	p = figure(title = "Iris Morphology")
	p.xaxis.axis_label = current_feature_name
	p.yaxis.axis_label = 'Petal Width'

	p.circle(flowers[current_feature_name], flowers["petal_width"],
		 color=colors, fill_alpha=0.2, size=10)
	return p

# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	if current_feature_name == None:
		current_feature_name = feature_names[0]

	# Create the plot
	plot = create_figure(current_feature_name)

	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("index.html", script=script, div=div,
		feature_names=feature_names,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)
