$(document).ready(function () {
    show_reservations();
});

function show_reservations() {
    $('#reservation-list').empty();
    $.ajax({
        type: "GET",
        url: "/reservation/show",
        data: {},
        success: function (response) {
            let rows = response['reservations']
            for (let i = 0; i < rows.length; i++) {
                let date = rows[i]['date']
                let time = rows[i]['time']
                let member = rows[i]['member']
                let tutor = rows[i]['tutor']
                let num = rows[i]['num']
                let temp_html = ``

                if (response['msg'] == '일반회원') {
                    temp_html = `
                    <div class="reservation-card" style="max-width: 250px;">
                        <div class="card bg-purple">
                            <div class="card-body reservation-content">
                                <h5 class="card-header border-light  mb-3">${date}</h5>
                                <h5 class="card-title">강사 : ${tutor}</h5>
                                <h5 class="card-title">시간 : ${time}</h5>
                                <a href="#" class="btn btn-sm btn-cancel" onclick="cancel(${num})">예약취소</a>
                            </div>
                        </div>
                    </div>`
                    $('#reservation-list').append(temp_html);
                } else {
                    temp_html = `
                    <div class="reservation-card" style="max-width: 250px;">
                        <div class="card bg-purple">
                            <div class="card-body reservation-content">
                                <h5 class="card-header border-light  mb-3">${date}</h5>
                                <h5 class="card-title">회원 : ${member}</h5>
                                <h5 class="card-title">시간 : ${time}</h5>
                                <a href="#" class="btn btn-sm btn-cancel" onclick="cancel(${num})">수업취소</a>
                            </div>
                        </div>
                    </div>`
                    $('#reservation-list').append(temp_html);
                }
            }
        }
    })
}

function cancel(num) {
    $.ajax({
        type: 'POST',
        url: '/reservation/cancel',
        data: {'num_give': num},
        success: function (response) {
            alert(response['msg'])
            location.reload();
        }
    });
}