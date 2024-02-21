// // var marksSelect = document.getElementById('marks_select');

// // marksSelect.onchange = function () {
// //     // задаем время, через которое наша оценка в local storage истечет (например, через 7 дней)
// //     var date = new Date();
// //     date.setDate(date.getDate() + 7);

// //     // записываем оценку в local storage
// //     localStorage.setItem('userRating', marksSelect.value);
// // }

// // // возвращает оценку из local storage, если есть, если нет, то undefined
// // var userRating = localStorage.getItem('userRating');

// // if (userRating) {
// //     marksSelect.value = userRating;
// // }

// var select = document.getElementById('marks_select');var select = document.getElementById('marks_select');
// var addButton = document.querySelector('button'); // Assuming this is the button in question

// // Function to set a cookie with the selected value
// function setCookie(name, value, days) {
//     var date = new Date();
//     date.setDate(date.getDate() + days);
//     document.cookie = name + '=' + value + '; path=/; expires=' + date.toUTCString();
// }

// // Function to get the value of a cookie by name
// function getCookie(name) {
//     var matches = document.cookie.match(new RegExp(
//         "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
//     ));
//     return matches ? decodeURIComponent(matches[1]) : undefined;
// }

// // Set the initial value of the select box based on the cookie
// var cookie = getCookie('marks_select');
// if (cookie) {
//     select.value = cookie;
// }

// // Event listener for the select box change
// select.addEventListener('change', function() {
//     // Store the selected rating in a cookie
//     setCookie('marks_select', select.value, 7);
// });

// // Set the 'selected' attribute dynamically based on the cookie
// document.addEventListener('DOMContentLoaded', function() {
//     var options = select.options;
//     for (var i = 0; i < options.length; i++) {
//         if (options[i].value === cookie) {
//             options[i].setAttribute('selected', 'selected');
//         } else {
//             options[i].removeAttribute('selected');
//         }
//     }
// });

// // Event listener for the button click
// addButton.addEventListener('click', function() {
//     alert('Оценка сохранена!'); // You can customize this message
// });
