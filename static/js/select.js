document.querySelectorAll('.category-item').forEach(function(item) {
    item.addEventListener('click', function() {
        document.getElementById('category-input').value = this.getAttribute('data-value');
    });
});

document.querySelectorAll('.project-item').forEach(function(item) {
    item.addEventListener('click', function() {
        document.getElementById('project-input').value = this.getAttribute('data-value');
    });
});

document.querySelectorAll('.task-item').forEach(function(item) {
    item.addEventListener('click', function() {
        document.getElementById('task-input').value = this.getAttribute('data-value');
    });
});

document.querySelectorAll('.tag-item').forEach(function(item) {
    item.addEventListener('click', function() {
        document.getElementById('tag-input').value = this.getAttribute('data-value');
    });
});