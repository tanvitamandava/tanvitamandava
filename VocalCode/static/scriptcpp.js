document.getElementById('runButton').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('codeForm').dispatchEvent(new Event('submit'));
});

document.getElementById('codeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const code = document.getElementById('code').value;
    const inputs = document.getElementById('inputs').value;

    fetch('/run_cpp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code, inputs: inputs })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').textContent = data.output;
    })
    .catch(error => {
        document.getElementById('output').textContent = 'Error: ' + error.message;
    });
});

document.getElementById('nightModeButton').addEventListener('click', function() {
    document.body.classList.toggle('night-mode');
});
