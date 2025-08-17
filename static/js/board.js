// board.js — handles drag/drop + delete for Job Board

document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll("[data-draggable='card']");
    const columns = document.querySelectorAll("[data-dropzone='col']");

    let draggedCard = null;

    // --- Drag start ---
    cards.forEach(card => {
        card.addEventListener("dragstart", e => {
            draggedCard = card;
            e.dataTransfer.effectAllowed = "move";
            setTimeout(() => card.classList.add("dragging"), 0);
        });

        card.addEventListener("dragend", () => {
            draggedCard.classList.remove("dragging");
            draggedCard = null;
        });
    });

    // --- Drag over / drop handling ---
    columns.forEach(col => {
        col.addEventListener("dragover", e => {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
        });

        col.addEventListener("drop", async e => {
            e.preventDefault();
            if (!draggedCard) return;

            const newStatus = col.dataset.status;
            const cardsContainer = col.querySelector(".cards");

            // Move in DOM
            cardsContainer.appendChild(draggedCard);

            // Update on server
            const jobId = draggedCard.dataset.id;
            try {
                const res = await fetch(`/update_status/${jobId}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ status: newStatus })
                });
                if (!res.ok) {
                    console.error("Failed to update job status");
                }
            } catch (err) {
                console.error("Error updating status:", err);
            }
        });
    });

    // --- Delete button ---
    document.addEventListener("click", async e => {
        if (e.target.matches("[data-action='delete']")) {
            const jobId = e.target.dataset.id;
            if (!confirm("Delete this job?")) return;

            try {
               const res = await fetch(`/api/jobs/${jobId}/delete`, { method: "POST" });

                if (res.ok) {
                    e.target.closest(".card").remove();
                } else {
                    console.error("Failed to delete job");
                }
            } catch (err) {
                console.error("Error deleting job:", err);
            }
        }
    });
});
