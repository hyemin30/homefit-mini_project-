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
    $('#timetables').empty()

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
                   <button class="btn btn-primary" onclick="reservation_confirm('${time}')">${time}</button>
                `
                    $('#timetables').append(temp_html);
                }
            }
        }
    });
}

function reservation_confirm(time) {
    let date = $('#date').val()
    alert(date + ' ' + time + '수업을 예약합니다')
       $.ajax({
        type: "POST",
        url: "/reservation/confirm",
        data: {"time_give": time, 'date_give': date},
        success: function (response) {
            location.href = "/reservation/list"
        }
    })
}


//수업스케줄등록
function timetables(){
    alert('수업등록확인')
        $.ajax({
        type: "GET",
        url: "/timetables",
        data: {},
        success: function (response) {
            alert(response["msg"])
        }
    });
}