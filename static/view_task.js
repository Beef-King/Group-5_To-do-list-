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