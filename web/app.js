app.js



async function callHello() {
    const name = document.getElementById('nameInput').value || 'World';
    const resultEl = document.getElementById('result');
    
    try {
        const response = await fetch('/api/hello', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name })
        });
        
        const data = await response.json();
        resultEl.innerHTML = `✅ ${data.message}`;
        resultEl.style.color = '#28a745';
    } catch (error) {
        resultEl.innerHTML = '❌ Error communicating with Python';
        resultEl.style.color = 'red';
    }
}

async function addNumbers() {
    const num1 = parseInt(document.getElementById('num1').value) || 0;
    const num2 = parseInt(document.getElementById('num2').value) || 0;
    const resultEl = document.getElementById('mathResult');
    
    try {
        const response = await fetch('/api/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ a: num1, b: num2 })
        });
        
        const data = await response.json();
        resultEl.innerHTML = `Result: <strong>${data.result}</strong>`;
        resultEl.style.color = '#28a745';
    } catch (error) {
        resultEl.innerHTML = '❌ Error';
        resultEl.style.color = 'red';
    }
}

// Bonus: Expose a function that Python can call (if using webview.expose)
window.getGreeting = function() {
    return "Hello from JavaScript!";
}

async function callmarriage() {

    alert("Before fetch");

    const fname = document.getElementById('groomfname').value;
    const lname = document.getElementById('groomlname').value;
    const mobile = document.getElementById('groom_mobile').value;

    try {

        const response = await fetch('/api/save_registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                groom_fname: fname,
                groom_lname: lname,
                groom_mobile: mobile
            })
        });

        const data = await response.json();

        alert(data.message);

    } catch(error) {
        alert("Fetch failed");
        console.log(error);
    }
}
