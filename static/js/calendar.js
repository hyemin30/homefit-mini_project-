const Day = document.querySelector('.day');
const month = document.querySelector('.month-name');
const date = new Date();

const pre = document.querySelector('.left');
const next = document.querySelector('.right');

const todoField = document.querySelector('.todo');
const todoTitle = document.querySelector('.todo-title');
const todoList = document.querySelector('.todoList');

const input = document.querySelector('input[type="text"]');
const add = document.querySelector('.add');
const reset = document.querySelector('.reset');
const allReset = document.querySelector('.allreset');


let currentMon = date.getMonth() + 1;
let currentYear = date.getFullYear();
let currentDay = date.getDate();

let DayOfChoice = currentDay;
let MonOfChoice = currentMon;
let yearOfChoice = currentYear;

let year = currentYear;
let mon = currentMon;

let clickEventArr = [];
let storeToDo = [];

function isLeapYear(year) {
    return (year % 4 == 0) && (year % 400 == 0 || year % 100 != 0);
}

function getDayOfMon(mon, year) {
    if (mon === 1 || mon === 3 || mon === 5 || mon === 7 || mon === 8 || mon === 10 || mon === 12) {
        return 31;
    } else if (mon === 2) {
        return isLeapYear(year) ? 29 : 28;
    } else {
        return 30;
    }
}

function getDay(year, mon, date) {
    const conYMD = year + '-' + mon + '-' + date;
    return (new Date(conYMD).getDay());
}

function makeCalendar(year, mon, dayCount) {
    clickEventArr = [];
    Day.innerHTML = '';
    let getFirstDay = getDay(year, mon, 1);
    let previousMon;
    if (currentMon - 1 < 0) {
        previousMon = 12;
    } else {
        previousMon = currentMon - 1;
    }
    let getDayOfPreMon = getDayOfMon(previousMon, year);
    for (let i = (getFirstDay + 6) % 7; i > 0; i--) {
        const listPre = document.createElement('li');
        listPre.textContent = `${getDayOfPreMon - (i - 1)}`;
        listPre.style.opacity = '0.5';
        listPre.classList.add('disabled');
        Day.appendChild(listPre);
    }

    for (let i = 1; i <= dayCount; i++) {
        if (i === currentDay && year === currentYear && mon === currentMon) {
            //선택한 년, 월, 일 다를 때 현재 날짜에 검은색 테두리
            const onlyOneList = document.createElement('li');

            onlyOneList.textContent = `${i}`;
            if (currentYear === yearOfChoice && currentMon === MonOfChoice && currentDay === DayOfChoice) {
                onlyOneList.style.border = '3px solid red';
            } else {
                onlyOneList.style.border = '3px solid black';
            }

            if (0 === getDay(year, mon, i)) {
                onlyOneList.style.color = 'red';
            } else if (6 == getDay(year, mon, i)) {
                onlyOneList.style.color = 'blue';
            }

            //현재 년, 월 같을 때

            Day.addEventListener('click', (event) => {
                if (event.target !== onlyOneList) {
                    onlyOneList.style.border = '3px solid black';
                }
            });

            Day.appendChild(onlyOneList);
            continue;
        }

        const list = document.createElement('li');
        list.textContent = `${i}`;
        if (i === DayOfChoice && year === yearOfChoice && mon === MonOfChoice) {
            list.style.border = '3px solid red';
            Day.addEventListener('click', (event) => {
                if (event.target !== list) {
                    list.style.border = 'none';
                }
            });
        }

        if (0 === getDay(year, mon, i)) {
            list.style.color = 'red';
        } else if (6 == getDay(year, mon, i)) {
            list.style.color = 'blue';
        }

        Day.appendChild(list);
    }
}

function setMonthTitle(year, mon) {
    month.textContent = `${year}. ${mon}`
}

function nextMonthOrYear() {
    if (mon === 12) {
        year = year + 1;
        mon = 1;
    } else {
        mon = mon + 1;
    }
    setMonthTitle(year, mon);
    makeCalendar(year, mon, getDayOfMon(mon, year));
}

function preMonthOrYear() {
    if (mon === 1) {
        year = year - 1;
        mon = 12;
    } else {
        mon = mon - 1;
    }
    setMonthTitle(year, mon);
    makeCalendar(year, mon, getDayOfMon(mon, year));
}


