var marksSelect = document.getElementById('marks_select');

marksSelect.onchange = function () {
    // задаем время, через которое наша оценка в local storage истечет (например, через 7 дней)
    var date = new Date();
    date.setDate(date.getDate() + 7);

    // записываем оценку в local storage
    localStorage.setItem('userRating', marksSelect.value);
}

// возвращает оценку из local storage, если есть, если нет, то undefined
var userRating = localStorage.getItem('userRating');

if (userRating) {
    marksSelect.value = userRating;
}
