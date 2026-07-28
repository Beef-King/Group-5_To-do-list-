 function switchTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById(tab).classList.add('active');

            const title = document.querySelector('.logo h1');
            const subtitle = document.querySelector('.logo p');

            if (tab === 'login') {
                title.textContent = 'Welcome Back';
                subtitle.textContent = 'Sign in to access your account';
            } else {
                title.textContent = 'Get Started';
                subtitle.textContent = 'Create your free account today';
            }
        }

        function handleLogin(e) {
            e.preventDefault();
            alert('Login submitted! (This is a demo)');
        }

        function handleSignup(e) {
            e.preventDefault();
            const inputs = e.target.querySelectorAll('input[type="password"]');
            if (inputs[0].value !== inputs[1].value) {
                alert('Passwords do not match!');
                return;
            }
            alert('Account created successfully! (Thanks for working with us)');
        }