function main() {
    setMonthTitle(year, mon);
    makeCalendar(year, mon, getDayOfMon(mon, year));
    todoTitle.textContent = `날짜를 선택하세요`;
    // displayToDoOnDays();
}

function displayToDoOnDays() {
    todoList.innerHTML = '';
    const YMD = year + '-' + mon + '-' + DayOfChoice;
    let arrayToDo;
    const elementToDo = document.createElement('li');
    if (!localStorage.getItem(YMD)) {
        return;
    }
    if (localStorage.getItem(YMD).includes(',')) {

        arrayToDo = localStorage.getItem(YMD).split(',');
        arrayToDo.forEach((value) => {
            const deleteBtn = document.createElement('button');
            deleteBtn.setAttribute('class', 'deleteBtn');
            deleteBtn.innerHTML = '<i class="far fa-minus-square"></i>';
            const elementToDo = document.createElement('li');

            elementToDo.innerText = value;
            elementToDo.appendChild(deleteBtn);

            elementToDo.scrollTo();

            todoList.appendChild(elementToDo);
        });
    } else {
        const deleteBtn = document.createElement('button');
        deleteBtn.setAttribute('class', 'deleteBtn');
        deleteBtn.innerHTML = '<i class="far fa-minus-square"></i>';

        elementToDo.textContent = localStorage.getItem(YMD);
        elementToDo.appendChild(deleteBtn);
        todoList.appendChild(elementToDo);
    }
}

pre.addEventListener('click', preMonthOrYear);
next.addEventListener('click', nextMonthOrYear);


function clearEvent() {
    clickEventArr.forEach((value) => {
        value.style.border = 'none';
    });
}

Day.addEventListener('click', (event) => {
    if (event.target.tagName === 'UL') return;
    if (event.target.className !== 'disabled') {
        clearEvent();
        let day = event.target.textContent
        todoTitle.textContent = `${year}년 ${mon}월 ${event.target.textContent}일`;
        event.target.style.border = '3px solid red';
        DayOfChoice = (event.target.textContent) * 1;
        MonOfChoice = mon;
        yearOfChoice = year;
        let date = year + '-' + mon + '-' + day
        console.log(date)

        $.ajax({
            type: 'POST',
            url: '/reservation/show',
            data: {'date_give': date},
            success: function (response) {
                console.log(response['reservations'])
                $('#reservation-text').empty()
                let rows = response['reservations']
                for (let i = 0; i < rows.length; i++) {
                    let date = rows[i]['date']
                    let time = rows[i]['time']
                    let member = rows[i]['member']
                    let tutor = rows[i]['tutor']
                    let num = rows[i]['num']
                    let temp_html = ``

                    if (response['status'] == '미래') {
                        if (response['msg'] == '일반회원') {
                            temp_html = `<h3> 시간 : ${time} </h3>
                                <h3> 강사 : ${tutor} </h3>
                                <button class="btn btn-cancel" onclick="cancel(${num})"> 예약취소 </button><hr>
                               `;
                        } else {
                            temp_html = `<h3> 시간 : ${time} </h3>
                                <h3> 회원 : ${member} </h3>
                                <button class="btn btn-cancel" onclick="cancel(${num})"> 예약취소 </button><hr>
                               `;
                        }
                        $('#reservation-text').append(temp_html);

                    } else {
                        if (response['msg'] == '일반회원') {
                            temp_html = `<h3> 시간 : ${time} </h3>
                                <h3> 강사 : ${tutor} </h3> <hr>`;
                        } else {
                            temp_html = `<h3> 시간 : ${time} </h3>
                                <h3> 회원 : ${member} </h3><hr>  `;
                        }
                        $('#reservation-text').append(temp_html);
                    }


                }

            }
        });

        displayToDoOnDays();
        clickEventArr.push(event.target);
        console.log(clickEventArr);
        // input.focus();
    }

});


function addToDoList() {
    if (input.value === '') {
        alert('please input you are going to do');
        return;
    }

    const YMD = year + '-' + mon + '-' + DayOfChoice;
    localStorage.setItem(YMD, storeToDo);

    displayToDoOnDays();
    input.value = "";
    input.focus();
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

main();

