// var select = document.getElementById('select')
// select.onchange = function(){

//     // задаем время, через которое наш cookie истечет
//     var date = new Date();
//     date.setDate(date.getDate() + 7);

//     // записываем cookie
//     document.cookie = 'select=' + select.value +'; path=/; expires=' + date.toUTCString();
// }

// // возвращает cookie с именем name, если есть, если нет, то undefined
// function getCookie(name) {
//     var matches = document.cookie.match(new RegExp(
//             "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
//     ));
//     return matches ? decodeURIComponent(matches[1]) : undefined;
// }
 
// var select = document.getElementById('select'),
// cookie = getCookie('select');
 
// if (cookie) {
//     select.value = cookie;
// }
document.getElementById('marks_select').onchange = function(){
    localStorage['Item'] = this.value;
};
if(localStorage['Item']){
    document.getElementById("marks_select").options[ localStorage['Item'] ].selected = true;
}