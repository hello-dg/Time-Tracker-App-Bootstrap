const categoryInput = document.getElementById('searchCategory');
const categoryList = document.querySelectorAll('.searchCategory li');

categoryInput.addEventListener('input', () => {
    const query = categoryInput.value.toLowerCase();

    categoryList.forEach(item => {
        const clientName = item.textContent.toLowerCase();
        if (clientName.includes(query)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});


const projectInput = document.getElementById('searchProject');
const projectList = document.querySelectorAll('.searchProject li');

projectInput.addEventListener('input', () => {
    const query = projectInput.value.toLowerCase();

    projectList.forEach(item => {
        const clientName = item.textContent.toLowerCase();
        if (clientName.includes(query)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});


const taskInput = document.getElementById('searchTask');
const taskList = document.querySelectorAll('.searchTask li');

taskInput.addEventListener('input', () => {
    const query = taskInput.value.toLowerCase();

    taskList.forEach(item => {
        const clientName = item.textContent.toLowerCase();
        if (clientName.includes(query)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});


