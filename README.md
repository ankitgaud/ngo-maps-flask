<h1 style="text-align: center;"><u>MAP-PROJECT</u></h1>
<h3><u>Implementation Details:</u></h3>
<ul>
  <li>Languages: Python, Javascript</li>
  <li>Frameworks: flask, flask-googlemaps, pandas, requests, PIL, IO</li>
</ul>
<br>
<h3><u>Tasks Completed:</u></h3>
<ul>
  <li>Pick your favourite india map/graph library</li>
  <li>(PFA the the list of NGO’s) Plot all of them on the map.</li>
  <li>Provide toggles to filter on NGO/Charity/Map.</li>
  <li>Different stuff on different zoom levels. 5000 entries, at no point should there be more than
200 items on map (pick by level and then display in decreasing order of quality rating). If
quality rating is changed (indicate slider), hide/show points accordingly.</li>
  <li>Name code should be visible on hover</li>
  <li><b><u>Bonus:</u></b> Use APIs to identify agencies on "water". Mark them as invalid.</li>
</ul>
<br>
<h3><u>Installation:</u></h3>
<ul>
  <li>Use pip or conda to install all above python-libraries</li>
  <li>Run python File</li>
  <li>Access on localhost:5000/</li>
</ul>
<h3><u>FUnctions:</u></h3>
<ul>
  <li>Custom zoom slider based on visibility level to show points, higher visibility tends to show
on zoom out
<img src="https://github.com/ankitgaud/ngo-maps-flask/blob/master/pic1.PNG" height="380" width="650" title="hover text"></li>
  <li> All water points filtered out with pixel detection from static google map without external api.</li>
  <li>Based on Quality and Zoom, adjust points dynamically with color of each <b>ngo types</b> with 200 Limit</li>
  <li>Front-end is not much polished.
  <img src="https://github.com/ankitgaud/ngo-maps-flask/blob/master/pic2.PNG" height="380" width="650" title="hover text"></li>
</ul>
