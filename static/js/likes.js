
document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');

    function getCookie(name) {
        const cookies = document.cookie.split(';');

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
            }
        }

        return null;
    }

    likeButtons.forEach(function (button) {
        button.addEventListener('click', async function () {
            if (button.disabled) {
                return;
            }

            button.disabled = true;

            try {
                const response = await fetch(button.dataset.url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    alert(data.error || 'Something went wrong.');
                    return;
                }

                const icon = button.querySelector('.like-icon');
                const count = button
                    .closest('.community-post-footer')
                    .querySelector('.likes-count');

                if (data.liked) {
                    button.classList.add('liked');
                    icon.textContent = '♥';
                } else {
                    button.classList.remove('liked');
                    icon.textContent = '♡';
                }

                count.textContent = data.likes_count + ' likes';

            } catch (error) {
                alert('Could not connect to the server.');
                console.error(error);
            } finally {
                button.disabled = false;
            }
        });
    });
});
