
// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');
const allSidedivider = document.querySelectorAll('.sidebar__section-title')

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');

	if(sidebar.classList.contains('hide')) {
		allSidedivider.forEach(item => {
			item.textContent = '.'
		})
	} 
	else {
		allSidedivider.forEach(item => {
			item.textContent = item.dataset.text;
		})
	}
})


// Profile Dropdown

const profile = document.querySelector('nav .profile');
const imgProfile = profile.querySelector('img');
const dropdownProfile = profile.querySelector('.profile-link');

imgProfile.addEventListener('click', function(){
	dropdownProfile.classList.toggle('show');
})

// collapse Profile Dropdown on outside click
window.addEventListener('click', function (e) {
	if (e.target !== imgProfile && e.target !== dropdownProfile && dropdownProfile.classList.contains('show')) {
       dropdownProfile.classList.remove('show');
 }
})

// Auto Toggle sidebar

if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} 


/*==================== DARK LIGHT THEME ====================*/ 

const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'bxs-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'bxs-moon' : 'bxs-sun'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'bxs-moon' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})


// Footer time 
let today = new Date();
let year = today.getFullYear();
document.getElementById('currentYear').innerHTML = year;


// OFF form close confirmation 
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}
