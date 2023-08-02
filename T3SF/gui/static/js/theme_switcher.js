// Check the initial theme preference and set it
const themePreference = localStorage.getItem('theme');
const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

if (themePreference === 'dark' || (themePreference === null && prefersDarkMode)) {
	enableDarkMode();
} else {
	enableLightMode();
}

// Toggle the theme when the button is clicked
const themeToggle = document.getElementById('theme-toggle');

themeToggle.addEventListener('click', () => {
	if (document.documentElement.getAttribute('data-bs-theme') === 'dark') {
		enableLightMode();
	} else {
		enableDarkMode();
	}
});

// Enable dark mode
function enableDarkMode() {
	document.documentElement.setAttribute('data-bs-theme', 'dark');
	localStorage.setItem('theme', 'dark');
	replaceClassNames('bg-light', 'bg-darkmode');
	replaceClassNames('bg-white', 'bg-dark');
	document.getElementById('theme-icon').classList.replace('bi-moon-fill', 'bi-sun-fill');
	document.getElementById('theme-text').textContent = 'Light mode';
	document.querySelectorAll('#logo-image').forEach((image) => {image.src = "/static/imgs/logo-dark.png";});
	document.getElementById('json-editor-container')?.classList.replace('jse-theme-light', 'jse-theme-dark');
}

// Enable light mode
function enableLightMode() {
	document.documentElement.setAttribute('data-bs-theme', 'light');
	localStorage.setItem('theme', 'light');
	replaceClassNames('bg-darkmode', 'bg-light');
	replaceClassNames('bg-dark', 'bg-white');
	document.getElementById('theme-icon').classList.replace('bi-sun-fill', 'bi-moon-fill');
	document.getElementById('theme-text').textContent = 'Dark mode';
	document.querySelectorAll('#logo-image').forEach((image) => {image.src = "/static/imgs/logo-light.png"; });
	document.getElementById('json-editor-container')?.classList.replace('jse-theme-dark', 'jse-theme-light');
}

// Replace class names
function replaceClassNames(oldClassName, newClassName) {
	const elements = document.querySelectorAll(`.${oldClassName}`);
	elements.forEach((element) => {
		element.classList.remove(oldClassName);
		element.classList.add(newClassName);
	});
}