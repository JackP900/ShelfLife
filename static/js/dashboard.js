document.querySelectorAll(".reprice-btn").forEach(button => {
    button.addEventListener("click", async () => {
        console.log("dashboard.js loaded");
        const id = button.dataset.id;
        const response = await fetch(`/reprice/${id}`, {method: "POST"});
        const result = await response.json();
        console.log(result);
        location.reload();

    })
})