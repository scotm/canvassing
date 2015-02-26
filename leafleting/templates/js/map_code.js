/**
 * Created by scotm on 26/02/15.
 */
var data = {{ object.get_simplified_geom_json | safe}};
var points = [];
var markers = [];

var mapboxTiles = L.tileLayer('	http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg?', {
    attribution: '© OpenStreetMap contributors - <a href="http://www.opendatacommons.org/licenses/odbl">Terms</a>'
});
var map = L.map('map')
        .addLayer(mapboxTiles)
        .setView([{{ object.centre_point.0 }}, {{ object.centre_point.1}}], 14);
L.geoJson(data, {}).addTo(map);

function redrawMarkers() {
    if (map.getZoom() >= 16) {
        m = map.getBounds();
        $.ajax({
                    url: '/ajax/get_domeciles',
                    cache: false,
                    data: {'BBox': m.toBBoxString(), '{% block object_type %}region{% endblock %}': {{object.pk}}},
                    success: function (data, textStatus, jqXHR) {
                        points = data['data'];
                        markers.forEach(function (entry) {
                            map.removeLayer(entry)
                        });

                        points.forEach(function (entry) {
                            var marker = L.marker([entry['point'][1], entry['point'][0]], {'title': entry['postcode']});
                            markers.push(marker);
                            map.addLayer(marker)
                        });

                    }
                }
        );
    } else {
        points = [];
        markers.forEach(function (entry) {
            map.removeLayer(entry)
        });
    }

}

// Add the event handlers
map.on('zoomend', redrawMarkers);
map.on('dragend', redrawMarkers);

