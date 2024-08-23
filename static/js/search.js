const searchInput = document.getElementById('search');
const clientList = document.querySelectorAll('.search li');

searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();

    clientList.forEach(item => {
        const clientName = item.textContent.toLowerCase();
        if (clientName.includes(query)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});