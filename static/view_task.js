console.log("view_task.js loaded");
// =====================
// Select Button
// =====================
const selectBtn = document.querySelector(".select-btn");
const deleteBtn = document.querySelector(".delete-btn");

if (selectBtn && deleteBtn) {
    selectBtn.addEventListener("click", () => {
        deleteBtn.style.display = "inline-block";
    });
}

// =====================
// Search
// =====================
const searchInput = document.getElementById("searchInput");

if (searchInput) {
    searchInput.addEventListener("input", function () {
        console.log(this.value.trim());
    });
}

// =====================
// Status Tabs
// =====================
const tabs = document.querySelectorAll(".status-tab");

if (tabs.length > 0) {
    tabs.forEach(tab => {
        tab.addEventListener("click", () => {

            tabs.forEach(btn => btn.classList.remove("active"));

            tab.classList.add("active");

        });
    });
}
async function deleteTask(id) {
    const confirmDelete = confirm("Are you sure you want to delete this task?");

    if (!confirmDelete) return;

    const response = await fetch(`/api/tasks/${id}`, {
        method: "DELETE"
    });

    console.log("Status:", response.status);

    if (response.ok) {
        alert("Deleted!");
        location.reload();
    } else {
        alert("Delete failed");
    }
}
async function editTask(id){

    const response = await fetch(`/api/tasks/${id}`);

    const task = await response.json();

    document.getElementById("editId").value = task.id;
    document.getElementById("editTitle").value = task.title;
    document.getElementById("editDescription").value = task.description;
    document.getElementById("editCategory").value = task.category;
    document.getElementById("editPriority").value = task.priority;
    document.getElementById("editDueDate").value = task.due_date;

    document.getElementById("editModal").style.display="flex";

}
function closeModal(){

    document.getElementById("editModal").style.display="none";

}
async function saveTask() {

    const id = document.getElementById("editId").value;

    const title = document.getElementById("editTitle").value;
    const description = document.getElementById("editDescription").value;
    const category = document.getElementById("editCategory").value;
    const priority = document.getElementById("editPriority").value;
    const due_date = document.getElementById("editDueDate").value;

    const response = await fetch(`/api/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title,
            description,
            category,
            priority,
            due_date
        })
    });

    if (response.ok) {
        alert("Task updated successfully!");
        closeModal();
        location.reload();
    } else {
        alert("Failed to update task.");
    }
}