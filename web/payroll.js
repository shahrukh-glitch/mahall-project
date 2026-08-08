document.getElementById("year").value = new Date().getFullYear();

document.getElementById("generatePayroll").addEventListener("click", async () => {

    const data = {

        month: document.getElementById("month").value,
        year: document.getElementById("year").value

    };

    const response = await fetch("/api/generate_payroll", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    alert(result.message);

});

async function loadSalaryHistory() {

    const response = await fetch("/api/view_salary_history");

    const salaries = await response.json();

    const table = document.getElementById("salaryTable");

    table.innerHTML = "";

    salaries.forEach(salary => {

        table.innerHTML += `

        <tr>

            <td>${salary[2]}</td>
            <td>${salary[3]}</td>
            <td>${salary[4]}</td>
            <td>${salary[5]}</td>
            <td>${salary[9]}</td>
            <td>${salary[11]}</td>

            <td>

                 ${
                    salary[11] === "Paid"

                    ? `<button onclick="generatePayslip(${salary[0]})">

                            Payslip
                       </button>`

                    : `<button onclick="paySalary(${salary[0]})">

                        Pay

                      </button>`
                }

            </td>

        </tr>

        `;

    });

}

loadSalaryHistory();

async function paySalary(id){

    const response = await fetch("/api/pay_salary",{

        method:"PUT",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            id:id
        })

    });

    const result = await response.json();

    alert(result.message);

    loadSalaryHistory();

}

async function generatePayslip(id){

    const response = await fetch("/api/generate_payslip",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            id:id
        })

    });

    const result = await response.json();

    if(result.message){

        alert(result.message);

        return;

    }

    document.getElementById("payslipCard").style.display = "block";

    const table = document.getElementById("payslipTable");

    table.innerHTML = `

        <tr>
            <td><b>Employee ID</b></td>
            <td>${result[2]}</td>
        </tr>

        <tr>
            <td><b>Employee Name</b></td>
            <td>${result[3]}</td>
        </tr>

        <tr>
            <td><b>Month</b></td>
            <td>${result[4]}</td>
        </tr>

        <tr>
            <td><b>Year</b></td>
            <td>${result[5]}</td>
        </tr>

        <tr>
            <td><b>Basic Salary</b></td>
            <td>${result[6]}</td>
        </tr>

        <tr>
            <td><b>Allowance</b></td>
            <td>${result[7]}</td>
        </tr>

        <tr>
            <td><b>Deduction</b></td>
            <td>${result[8]}</td>
        </tr>

        <tr>
            <td><b>Net Salary</b></td>
            <td>${result[9]}</td>
        </tr>

        <tr>
            <td><b>Payment Date</b></td>
            <td>${result[10]}</td>
        </tr>

        <tr>
            <td><b>Status</b></td>
            <td>${result[11]}</td>
        </tr>

    `;

}

document.getElementById("searchPayslip").addEventListener("click", async () => {

    const data = {

        employee_id: document.getElementById("search_employee_id").value,

        month: document.getElementById("search_month").value,

        year: document.getElementById("search_year").value

    };

    const response = await fetch("/api/search_payslip", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    if (result.message) {

        alert(result.message);

        return;

    }

    document.getElementById("payslipCard").style.display = "block";

    document.getElementById("payslipTable").innerHTML = `

        <tr><td><b>Employee ID</b></td><td>${result[2]}</td></tr>
        <tr><td><b>Employee Name</b></td><td>${result[3]}</td></tr>
        <tr><td><b>Month</b></td><td>${result[4]}</td></tr>
        <tr><td><b>Year</b></td><td>${result[5]}</td></tr>
        <tr><td><b>Basic Salary</b></td><td>${result[6]}</td></tr>
        <tr><td><b>Allowance</b></td><td>${result[7]}</td></tr>
        <tr><td><b>Deduction</b></td><td>${result[8]}</td></tr>
        <tr><td><b>Net Salary</b></td><td>${result[9]}</td></tr>
        <tr><td><b>Payment Date</b></td><td>${result[10]}</td></tr>
        <tr><td><b>Status</b></td><td>${result[11]}</td></tr>

    `;

});