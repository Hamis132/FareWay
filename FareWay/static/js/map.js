function Map(attractions) {
    var self = this;
    this.MARKER_ICON = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 7,
        fillColor: 'lightgrey',
        strokeColor: "grey",
        fillOpacity: 1
    };
    var INFO_WINDOW_TIMEOUT = 700;

    this.onSelect = null;
    this.onDeselect = null;

    this.attractions = attractions;
    this.distanceMatrixService = new google.maps.DistanceMatrixService();
    this.directionsService = new google.maps.DirectionsService();
    this.directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true
    });
    this.map = new google.maps.Map($('#map')[0], {
        disableDoubleClickZoom: true
    });
    self.map.fitBounds(getBounds(self.attractions));
    self.attractions.forEach(function (attraction) {
        attraction.fields.marker.setMap(self.map);
        attraction.fields.marker.addListener('click', function () {
            self.selectAttraction(attraction);
        });
        var infoWindow = new google.maps.InfoWindow({
            content: "<b>" + attraction.fields.name + "</b>" +
            "<br/>cena: " + attraction.fields.price +
            "<br/>czas: " + attraction.fields.time
        });
        var mouseout;
        attraction.fields.marker.addListener('mouseover', function () {
            mouseout = false;
            window.setTimeout(function () {
                if (!mouseout) {
                    infoWindow.open(self.map, attraction.fields.marker);
                }
            }, INFO_WINDOW_TIMEOUT);
        });
        attraction.fields.marker.addListener('mouseout', function () {
            mouseout = true;
            window.setTimeout(function () {
                if (mouseout) {
                    infoWindow.close();
                }
            }, INFO_WINDOW_TIMEOUT);
        });
    });
    self.selectAttraction(null);
    self.clearDirections();
    self.map.addListener('click', function () {
        self.selectAttraction(null);
    });
    self.map.addListener('dblclick', function () {
        self.map.fitBounds(getBounds(self.attractions));
    });

    function getBounds(attractions) {
        debugger;
        var lats = [], lngs = [];
        attractions.forEach(function (attraction) {
            lats.push(attraction.fields.position.lat);
            lngs.push(attraction.fields.position.lng);
        });
        return new google.maps.LatLngBounds({
            lat: Math.min.apply(null, lats),
            lng: Math.min.apply(null, lngs)
        }, {
            lat: Math.max.apply(null, lats),
            lng: Math.max.apply(null, lngs),
        });
    }
}

Map.prototype.selectAttraction = function (selectedAttraction) {
    var self = this;
    self.attractions.forEach(function (attraction) {
        attraction.fields.marker.setOpacity(0.6);
    });
    if (selectedAttraction) {
        selectedAttraction.fields.marker.setOpacity(1);
        if (self.onSelect) {
            self.onSelect(selectedAttraction);
        }
    } else if (self.onDeselect) {
        self.onDeselect();
    }
};

Map.prototype.clearDirections = function () {
    var self = this;
    this.attractions.forEach(function (attraction) {
        attraction.fields.marker.setLabel(null);
        attraction.fields.marker.setIcon(self.MARKER_ICON);
        self.directionsRenderer.setDirections({routes: []});
    });
};

Map.prototype.drawDirections = function (attractions, start, end, callback) {
    var self = this;
    self.clearDirections();
    self.directionsRenderer.setMap(this.map);
    var attr = [];
    attractions.forEach(function (a) {
        attr.push(a);
    });
    if (attr.indexOf(start) === -1 && start) {
        attr.push(start);
    }
    if (attr.indexOf(end) === -1 && end) {
        attr.push(end);
    }
    attr.forEach(function (attraction) {
        attraction.fields.marker.setIcon(null);
    });
    if (attr.length < 2) {
        if (callback) {
            callback(attr, 0, 0);
        }
        return;
    }
    if (!start || !end) {
        var places = [];
        attr.forEach(function (attraction) {
            places.push(attraction.fields.marker.getPosition());
        });
        self.distanceMatrixService.getDistanceMatrix({
            origins: places,
            destinations: places,
            travelMode: google.maps.TravelMode.WALKING
        }, function (res, status) {
            console.log(res, "DistanceMatrixService result");
            var max = 0;
            var a, b;
            for (var row = 0; row < res.rows.length; row++) {
                for (var element = 0; element < res.rows[row].elements.length; element++) {
                    var dist = res.rows[row].elements[element].distance.value;
                    if (dist > max) {
                        max = dist;
                        a = attr[row];
                        b = attr[element];
                    }
                }
            }
            if (!start) {
                start = a === end ? b : a;
            }
            if (!end) {
                end = a === start ? b : a;
            }
            draw();
        });
    } else {
        draw();
    }

    function draw() {
        var waypoints = [];
        attr.forEach(function (attraction) {
            if (attraction !== start && attraction !== end) {
                waypoints.push({
                    location: attraction.fields.marker.getPosition()
                });
            }
        });
        var request = {
            origin: start.fields.marker.getPosition(),
            destination: end.fields.marker.getPosition(),
            waypoints: waypoints,
            optimizeWaypoints: true,
            travelMode: google.maps.TravelMode.WALKING
        };
        self.directionsService.route(request, function (res, status) {
            self.directionsRenderer.setDirections(res);
            console.log(res, "DirectionsService result");
            var route = getRoute(res);
            console.log(route, attr)
            for (var i = 0; i < route.length; i++) {
                route[i].fields.marker.setLabel(String.fromCharCode('A'.charCodeAt(0) + i));
            }
            if (callback) {
                var distance = 0, duration = 0;
                res.routes[0].legs.forEach(function (leg) {
                    distance += leg.distance.value;
                    duration += leg.duration.value;
                });
                callback(route, distance, duration);
            }
        });
    }

    function getRoute(directionsServiceResult) {
        var route = [start];
        if (attr.indexOf(start) !== -1) attr.splice(attr.indexOf(start), 1);
        if (attr.indexOf(end) !== -1) attr.splice(attr.indexOf(end), 1);
        var order = directionsServiceResult.routes[0].waypoint_order;
        for (var i = 0; i < order.length; i++) {
            route[order[i] + 1] = attr[i];
        }
        if (start !== end) route.push(end);
        return route;
    }
};