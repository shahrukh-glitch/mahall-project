const familyId = sessionStorage.getItem("family_id");
const table = document.getElementById("memberTable");

document.getElementById("addMember").addEventListener("click", async () => {

    const data = {

        family_id: familyId,   // Temporary value

        member_name: document.getElementById("member_name").value,
        gender: document.getElementById("gender").value,
        age: document.getElementById("age").value,
        relationship: document.getElementById("relationship").value,
        occupation: document.getElementById("occupation").value,
        education: document.getElementById("education").value

    };

    const response = await fetch("/api/save_family_member", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    alert(result.message);

    table.innerHTML += `
        <tr>
            <td>${data.member_name}</td>
            <td>${data.gender}</td>
            <td>${data.age}</td>
            <td>${data.relationship}</td>
            <td>${data.occupation}</td>
        </tr>
    `;

});