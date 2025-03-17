document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    
    if(response.ok) {
        localStorage.setItem('token', data.token);
        alert('Giriş başarılı!');
        // token ile giriş yapılacak sayfaya yönlendirme
        window.location.href = '/protected.html';
    } else {
        alert(data.message);
    }
});


document.getElementById('registerLink').addEventListener('click', async (e) => {
    e.preventDefault();
    const username = prompt("Kullanıcı adı girin:");
    const password = prompt("Şifre girin:");

    const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    alert(data.message);
});