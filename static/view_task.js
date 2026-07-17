const selectBtn = document.querySelector(".select-btn");
const deleteBtn = document.querySelector(".delete-btn");

selectBtn.addEventListener("click", () => {
    deleteBtn.style.display = "inline-block";
});