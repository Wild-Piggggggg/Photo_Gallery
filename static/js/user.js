document.querySelector('.edit-btn').addEventListener('click', function() {
    alert('Edit Profile button clicked');
});

document.querySelector('.logout-btn').addEventListener('click', function() {
    alert('Logout button clicked');
});

const avatar = document.getElementById('user-avatar');
const overlay = document.getElementById('overlay');
const overlayImg = document.getElementById('overlay-img');

avatar.addEventListener('click', function() {
    overlay.style.display = 'flex';
});

overlay.addEventListener('click', function() {
    overlay.style.display = 'none';
});
