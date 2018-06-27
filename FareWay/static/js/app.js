(function () {
    console.log(ROUTE);
    var app = angular.module("guide", []).config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    });

    app.controller('GuideController', ['$http', '$scope', function ($http, $scope) {
        $scope.map = null;
        $scope.attractions = [];
        $scope.route = [];
        $scope.routeName = "Bez nazwy";
        $scope.selectedAttraction = null;
        $scope.distance = 0;
        $scope.duration = 0;
        $scope.start = null;
        $scope.end = null;

        $scope.updateMap = function () {
            var start = null, end = null;
            if ($scope.start) {
                start = $scope.route.filter(function (attraction) {
                    return attraction.pk === parseInt($scope.start);
                })[0];
            }
            if ($scope.end) {
                end = $scope.route.filter(function (attraction) {
                    return attraction.pk === parseInt($scope.end);
                })[0];
            }
            $scope.map.drawDirections($scope.route, start, end, function (newRoute, distance, duration) {
                $scope.$evalAsync(function () {
                    $scope.route = newRoute;
                    $scope.distance = distance;
                    $scope.duration = duration;
                });
            });
        };

        $scope.inRoute = function (attraction) {
            return $scope.route.indexOf(attraction) !== -1;
        };

        $scope.addToRoute = function (attraction) {
            $scope.route.push(attraction);
            $scope.updateMap();
        };

        $scope.removeFromRoute = function (attraction) {
            if ($scope.end === attraction.pk + "") {
                $scope.end = "";
            }
            if ($scope.start === attraction.pk + "") {
                $scope.start = "";
            }
            $scope.route.splice($scope.route.indexOf(attraction), 1);
            $scope.updateMap();
        };

        $scope.getSightseeingTime = function () {
            var time = 0;
            $scope.route.forEach(function (attraction) {
                time += timeToInt(attraction.fields.time);
            });
            return timeToString(time);
        };

        $scope.getTravelTime = function () {
            return timeToString($scope.duration);
        };

        $scope.getTotalTime = function () {
            return timeToString(timeToInt($scope.getSightseeingTime()) + $scope.duration);
        };

        $scope.getDistance = function () {
            return $scope.distance / 1000;
        };

        $scope.routeEmpty = function () {
            return $scope.route.length === 0;
        };

        $scope.submitRoute = function () {
            if (!$scope.routeName) { // TODO: wyswietlic jakis komunikat
                return;
            }
            if ($scope.route.length === 0) { // TODO: tutaj też
                return;
            }
            var data = {
                name: $scope.routeName,
                start: $scope.start ? parseInt($scope.start) : null,
                end: $scope.end ? parseInt($scope.end) : null,
                attractions: $scope.route.slice(0).map(function (atr) {
                    return atr.pk;
                })
            };
            if(ROUTE.pk){
                data.pk = parseInt(ROUTE.pk);
            }
            console.log(data, "DATA");
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                    }
                }
            });
            $.ajax({
                url: "/routes/update/",
                type: "POST",
                data: data,
                complete: function () {
                    window.location.replace("/routes/");
                }
            });
        };

        $http.get('/attractions/').success(function (attractions) {
            $http.get('/categories/').success(function (cat) {
                attractions.forEach(function (attraction) {
                    var myLatLng = new google.maps.LatLng(attraction.fields.latitude, attraction.fields.longitude);
                    var Numers = {lat: attraction.fields.latitude, lng: attraction.fields.longitude};
                    attraction.fields.position = Numers;

                    attraction.fields.marker = new google.maps.Marker({
                        position: myLatLng
                    });
                    var category = cat.filter(function (c) {
                        return c.pk === attraction.fields.category;
                    })[0];
                    attraction.fields.category = category.fields.name;
                    attraction.fields.price = parseFloat(attraction.fields.price);

                });
                console.log(attractions, "ATTRACTIONS");//////////////////////
                $scope.attractions = attractions;
                $scope.map = new Map(attractions);
                $scope.map.onSelect = function (attraction) {
                    $scope.$evalAsync(function () {
                        $scope.selectedAttraction = attraction;
                    });
                };
                $scope.map.onDeselect = function () {
                    $scope.$evalAsync(function () {
                        $scope.selectedAttraction = null;
                    });
                };
                if (ROUTE.name) {
                    $scope.routeName = ROUTE.name;
                }
                $scope.start = ROUTE.start ? ROUTE.start + "" : "";
                $scope.end = ROUTE.end ? ROUTE.end + "" : "";
                $scope.route = ROUTE.attractions.slice(0).map(function (pk) {
                    return $scope.attractions.filter(function (atr) {
                        return atr.pk === pk;
                    })[0];
                });
                $scope.updateMap();
                console.log($scope.route, "$scope.route")
            });
        });
    }]);
})();

function timeToString(time) {
    var hms = [time / 3600, (time % 3600) / 60, time % 60].map(function (x) {
        return ("0" + parseInt(x)).slice(-2);
    });
    return hms[0] + ":" + hms[1] + ":" + hms[2];
}

function timeToInt(time) {
    var hms = time.split(":").map(function (x) {
        return parseInt(x);
    });
    return hms[0] * 3600 + hms[1] * 60 + hms[2];
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}