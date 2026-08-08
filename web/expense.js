async function saveExpense() {

    const response = await fetch("/api/save_expense", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            expense_category: document.getElementById("expense_category").value,

            expense_description: document.getElementById("expense_description").value,

            expense_amount: document.getElementById("expense_amount").value,

            payment_method: document.getElementById("payment_method").value,

            paid_to: document.getElementById("paid_to").value,

            approved_by: document.getElementById("approved_by").value,

            remarks: document.getElementById("remarks").value

        })

    });

    const result = await response.json();

    alert(result.message);

    loadExpense();

    clearExpenseForm();

}

async function loadExpense() {

    const response = await fetch("/api/view_expense");

    const expenses = await response.json();

    const table = document.getElementById("expenseTable");

    table.innerHTML = "";

    expenses.forEach(expense => {

        table.innerHTML += `

        <tr>

            <td>${expense[1]}</td>
            <td>${expense[3]}</td>
            <td>${expense[4]}</td>
            <td>${expense[5]}</td>
            <td>${expense[6]}</td>
            <td>${expense[7]}</td>
            <td>${expense[2]}</td>
            <td>${expense[8]}</td>

            <td>

                <button onclick="editExpense('${expense[1]}')">

                   Edit

                </button>

                <button onclick="deleteExpense(${expense[0]})">

                   Delete

                </button>

            </td>

        </tr>

        `;

    });

}

window.onload = function () {

    loadExpense();

}

async function searchExpense() {

    const searchValue =
    document.getElementById("searchExpense").value;

    const response = await fetch(
        `/api/search_expense/${searchValue}`
    );

    const expenses = await response.json();

    const table =
    document.getElementById("expenseTable");

    table.innerHTML = "";

    if (expenses.message) {

        alert(expenses.message);
        return;

    }

    expenses.forEach(expense => {

        table.innerHTML += `

        <tr>

            <td>${expense[1]}</td>
            <td>${expense[3]}</td>
            <td>${expense[4]}</td>
            <td>${expense[5]}</td>
            <td>${expense[6]}</td>
            <td>${expense[7]}</td>
            <td>${expense[2]}</td>
            <td>${expense[8]}</td>

            <td>

                <button onclick="editExpense('${expense[1]}')">
                   Edit

                </button>

                <button onclick="deleteExpense(${expense[0]})">

                  Delete

                </button>

            </td>

        </tr>

        `;

    });

}

let selectedExpenseId = null;

async function editExpense(expenseNumber) {

    const response = await fetch(
        `/api/search_expense/${expenseNumber}`
    );

    const expenses = await response.json();

    if (expenses.message) {
        alert(expenses.message);
        return;
    }

    const expense = expenses[0];

    selectedExpenseId = expense[0];

    document.getElementById("expense_category").value = expense[3];
    document.getElementById("expense_description").value = expense[4];
    document.getElementById("expense_amount").value = expense[5];
    document.getElementById("payment_method").value = expense[6];
    document.getElementById("paid_to").value = expense[7];
    document.getElementById("approved_by").value = expense[8];
    document.getElementById("remarks").value = expense[9];

    const button = document.getElementById("saveButton");

    button.innerText = "Update Expense";

    button.onclick = updateExpense;

}

async function updateExpense() {

    const response = await fetch("/api/update_expense", {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            id: selectedExpenseId,

            expense_category: document.getElementById("expense_category").value,

            expense_description: document.getElementById("expense_description").value,

            expense_amount: document.getElementById("expense_amount").value,

            payment_method: document.getElementById("payment_method").value,

            paid_to: document.getElementById("paid_to").value,

            approved_by: document.getElementById("approved_by").value,

            remarks: document.getElementById("remarks").value

        })

    });

    const result = await response.json();

    alert(result.message);

    loadExpense();

    clearExpenseForm();

}

function clearExpenseForm() {

    document.getElementById("expense_category").value = "Electricity";
    document.getElementById("expense_description").value = "";
    document.getElementById("expense_amount").value = "";
    document.getElementById("payment_method").value = "";
    document.getElementById("paid_to").value = "";
    document.getElementById("approved_by").value = "";
    document.getElementById("remarks").value = "";
    selectedExpenseId = null;

    const button = document.getElementById("saveButton");

    button.innerText = "Save Expense";

    button.onclick = saveExpense;

}

async function deleteExpense(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this expense?"
    );

    if (!confirmDelete) {
        return;
    }

    const response = await fetch("/api/delete_expense", {

        method: "DELETE",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            id: id

        })

    });

    const result = await response.json();

    alert(result.message);

    loadExpense();

}