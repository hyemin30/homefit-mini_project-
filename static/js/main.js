function reservation(num) {
    $.ajax({
        type: "POST",
        url: "/tutors/reservation",
        data: {"num_give": num},
        success: function (response) {
            location.href = "/tutors/reservation"
        }
    })
}

function show_timetables() {
    let date = $('#date').val()
    let select_date = new Date(date)
    let today = new Date();
    if (date == '' || select_date <= today ) {
        alert('예약은 하루 전까지만 가능합니다')
    } else {
        $('#timetables').empty();

        $.ajax({
            type: 'POST',
            url: '/reservation',
            data: {'date_give': date},
            success: function (response) {
                let rows = response['timetables']
                if (rows.length == 0) {
                    alert('예약 가능한 시간이 없습니다');
                } else {
                    for (let i = 0; i < rows.length; i++) {
                        let time = rows[i]['time'];
                        let temp_html = `                  
                   <button class="btn btn-outline-warning" onclick="reservation_confirm('${time}')">${time}</button>
                `
                        $('#timetables').append(temp_html);
                    }
                }
            }
        });
    }
}

function reservation_confirm(time) {
    let date = $('#date').val()
    alert(date + ' ' + time + '시 수업을 예약합니다')
       $.ajax({
        type: "POST",
        url: "/reservation/confirm",
        data: {"time_give": time, 'date_give': date},
        success: function (response) {
            if (response['msg'] == '예약 완료') {
                location.href = "/reservation/list"
            } else {
                alert(response["msg"])
            }

        }
    })
}

//예약조회화면이동
function reservation_list() {
    location.href = "/reservation/list"
}

//수업스케줄등록화면
function timetables(){
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
function schedule(){
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
            data: {'date_give':date, 'time_give':time},
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