// REMOVE MESSAGES
const alertMsg = document.querySelector('.alert');
const closeMsg = document.querySelector('.alert-close');

closeMsg.addEventListener('click', function () {
	alertMsg.classList.toggle('hide');

})

