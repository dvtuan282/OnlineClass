var app = angular.module("class-app", [])
app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
app.controller("class-ctrl", function ($scope, $http, $window, $filter, $interval) {
    $scope.dc = 'dddd';
    const pathName = location.pathname;
    $scope.idClass = pathName.substring(pathName.lastIndexOf("/") + 1)
    // class for account
    $scope.a = function () {
        $http.get("http://127.0.0.1:5000/OnlineClass/list-class-of-account").then(resp => {
            console.log(resp.data)
            $scope.lisClassOfAccount = resp.data;
        }).catch(error => {
            console.log(error)
        })
    }
    // information class
    $http.get("http://127.0.0.1:5000/OnlineClass/informationClass/" + $scope.idClass).then(resp => {
        $scope.inforClass = resp.data;
    }).catch(error => {
        console.log(error)
    })

    //========POST==========//
    // list post in class
    $scope.listPost = function () {
        $http.get("http://127.0.0.1:5000/OnlineClass/list-post-in-class/" + $scope.idClass).then(resp => {
            $scope.listPostInClass = resp.data;
        }).catch(error => {
            console.log(error)
        })
    }

    $scope.listPost()
    // create post
    $scope.createPost = function () {
        const data = {
            content: $scope.content,
            classOn: $scope.idClass
        }
        $http.post("http://127.0.0.1:5000/OnlineClass/create-post", data).then(r => {
            $scope.listPost()
            $scope.content = ''
        })
    }

    // delete post
    $scope.deletePost = function (idPost) {
        $http.delete("http://127.0.0.1:5000/OnlineClass/delete-post/" + idPost).then(r => {
            $scope.listPost()
        })
    }
    // information post
    $scope.idPost = ''
    $scope.informationPost = function (idPost) {
        $http.get("http://127.0.0.1:5000/OnlineClass/information-post/" + idPost).then(r => {
            const post = r.data
            $scope.contentEdit = post.content
            $scope.idPost = post.id
        })
    }
    // edit post
    $scope.updatePost = function () {
        const data = {
            content: $scope.contentEdit
        }
        $http.put("http://127.0.0.1:5000/OnlineClass/update-post/" + $scope.idPost, data).then(r => {
            $scope.contentEdit = ''
            $scope.listPost()
        })
    }
    // ========COMMENT=======//
    // create comment
    // $scope.createComment = function(idPost) {
    //     console.log('aa', $scope.comment);
    //     // Thực hiện các bước xử lý khác ở đây nếu cần
    // };
    $scope.comment = '';
    $scope.createComment = function (idPost) {
        var data = {
            content: $scope.content
        };
        $http.post("http://127.0.0.1:5000/OnlineClass/comment/" + idPost, data).then(r => {
            $scope.listPost();
        });
    };

    $scope.deleteComment = function (idComment) {
        $http.delete("http://127.0.0.1:5000/OnlineClass/comment/" + idComment).then(r => {
            $scope.listPost();
        });
    }

    // ========== ClassMember ============//
    //show member in class
    $scope.listMember = function () {
        $http.get("http://127.0.0.1:5000/OnlineClass/member/" + $scope.idClass).then(r => {
            $scope.memberInClass = r.data;
            console.log(r.data)
        })
    }
    $scope.listMember()

    $scope.deleteMember = function (idClassMember) {
        $http.delete("http://127.0.0.1:5000/OnlineClass/member/" + idClassMember).then(r => {
            $scope.listMember()
        });
    }
    $scope.accounts = [];
    $scope.addMember = function () {
        // Kiểm tra xem có option nào được chọn không
        if ($scope.accounts.length === 0) {
            alert('Vui lòng chọn ít nhất một email.');
            return;
        }
        let data = {
            accounts: $scope.accounts,
            classOn: $scope.idClass
        }
        $http.post("http://127.0.0.1:5000/OnlineClass/member", data).then(r => {
            alert('Thành công');
        })
    };
    // upload file list member add class
    $scope.uploadFile = function () {
        var fileInput = document.getElementById('fileInput');
        var file = fileInput.files[0];

        if (file) {
            var formData = new FormData();
            formData.append('file', file);

            $http.post('http://127.0.0.1:5000/OnlineClass/create-members/' + $scope.idClass, formData, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            }).then(function (response) {
                alert('Thành công');
                $scope.listMember()
                fileInput = ''
            }, function (error) {
                console.error('Error uploading file:', error);
            });
        } else {
            console.error('No file selected.');
        }
    };
    // =========== Lời mời tham gia ===========//
    $scope.showListInvitation = function () {
        $http.get('http://127.0.0.1:5000/OnlineClass/listInvitation').then(r => {
            $scope.listInvitation = r.data
            console.log('sad:', r.data)
        })
    }
    $scope.showListInvitation()
    $scope.confirmJoinClass = function (idClassMember) {
        $http.put('http://127.0.0.1:5000/OnlineClass/member/' + idClassMember).then(r => {
            $scope.showListInvitation()
        })
    }
// ========Quizz======//
    $scope.showQuizz = function () {
        $http.get('http://127.0.0.1:5000/OnlineClass/quizz-class/' + $scope.idClass).then(r => {
            $scope.listQuizz = r.data
        })
    }
    $scope.showQuizz()
    $scope.toDate = function (data) {
        // Parse the input string into a JavaScript Date object
        const myDate = new Date(data);

        // Use AngularJS date filter to format the date
        return $filter('date')(myDate, 'yyyy-MM-ddTHH:mm:ss');
    };

    // create quizz
    $scope.classOnQuizz = []

    $scope.createQuizz = function () {
        const formData = new FormData()
        var fileInput = document.getElementById('fileCauHoi');
        var file = fileInput.files[0];
        formData.append('title', $scope.titleQuizz);
        formData.append('openTime', $scope.toDate($scope.ngayBatDau));
        formData.append('closedTime', $scope.toDate($scope.ngayHetHan));
        formData.append('testTime', $scope.thoiGianLamBai);
        formData.append('image', $scope.imageQuizz);
        formData.append('listClassShare', $scope.classOnQuizz);
        formData.append("fileQuestion", file)
        $http.post('http://127.0.0.1:5000/OnlineClass/quizz/' + $scope.idClass, formData, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        }).then(r => {
            alert("Thành công")
            $scope.showQuizz()
        })
    }

