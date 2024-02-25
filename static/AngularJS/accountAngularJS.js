var app = angular.module("account-app", [])

app.controller("account-ctrl", function ($scope, $http, $window) {

//     register
    $scope.register = function () {
        const data = {
            email: $scope.email,
            password: $scope.password,
            name: $scope.name,
            verificationCode: $scope.code
        }
        $http.post("http://127.0.0.1:5000/OnlineClass/register-account", data).then(r => {
            alert("Thêm thành công")
            $window.location.href = 'http://127.0.0.1:5000/onlineClass/login';
        })
    }

    $scope.sendVerificationCode = function () {
        const email = $scope.email
        console.log($scope.email)
        $http.post("http://127.0.0.1:5000/OnlineClass/send-Verification-code/" + email).then(r => {
            alert("Gửi mã xác nhận thành công")
        })
    }

    $scope.login = function () {
        const account = {
            email: $scope.emailLogin,
            password: $scope.passwordLogin
        }
        $http.post("http://127.0.0.1:5000/OnlineClass/login", account).then(r => {
            $scope.districts = r.data;
            $window.location.href = 'http://127.0.0.1:5000/onlineClass/home';
            alert("Đăng nhập thành công")
        })
    }


})