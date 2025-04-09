document.addEventListener('DOMContentLoaded', () => {
    console.log('Login page loaded');
    
    const loginForm = document.getElementById('login-form');
    const errorMessageElement = document.createElement('div');
    errorMessageElement.className = 'error-message';
    errorMessageElement.style.color = 'red';
    errorMessageElement.style.marginTop = '10px';
    errorMessageElement.style.display = 'none';
    
    // Insert error message element after the form
    loginForm.appendChild(errorMessageElement);

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get email and password values
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                // Make AJAX request to API
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                // Handle API response
                if (response.ok) {
                    const data = await response.json();
                    
                    // Store JWT token in a cookie
                    document.cookie = `token=${data.access_token}; path=/`;
                    
                    // Redirect to index.html
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    errorMessageElement.textContent = errorData.message || 'Login failed. Please check your credentials.';
                    errorMessageElement.style.display = 'block';
                }
            } catch (error) {
                console.error('Error during login:', error);
                errorMessageElement.textContent = 'An error occurred during login. Please try again.';
                errorMessageElement.style.display = 'block';
            }
        });
    }
});
