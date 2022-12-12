function reservation(num) {
    $.ajax({
        type: "POST",
        url: "/tutors/reservation",
        data: {'num_give': num},
        success: function (response) {
            location.href = "/tutors/reservation"
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

