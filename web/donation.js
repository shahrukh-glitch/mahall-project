async function saveDonation() {

    const response = await fetch("/api/save_donation", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            donor_name: document.getElementById("donor_name").value,

            donor_phone: document.getElementById("donor_phone").value,

            donation_type: document.getElementById("donation_type").value,

            donation_amount: document.getElementById("donation_amount").value,

            payment_method: document.getElementById("payment_method").value,

            remarks: document.getElementById("remarks").value,

            received_by: document.getElementById("received_by").value

        })

    });

    const result = await response.json();

    alert(result.message);

    loadDonations();

    clearDonationForm();

}

async function loadDonations() {

    const response = await fetch("/api/view_donations");

    const donations = await response.json();

    const table = document.getElementById("donationTable");

    table.innerHTML = "";

    donations.forEach(donation => {

        table.innerHTML += `

        <tr>

            <td>${donation[1]}</td>
            <td>${donation[2]}</td>
            <td>${donation[3]}</td>
            <td>${donation[5]}</td>
            <td>${donation[6]}</td>
            <td>${donation[7]}</td>
            <td>${donation[4]}</td>
            <td>${donation[9]}</td>

            <td>

                <button onclick="editDonation('${donation[1]}')">

                   Edit

                </button>

                <button onclick="deleteDonation(${donation[0]})">

                   Delete

                </button>

            </td>

        </tr>

        `;

    });

}

window.onload = function () {

    loadDonations();

}

async function searchDonation() {

    const searchValue =
    document.getElementById("searchDonation").value;

    const response = await fetch(
        `/api/search_donation/${searchValue}`
    );

    const donations = await response.json();

    const table =
    document.getElementById("donationTable");

    table.innerHTML = "";

    if (donations.message) {

        alert(donations.message);
        return;

    }

    donations.forEach(donation => {

        table.innerHTML += `

        <tr>

            <td>${donation[1]}</td>
            <td>${donation[2]}</td>
            <td>${donation[3]}</td>
            <td>${donation[5]}</td>
            <td>${donation[6]}</td>
            <td>${donation[7]}</td>
            <td>${donation[4]}</td>
            <td>${donation[9]}</td>

            <td>

                <button onclick="editDonation('${donation[1]}')">
                   Edit

                </button>

                <button onclick="deleteDonation(${donation[0]})">

                  Delete

                </button>

            </td>

        </tr>

        `;

    });

}

let selectedDonationId = null;

async function editDonation(donationNumber) {

    const response = await fetch(
        `/api/search_donation/${donationNumber}`
    );

    const donations = await response.json();

    if (donations.message) {
        alert(donations.message);
        return;
    }

    const donation = donations[0];

    selectedDonationId = donation[0];

    document.getElementById("donor_name").value = donation[2];
    document.getElementById("donor_phone").value = donation[3];
    document.getElementById("donation_type").value = donation[5];
    document.getElementById("donation_amount").value = donation[6];
    document.getElementById("payment_method").value = donation[7];
    document.getElementById("remarks").value = donation[8];
    document.getElementById("received_by").value = donation[9];

    const button = document.getElementById("saveButton");

    button.innerText = "Update Donation";

    button.onclick = updateDonation;

}

async function updateDonation() {

    const response = await fetch("/api/update_donation", {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            id: selectedDonationId,

            donor_name: document.getElementById("donor_name").value,

            donor_phone: document.getElementById("donor_phone").value,

            donation_type: document.getElementById("donation_type").value,

            donation_amount: document.getElementById("donation_amount").value,

            payment_method: document.getElementById("payment_method").value,

            remarks: document.getElementById("remarks").value,

            received_by: document.getElementById("received_by").value

        })

    });

    const result = await response.json();

    alert(result.message);

    loadDonations();

    clearDonationForm();

}

function clearDonationForm() {

    document.getElementById("donor_name").value = "";
    document.getElementById("donor_phone").value = "";
    document.getElementById("donation_type").value = "General Donation";
    document.getElementById("donation_amount").value = "";
    document.getElementById("payment_method").value = "";
    document.getElementById("remarks").value = "";
    document.getElementById("received_by").value = "";

    selectedDonationId = null;

    const button = document.getElementById("saveButton");

    button.innerText = "Save Donation";

    button.onclick = saveDonation;

}

async function deleteDonation(id) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this donation?"
    );

    if (!confirmDelete) {
        return;
    }

    const response = await fetch("/api/delete_donation", {

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

    loadDonations();

}