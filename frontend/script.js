const API = "http://127.0.0.1:8000";


function showSection(section) {
    document.getElementById("customer").classList.add("hidden");
    document.getElementById("admin").classList.add("hidden");

    document.getElementById(section).classList.remove("hidden");

    if (section === "admin") {
        loadRefunds();
    }
}


document.getElementById("refundForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const resultDiv = document.getElementById("result");

    const data = {
        customer_id: Number(document.getElementById("customer_id").value),
        order_number: document.getElementById("order_number").value.trim(),
        reason: document.getElementById("reason").value.trim()
    };

    resultDiv.innerHTML = "<p>ResolveAI is investigating your request...</p>";

    try {
        const response = await fetch(`${API}/refunds`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const responseData = await response.json();

        if (!response.ok) {
            throw new Error(responseData.detail || "Request failed");
        }

        resultDiv.innerHTML = `
            <div class="result-box">
                <h3>Investigation Completed</h3>
                <p><strong>Refund ID:</strong> ${responseData.refund_id}</p>
                <p><strong>Status:</strong> ${responseData.status}</p>
                <p><strong>Risk:</strong> ${responseData.risk_level}</p>
                <p><strong>Decision:</strong> ${responseData.decision}</p>
            </div>
        `;

        document.getElementById("refundForm").reset();

        await loadRefunds();

    } catch (error) {
        resultDiv.innerHTML = `
            <div class="error">${error.message}</div>
        `;
    }
});


async function loadRefunds() {
    try {
        const response = await fetch(`${API}/refunds`);

        if (!response.ok) {
            throw new Error("Unable to load refund requests");
        }

        const refunds = await response.json();

        const table = document.getElementById("refundTable");
        const history = document.getElementById("customerHistory");

        if (table) {
            table.innerHTML = "";

            refunds.forEach(refund => {
                const row = document.createElement("tr");

                const values = [
                    refund.id,
                    refund.customer_id,
                    refund.order_number,
                    refund.risk_level,
                    refund.status,
                    refund.decision
                ];

                values.forEach((value, index) => {
                    const cell = document.createElement("td");

                    if (index === 3 || index === 4) {
                        const badge = document.createElement("span");
                        badge.className = "badge " + String(value).toLowerCase();
                        badge.textContent = value;
                        cell.appendChild(badge);
                    } else {
                        cell.textContent = value ?? "";
                    }

                    row.appendChild(cell);
                });

                const actionCell = document.createElement("td");

                if (refund.status === "pending_review") {
                    actionCell.innerHTML = `
                        <button class="action-btn approve-btn"
                            onclick="reviewRefund(${refund.id}, 'approved')">
                            Approve
                        </button>

                        <button class="action-btn reject-btn"
                            onclick="reviewRefund(${refund.id}, 'rejected')">
                            Reject
                        </button>
                    `;
                } else {
                    actionCell.textContent = "Completed";
                }

                row.appendChild(actionCell);
                table.appendChild(row);
            });
        }

        if (history) {
            history.innerHTML = "";

            if (refunds.length === 0) {
                history.textContent = "No refund requests found.";
            } else {
                refunds.forEach(refund => {
                    const item = document.createElement("div");
                    item.className = "log-item";

                    item.textContent =
                        `Refund #${refund.id} | Order: ${refund.order_number} | Status: ${refund.status}`;

                    history.appendChild(item);
                });
            }
        }

        document.getElementById("totalRequests").textContent = refunds.length;

        document.getElementById("approvedRequests").textContent =
            refunds.filter(r => r.status === "approved").length;

        document.getElementById("pendingRequests").textContent =
            refunds.filter(r => r.status === "pending_review").length;

        document.getElementById("rejectedRequests").textContent =
            refunds.filter(r => r.status === "rejected").length;

    } catch (error) {
        console.error(error);
    }
}


async function reviewRefund(id, decision) {
    try {
        const response = await fetch(
            `${API}/refunds/${id}/review?decision=${decision}`,
            {
                method: "POST"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Review failed");
        }

        alert(data.message);

        await loadRefunds();

    } catch (error) {
        alert(error.message);
    }
}