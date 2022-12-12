$(document).ready(function () {
    show_profile();
});


function show_profile() {
   $.ajax({
        type: "GET",
        url: "/tutors/reservation/profile",
        data: {},
       success: function (response) {
           let tutor = response['tutor']
           console.log(tutor)
           let img = tutor[0]['img']
            let id = tutor[0]['id']

            temp_html = `  <img  src="${img}"
                         class="img-fluid" alt="tutor_name"><br><br>
                        <h5> ${id} 강사 시간표</h5>`

            $('#reservation-profile').append(temp_html)
        }
    })

}

function show_timetables() {
    let date = $('#date').val()
    let select_date = new Date(date)
    let today = new Date();
    if (date == '' || select_date <= today) {
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
                   <button class="btn btn-time" onclick="reservation_confirm('${time}')">${time}</button>
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
