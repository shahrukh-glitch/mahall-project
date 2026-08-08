// ===============================
// Save Member
// ===============================

let selectedRegistrationId = null;

async function saveMember() {

    const url = selectedRegistrationId
        ? "/api/update_member"
        : "/api/save_member";

    const method = selectedRegistrationId
        ? "PUT"
        : "POST";

    const response = await fetch(url, {

    method: method,

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            id: selectedRegistrationId,

            registration_number: document.getElementById("registration_number").value,
            mahallu: document.getElementById("mahallu").value,
            ward: document.getElementById("ward").value,
            house_number: document.getElementById("house_number").value,
            family_number: document.getElementById("family_number").value,
            registration_date: document.getElementById("registration_date").value,

            family_head: document.getElementById("family_head").value,
            father_name: document.getElementById("father_name").value,
            house_name: document.getElementById("house_name").value,
            phone: document.getElementById("phone").value,
            address: document.getElementById("address").value

        })

    });

    const result = await response.json();

    alert(result.message);

    if (result.family_id) {

        sessionStorage.setItem("family_id", result.family_id);

    }

    loadMembers();

    clearMemberForm();

}


// ===============================
// View Members
// ===============================

async function loadMembers() {

    const response = await fetch("/api/view_members");

    const members = await response.json();

    const table = document.getElementById("memberTable");

    table.innerHTML = "";

    members.forEach(member => {

        table.innerHTML += `

        <tr>

            <td>${member[1]}</td>
            <td>
                <a href="#"
                   onclick="viewFamily('${member[1]}'); return false;">

                   ${member[7]}
                </a>
            </td>
            <td>${member[2]}</td>
            <td>${member[10]}</td>
            <td>${member[5]}</td>

            <td>

                <button onclick="manageMembers(${member[0]}, '${member[1]}')">

                   👥 Manage Members

                </button>

            </td>

            <td>

                <button onclick="editMember(${member[0]})">

                    Edit

                </button>

                <button onclick="deleteMember(${member[0]})">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

}


// ===============================
// Search Member
// ===============================

async function searchMember() {

    const searchValue = document.getElementById("searchMember").value;

    const response = await fetch(`/api/search_member/${searchValue}`);

    const result = await response.json();

    const table = document.getElementById("memberTable");

    table.innerHTML = "";

    if (result.message) {

        alert(result.message);

        return;

    }

    const member = result.member;

    table.innerHTML += `

    <tr>

        <td>${member[1]}</td>
        <td>
            <a href="#"
               onclick="viewFamily('${member[1]}'); return false;">

                ${member[7]}
            </a>
        </td>
        <td>${member[2]}</td>
        <td>${member[10]}</td>
        <td>${member[5]}</td>
        <td>

            <button onclick="manageMembers(${member[0]})">

                👥 Manage Members

            </button>

        </td>

        <td>

            <button onclick="editMember(${member[0]})">

                Edit

            </button>

            <button onclick="deleteMember(${member[0]})">

                Delete

            </button>

        </td>

    </tr>

    `;

}


// ===============================
// Clear Form
// ===============================

function clearMemberForm() {

    document.getElementById("registration_number").value = "";
    document.getElementById("mahallu").value = "";
    document.getElementById("ward").value = "";
    document.getElementById("house_number").value = "";
    document.getElementById("family_number").value = "";
    document.getElementById("registration_date").value = "";

    document.getElementById("family_head").value = "";
    document.getElementById("father_name").value = "";
    document.getElementById("house_name").value = "";
    document.getElementById("phone").value = "";
    document.getElementById("address").value = "";

}


// ===============================
// Load on Page Open
// ===============================

window.onload = async function () {

    await loadMembers();

    const registrationNumber =
        sessionStorage.getItem("selected_registration");

    if (registrationNumber) {

        viewFamily(registrationNumber);

    }

}

async function viewFamily(registrationNumber){

    const response = await fetch(
        `/api/search_member/${registrationNumber}`
    );

    const result = await response.json();

    document.getElementById("familySection").style.display = "block";

    document.getElementById("familyTitle").innerText =
    "Family Members - " + result.member[7];

    const table = document.getElementById("familyTable");

    table.innerHTML = "";

    if(result.message){

        table.innerHTML = `
        <tr>
            <td colspan="6">No Family Members Found</td>
        </tr>
        `;

        return;

    }

    result.family_members.forEach(member => {

        table.innerHTML += `

        <tr>

            <td>${member[2]}</td>
            <td>${member[3]}</td>
            <td>${member[4]}</td>
            <td>${member[5]}</td>
            <td>${member[6]}</td>
            <td>${member[7]}</td>

        </tr>

        `;

    });

}

function manageMembers(familyId, registrationNumber) {

    sessionStorage.setItem("family_id", familyId);

    sessionStorage.setItem(
        "selected_registration",
        registrationNumber
    );

    window.location.href = "/family_members";

}

async function editMember(id) {

    const response = await fetch(
        `/api/search_member_by_id/${id}`
    );

    console.log(response.status);

    const member = await response.json();

    console.log(member);

    selectedRegistrationId = member[0];

    document.getElementById("registration_number").value = member[1];
    document.getElementById("mahallu").value = member[2];
    document.getElementById("ward").value = member[3];
    document.getElementById("house_number").value = member[4];
    document.getElementById("family_number").value = member[5];
    document.getElementById("registration_date").value = member[6];

    document.getElementById("family_head").value = member[7];
    document.getElementById("father_name").value = member[8];
    document.getElementById("house_name").value = member[9];
    document.getElementById("phone").value = member[10];
    document.getElementById("address").value = member[11];

    document.getElementById("saveButton").innerText = "Update Member";

}

async function deleteMember(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this family?"
    );

    if (!confirmDelete) {

        return;

    }

    const response = await fetch("/api/delete_member", {

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

    loadMembers();

    document.getElementById("familyTable").innerHTML = "";

    document.getElementById("familySection").style.display = "none";

}