

from flask import Flask, render_template, request, jsonify
from flask_googlemaps import GoogleMaps, icons
from flask_googlemaps import Map
from flask_cors import CORS, cross_origin
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Flask Config
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['GOOGLEMAPS_KEY'] = "your_api_key"
GoogleMaps(app, key="your_api_key")

# Load List
df_ngo = pd.read_csv('./df_ngo.csv', header=[0])

# Config Params
display_limit_instance = 200
zoom_level = 4 # 4 to 15, min to max
quality_rating = "max"
range_quality = [1, 5]
list_ngo_type = ['all', 'NGO', 'Charity', 'Trust']
color_type = {'NGO':'http://maps.google.com/mapfiles/ms/icons/blue-dot.png', 'Trust':'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'Charity':'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'}

# Detect Water
def _not_water_(lat, lng):
    color_water = (163, 203, 255)
    
    response = requests.get("http://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lng)+"&zoom=15&size=1x1&maptype=roadmap&sensor=false&key=AIzaSyCneaKSXn025PON1aNr-kwqNi-87MS3H3M")
    img = Image.open(BytesIO(response.content))
    
    # Water Color, Could Skip
    if (img.convert('RGB').getpixel((0, 0))) == color_water:
        return False
    else:
        return True
    
# Write to CSV
# not_water_index = []

# for rows in df_ngo.iterrows():
#     value_w = _not_water_(rows[1]['LAT'], rows[1]['LONG'])
#     print(len(not_water_index)+1, value_w)
#     not_water_index.append(value_w)
#df_ngo['NOT_WATER'] = not_water_index
# print(df_ngo['NOT_WATER'][2162])
# print(df_ngo['name_code'][2162])
#df_ngo.to_csv('/home/abhishek/Project Notebooks/L_Map/df_ngo.csv')

# Returns Map Object based on Params

def _display_matx_ins(zoom_level, quality_rating, ngo_type):
    # Check Params
    if zoom_level < 4 or zoom_level > 15:
        zoom_level = 10
    if quality_rating < range_quality[0] or quality_rating > range_quality[1]:
        quality_rating = 2
    
    # New DF
    df_plot = pd.DataFrame()
    
    # Set Visibility From Map Zoom
    visibility_level = 5 - int((zoom_level-4)/2)
    
    # Visibility Level Check
    if visibility_level < 1:
        visibility_level = 1
    
    # List of Types
    for ngo in ngo_type:
        ngo = ngo.strip(' ')
        if (' '.join(list_ngo_type)).find(ngo) != -1: # Check for Type
            df_plot = df_plot.append(df_ngo[(df_ngo.visibility_level == visibility_level) & (df_ngo.Quality >= quality_rating) & (df_ngo.Type == ngo) & (df_ngo.Valid == True) & (df_ngo.NOT_WATER == True)])
    
    # Sort and Limit Values based on validity
    df_plot_sort = df_plot.sort_values(['Quality'], ascending=False)
    
    if len(df_plot_sort) > display_limit_instance:
        df_plot_sort = df_plot_sort.head(n=200)
        
    # Map Plot
    plot_map = Map(
        identifier="sndmap",
        varname="sndvar",
        zoom=zoom_level,
        zoom_control=False,
        style="height:800px;width:1200px;margin:100px;",
        lat=df_ngo['LAT'][0],
        lng=df_ngo['LONG'][1],
        markers=[{
             'icon': color_type[df_idx[1]['Type']],
             'lat': df_idx[1]['LAT'],
             'lng': df_idx[1]['LONG'],
             'infobox': "<b>"+ df_idx[1]['name_code'] +"</b>"
          } for df_idx in df_plot_sort.iterrows()]
    )
    return plot_map


@app.route("/")
def mainview():
    return render_template('map_index.html')

# For GET API
@app.route("/app")
def mapview():
    # creating a map in the view
    req_params = request.args.to_dict()
    return jsonify(_display_matx_ins(int(req_params['zoom_level']), int(req_params['quality']), req_params['type'].strip('[').strip(']').replace("'", '').strip(" ").split(',')).as_json())

if __name__ == "__main__":
    app.run(port=5001) 
