async function loadDashboard() {

    const response = await fetch("/api/dashboard");

    const data = await response.json();

    document.getElementById("members-count").innerText =
        data.total_family_members;

    document.getElementById("families-count").innerText =
        data.total_families;

    document.getElementById("donation-total").innerText =
        "₹" + data.month_donation;

    document.getElementById("expense-total").innerText =
        "₹" + data.month_expenses;

    document.getElementById("net-cash").innerText =
        "₹" + data.net_cash;

    document.getElementById("usthad-count").innerText =
        data.total_usthads;

}

loadDashboard();