//     Show infor quizz
    $scope.thongTinQuizz = function (idQuizz) {
        $http.get('http://127.0.0.1:5000/OnlineClass/quizz/' + idQuizz).then(r => {
            $scope.infQuizz = r.data
        })
    }
    //     đồng hồ bấm giờ
    $scope.formattedTime = "00:00:00";
    $scope.timerInterval = null;
    $scope.startCountdown = function (durationInSeconds) {
        const startTime = new Date().getTime();
        const endTime = startTime + durationInSeconds * 60 * 1000;

        function updateTimer() {
            const currentTime = new Date().getTime();
            const remainingTime = endTime - currentTime;

            if (remainingTime >= 0) {
                const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

                $scope.formattedTime = formatTime(hours) + ":" + formatTime(minutes) + ":" + formatTime(seconds);
            } else {
                $scope.formattedTime = "00:00:00";
                $interval.cancel($scope.timerInterval);
            }
        }

        function formatTime(value) {
            return value < 10 ? "0" + value : value;
        }

        updateTimer(); // Initial call to set the timer immediately

        $scope.timerInterval = $interval(updateTimer, 1000); // Update every second

    };
//     show question In quizz
    $scope.showQuestionInQuizz = function (idQuizz, timeTest) {
        $http.get('http://127.0.0.1:5000/OnlineClass/quizz-question/' + idQuizz).then(r => {
            $scope.listQuestion = r.data
            $scope.startCountdown(45)
        })
    }
    // hàm lấy vào radio name khi click vào radio
    $scope.clickRadioAnswer = function (radioGroupName) {
        return radioGroupName;
    }
    // hàm kiểm tra radio đã chọn hay chưa
    $scope.isRadioSelected = function (radioGroupName) {
        const radios = document.getElementsByName(radioGroupName);
        for (var i = 0; i < radios.length; i++) {
            if (radios[i].checked) {
                return true;
            }
        }
        return false;
    };

});
