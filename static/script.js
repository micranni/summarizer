
document.getElementById('transForm').addEventListener('submit', async function(e){
    e.preventDefault();

    try{
        const input = document.getElementById('input-field').value;
        console.log(input);
    
        const response = await fetch("http://127.0.0.1:8000/summarize", {
            method: "POST",
            headers: {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify({
                message: input
            })
        });
    
        const responseData = await response.json();
        console.log("response data:");
        console.log(responseData);
        document.getElementById('display').textContent = responseData.response;
    } catch(error){
        document.getElementById('display').textContent = error.message;
    }
});