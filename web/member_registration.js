document.querySelector("form").addEventListener("submit", async function (e) {

    e.preventDefault();

    const data = {

        registration_number: document.querySelector('[name="registration_number"]').value,
        mahallu: document.querySelector('[name="mahallu"]').value,
        ward: document.querySelector('[name="ward"]').value,
        house_number: document.querySelector('[name="house_number"]').value,
        family_number: document.querySelector('[name="family_number"]').value,
        registration_date: document.querySelector('[name="registration_date"]').value,

        family_head: document.querySelector('[name="family_head"]').value,
        father_name: document.querySelector('[name="father_name"]').value,
        house_name: document.querySelector('[name="house_name"]').value,
        phone: document.querySelector('[name="phone"]').value,
        address: document.querySelector('[name="address"]').value

    };

    const response = await fetch("/api/save_member", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(data)

    });

   const result = await response.json();

   
   sessionStorage.setItem("family_id", result.family_id);

   alert(result.message);

   window.location.href = "/family_members";
   
});