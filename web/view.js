async function loadRegistrations() {

    const response = await fetch('/api/view');
    const data = await response.json();

    let html = `
        <table border="1">
            <tr>
                <th>ID</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Mobile</th>
            </tr>
    `;

    for (let row of data) {

        html += `
            <tr>
                <td>${row[0]}</td>
                <td>${row[1]}</td>
                <td>${row[2]}</td>
                <td>${row[3]}</td>
            </tr>
        `;
    }

    html += `</table>`;

    document.getElementById("results").innerHTML = html;
}