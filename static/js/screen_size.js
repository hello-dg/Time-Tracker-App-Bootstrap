document.addEventListener("DOMContentLoaded", function() {
  function updateDate() {
    const dateContainer = document.getElementById('date-container');
    const dateString = "{{ entry.date }}";
    const date = new Date(dateString);

    const fullDateString = date.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' });
    const shortDateString = date.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' });

    if (window.innerWidth < 992) {
      dateContainer.textContent = shortDateString;
    } else {
      dateContainer.textContent = fullDateString;
    }
  }

  window.addEventListener('resize', updateDate);
  updateDate();
});