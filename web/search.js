async function searchRegistration() {

    const name = document.getElementById("groom_fname").value;

    const response = await fetch(`/api/search/${name}`);

    const data = await response.json();

    console.log(data);

    document.getElementById("results").innerHTML = `
        <h3>Registration Found</h3>
        <p>First Name: ${data[1]}</p>
        <p>Last Name: ${data[2]}</p>
        <p>Mobile: ${data[3]}</p>
    `;
}