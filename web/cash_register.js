async function loadCashRegister(){

    const response = await fetch("/api/view_cash_register");

    const transactions = await response.json();

    const table = document.getElementById("cashTable");

    table.innerHTML = "";

    transactions.forEach(transaction => {

        table.innerHTML += `

        <tr>

            <td>${transaction[1]}</td>

            <td>${transaction[2]}</td>

            <td>${transaction[3]}</td>

            <td>${transaction[4]}</td>

            <td>${transaction[5]}</td>

            <td>${transaction[6]}</td>

            <td><b>${transaction[7]}</b></td>

        </tr>

        `;

    });

}

loadCashRegister();