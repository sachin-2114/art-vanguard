script.js
const input = document.getElementById('input');
const generate = document.getElementById('generate');
const output = document.getElementById('output');

generate.addEventListener('click', () => {
  console.log('Generate button clicked!');
  output.textContent = input.value;
});
