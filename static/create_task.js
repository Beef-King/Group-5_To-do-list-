let tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
  let filter = 'all';
  let categoryFilter = 'all';
  let priorityFilter = 'all';

  function save(){
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }

  function addTask(){
    const input = document.getElementById('taskInput');
    const category = document.getElementById('categoryInput');
    const priority = document.getElementById('priorityInput');
    const text = input.value.trim();
    if(!text) return;
    tasks.push({ id: Date.now(), text, category: category.value, priority: priority.value, done: false });
    input.value = '';
    save();
    render();
  }

  function toggleTask(id){
    const t = tasks.find(t => t.id === id);
    if(t) t.done = !t.done;
    save();
    render();
  }

  function deleteTask(id){
    tasks = tasks.filter(t => t.id !== id);
    save();
    render();
  }

  function setFilter(f){
    filter = f;
    document.querySelectorAll('.filters button[data-filter]').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-filter="${f}"]`).classList.add('active');
    render();
  }

  function filterByCategory(c){
    categoryFilter = c;
    render();
  }

  function filterByPriority(p){
    priorityFilter = p;
    render();
  }

  function render(){
    const list = document.getElementById('taskList');
    let visible = tasks;
    if(filter === 'active') visible = visible.filter(t => !t.done);
    if(filter === 'done') visible = visible.filter(t => t.done);
    
    if(categoryFilter !== 'all') visible = visible.filter(t => (t.category || 'Other') === categoryFilter);
    
    if(priorityFilter !== 'all') visible = visible.filter(t => (t.priority || 'Medium') === priorityFilter);

    if(visible.length === 0){
      list.innerHTML = '<p class="empty">No tasks here.</p>';
    } else {
      list.innerHTML = visible.map(t => `
        <div class="task ${t.done ? 'done' : ''}">
       
       
            <div class="check" onclick="toggleTask(${t.id})"></div>
          <span class="label">${t.text}</span>
          <span class="category">${t.category || 'Other'}</span>
          <span class="priority">${t.priority || 'Medium'}</span>
          <button class="delete" onclick="deleteTask(${t.id})">✕</button>
        </div>
      `).join('');
    }

    const remaining = tasks.filter(t => !t.done).length;
    document.getElementById('counter').textContent =
      tasks.length === 0 ? '' : `${remaining} task${remaining !== 1 ? 's' : ''} left`;
  }

  document.getElementById('taskInput').addEventListener('keypress', e => {
    if(e.key === 'Enter') addTask();
  });

  render();
  // close dropdown if clicking outside
  document.addEventListener('click', function(e){
    const menu = document.getElementById('navDropdown');
    const btn = document.querySelector('.menu-btn');
    if(!menu.contains(e.target) && !btn.contains(e.target)){
      menu.classList.remove('show');
    }
  });