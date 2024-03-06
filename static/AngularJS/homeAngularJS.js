var app = angular.module("home-app", []);
app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller("home-ctrl", function ($scope, $http, $window) {
    $scope.a = function () {
        $http.get("http://127.0.0.1:5000/OnlineClass/list-class-of-account").then(resp => {
            console.log(resp.data)
            $scope.lisClassOfAccount = resp.data;
        }).catch(error => {
            console.log(error)
        })
    }

    $scope.a()

    $http.get("http://127.0.0.1:5000/OnlineClass/list-of-class-involved").then(resp => {
        console.log(resp.data)
        $scope.listOfClassInvovled = resp.data;
    }).catch(error => {
        console.log(error)
    })

    $http.get("http://127.0.0.1:5000/OnlineClass/OnlineClass/information").then(resp => {
        console.log('account' + resp.data)
        $scope.account = resp.data;
    }).catch(error => {
        console.log(error)
    })

    $scope.createClass = function () {
        var data = {
            className: $scope.className
        }
        $http.post("http://127.0.0.1:5000/OnlineClass/create-class", data).then(r => {
            alert("Tạo lớp thành công")
            $scope.className = ""
            $('#staticBackdrop').modal('hide');
            $scope.a()
        })
    }
});
