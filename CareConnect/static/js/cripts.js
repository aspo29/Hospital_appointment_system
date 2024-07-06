// find_doctor js
// function searchCards() {
//     var query = document.getElementById('search-query').value.trim().toLowerCase();
//     var cards = document.querySelectorAll('.col-md-4.mb-4');

//     cards.forEach(function (card) {
//         var title = card.querySelector('.card-title').innerText.trim().toLowerCase();
//         if (title.includes(query)) {
//             card.style.display = 'block';
//         } else {
//             card.style.display = 'none';
//         }
//     });
// }

//document.getElementById('search-button').addEventListener('click', searchCards);
// document.getElementById('search-query').addEventListener('keyup', searchCards);

//appointment
// var today = new Date().toISOString().split('T')[0];
// var oneWeekLater = new Date();
// oneWeekLater.setDate(oneWeekLater.getDate() + 7);
// var maxDate = oneWeekLater.toISOString().split('T')[0];

// document.getElementById("appointment_date").setAttribute("min", today);
// document.getElementById("appointment_date").setAttribute("max", maxDate);