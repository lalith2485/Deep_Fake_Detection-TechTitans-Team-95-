function uploadVideo() {
    const videoInput = document.getElementById('videoUpload');
    const formData = new FormData();
    formData.append('video', videoInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            document.getElementById('results').innerHTML = `<p>${data.result}</p>`;
        } else if (data.error) {
            document.getElementById('results').innerHTML = `<p>Error: ${data.error}</p>`;
        }
    })
    .catch(error => {
        document.getElementById('results').innerHTML = `<p>Error: ${error}</p>`;
    });
}

function refreshPage() {
    window.location.reload();
}
