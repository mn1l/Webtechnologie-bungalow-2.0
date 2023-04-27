// Get UI elements
const nativePicker = document.querySelector('.nativeWeekPicker');
const fallbackPicker = document.querySelector('.fallbackWeekPicker');
const fallbackLabel = document.querySelector('.fallbackLabel');

const yearSelect = document.querySelector('#year');
const weekSelect = document.querySelector('#fallbackWeek');

// Hide fallback initially
fallbackPicker.style.display = 'none';
fallbackLabel.style.display = 'none';

// Test whether a new date input falls back to a text input or not
const test = document.createElement('input');

try {
  test.type = 'week';
} catch (e) {
  console.log(e.description);
}

// If it does, run the code inside the if () {} block
if ( test.type === 'text') {
  // Hide the native picker and show the fallback
  nativePicker.style.display = 'none';
  fallbackPicker.style.display = 'block';
  fallbackLabel.style.display = 'block';

  // populate the weeks dynamically
  populateWeeks();
}

function populateWeeks() {
  // Populate the week select with 52 weeks
  for (let i = 1; i <= 52; i++) {
    const option = document.createElement('option');
    option.textContent = (i < 10) ? `0${i}` : i;
    weekSelect.appendChild(option);
  }
}
