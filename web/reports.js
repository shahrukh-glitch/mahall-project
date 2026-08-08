document.getElementById("loadSummary").addEventListener("click", loadSummary);

async function loadSummary() {

    const response = await fetch("/api/financial_summary", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            month: document.getElementById("summary_month").value,

            year: document.getElementById("summary_year").value

        })

    });

    const result = await response.json();

    document.getElementById("totalDonations").innerText =
        result.total_donations;

    document.getElementById("totalExpenses").innerText =
        result.total_expenses;

    document.getElementById("netCash").innerText =
        result.net_cash;

    document.getElementById("donationTransactions").innerText =
        result.total_donation_transactions;

    document.getElementById("expenseTransactions").innerText =
        result.total_expense_transactions;

}

document.getElementById("searchDonationReport").addEventListener("click", loadDonationReport);

async function loadDonationReport() {

    const response = await fetch("/api/donation_reports", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            month: document.getElementById("donation_month").value,

            year: document.getElementById("donation_year").value

        })

    });

    const result = await response.json();

    const table = document.getElementById("donationReportTable");

    table.innerHTML = "";

    result.donation_records.forEach(donation => {

        table.innerHTML += `

        <tr>

            <td>${donation[1]}</td>
            <td>${donation[2]}</td>
            <td>${donation[4]}</td>

        </tr>

        `;

    });

}

document.getElementById("searchExpenseReport").addEventListener("click", loadExpenseReport);

async function loadExpenseReport() {

    const response = await fetch("/api/expense_reports", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            month: document.getElementById("expense_month").value,

            year: document.getElementById("expense_year").value

        })

    });

    const result = await response.json();

    const table = document.getElementById("expenseReportTable");

    table.innerHTML = "";

    result.expense_records.forEach(expense => {

        table.innerHTML += `

        <tr>

            <td>${expense[1]}</td>
            <td>${expense[2]}</td>
            <td>${expense[4]}</td>

        </tr>

        `;

    });

}