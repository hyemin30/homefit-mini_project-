$(document).ready(function () {
    $.ajax({
                type: "GET",
                url: "/getcookie",
                data: {},
                success: function (response) {
                    let user = response['user'];
                    if (user == null) {
                        alert('로그인하세요');
                        document.location = '/'
                    }
                }
            })

    show_navbar()
});

function reservation(num) {
     $.ajax({
        type: "GET",
        url: "/getcookie",
        data: {},
        success: function (response) {
            let user = response['user'];
            if (user == 'normal') {
                $.ajax({
                    type: "POST",
                    url: "/tutors/reservation",
                    data: {'num_give': num},
                    success: function (response) {
                        location.href = "/tutors/reservation"
                    }
                });
            } else {
                alert('일반회원만 이용 가능합니다')
            }
        }
    })




}


//예약조회화면이동
function reservation_list() {
    location.href = "/reservation/list"
}

//수업스케줄등록화면
function timetables() {
    $.ajax({
        type: "GET",
        url: "/timetables",
        data: {},
        success: function (response) {
            if (response['msg'] == undefined) {
                location.href = '/timetables';
            } else {
                alert(response["msg"])
            }
        }
    });
}

// 스케줄 등록하기
function schedule() {
    let date = $('#date').val()
    let time = $('#time').val()
    console.log('날짜는' + date)
    console.log(time)
    if (date == '' || time == '수업시간 선택') {
        alert('날짜와 시간을 선택하세요');
    } else {
        $.ajax({
            type: "POST",
            url: "/timetables",
            data: {'date_give': date, 'time_give': time},
            success: function (response) {
                if (response['msg'] == '이미 등록하였습니다') {
                    alert(response["msg"])
                } else {
                    alert(response["msg"])
                }
            }
        });
    }
}

//회원, 강사 구분
function check_member() {
    $.ajax({
        type: "GET",
        url: "/checkmember",
        data: {},
        success: function (response) {
            let msg = response['msg']
            document.cookie = "user=" + msg;
        }
    })
}

function show_navbar() {
    $.ajax({
        type: "GET",
        url: "/getcookie",
        data: {},
        success: function (response) {
            $('#nav-item').empty()
            let user = response['user']
            if (user == 'normal') {
                temp_html = `<li class="nav-item">
                                <a class="nav-link nav-right" href="/main">강사검색</a>
                            </li>
                              <li class="nav-item">
                                <a class="nav-link  nav-right" href="reservation/list">예약조회</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link  nav-right" href="/advise">상담하기</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link nav-right" onclick="logout()">로그아웃</a>
                            </li>`
                $('#nav-item').append(temp_html)
            } else if (user == 'tutor') {
                temp_html = `
                              <li class="nav-item">
                                <a class="nav-link  nav-right" href="reservation/list">예약조회</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link  nav-right" onclick="timetables()">수업등록</a>
                
                            </li>
                            <li class="nav-item">
                                <a class="nav-link  nav-right" href="/profile"">프로필수정</a>
                
                            </li>
                            <li class="nav-item">
                                <a class="nav-link nav-right" onclick="logout()">로그아웃</a>
                            </li>`
                $('#nav-item').append(temp_html)

            }
        }
    })
}

function logout() {
     $.ajax({
        type: "GET",
        url: "/logout",
        data: {},
        success: function (response) {
            location.href = "/"
        }
    });
}