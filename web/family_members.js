const familyId = sessionStorage.getItem("family_id");
let selectedMemberId = null;
console.log("Selected Family ID:", familyId);
const table = document.getElementById("memberTable");

async function loadFamilyMembers() {

    const response = await fetch("/api/view_family_members");

    const members = await response.json();

    table.innerHTML = "";

    members.forEach(member => {

        if (member[1] == familyId) {

            table.innerHTML += `

            <tr>

                <td>${member[2]}</td>
                <td>${member[3]}</td>
                <td>${member[4]}</td>
                <td>${member[5]}</td>
                <td>${member[6]}</td>
                <td>${member[7]}</td>
                <td>

                   <button onclick="editFamilyMember(${member[0]})">

                      Edit

                   </button>

                   <button onclick="deleteFamilyMember(${member[0]})">

                      Delete

                   </button>

                </td>

            </tr>

            `;

        }

    });

}

document.getElementById("addMember").addEventListener("click", async () => {

    const data = {

        id: selectedMemberId,
        
        family_id: familyId,   // Temporary value

        member_name: document.getElementById("member_name").value,
        gender: document.getElementById("gender").value,
        age: document.getElementById("age").value,
        relationship: document.getElementById("relationship").value,
        occupation: document.getElementById("occupation").value,
        education: document.getElementById("education").value

    };

    const url = selectedMemberId
        ? "/api/update_family_member"
        : "/api/save_family_member";

    const method = selectedMemberId
        ? "PUT"
        : "POST";

    const response = await fetch(url, {

          method: method,

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });

    const result = await response.json();

    alert(result.message);

    selectedMemberId = null;

    document.getElementById("memberForm").reset();

    document.getElementById("addMember").innerText = "Add Member";

    loadFamilyMembers();

});

loadFamilyMembers();

document.getElementById("memberForm").reset();

async function deleteFamilyMember(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this family member?"
    );

    if (!confirmDelete) {
        return;
    }

    const response = await fetch("/api/delete_family_member", {

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

    loadFamilyMembers();

}

async function editFamilyMember(id) {

    const response = await fetch(
        `/api/search_family_member/${id}`
    );

    const member = await response.json();

    if (member.message) {

        alert(member.message);

        return;

    }

    selectedMemberId = member[0];

    document.getElementById("member_name").value = member[2];
    document.getElementById("gender").value = member[3];
    document.getElementById("age").value = member[4];
    document.getElementById("relationship").value = member[5];
    document.getElementById("occupation").value = member[6];
    document.getElementById("education").value = member[7];

    document.getElementById("addMember").innerText = "Update Member";

}

function goBackToMembers() {

    window.location.href = "/member_registration";

}