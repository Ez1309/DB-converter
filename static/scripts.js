
// Function to show download modal
function showDownloadModal(db_name) {
    document.getElementById("modal-title").innerText = "File Successfully Converted!";
    document.getElementById("modal_paragraph").innerText = "Your file was successfully converted to a database file. Click the button below to download it.";
    let modalbutton = document.getElementById("modal_button");
    modalbutton.innerText = "Download";
    modalbutton.onclick = function () {
        window.location.href = "/download/" + db_name;
    }

    // Delay execution until DOM is fully loaded
    document.addEventListener('DOMContentLoaded', (event) => {
        // Check if jQuery is defined
        if (typeof $ !== 'undefined') {
            $("#reg-modal").modal("show");
        } else {
            console.log('Error: jQuery is not loaded.');
        }
    });
}

// Event listener for form submission
document.addEventListener('DOMContentLoaded', (event) => {
    // Check if db_name input exists and call showDownloadModal if so
    if (document.getElementById('db_name').value) {
        showDownloadModal(document.getElementById('db_name').value);
    }

    // Event listener for form submission
    document.getElementById("file_form").addEventListener("submit", function(event) {
        let db_name = document.getElementById("db_name").value;
        let fileinput = document.getElementById("file_input").value;
        let parts = fileinput.split(/[/\\]/);
        let filename = parts[parts.length - 1];
        
        if (!fileinput) {
            event.preventDefault();
            showErrorModal("Oops! It seems like you didn't upload a file.");
        } else if (!db_name) {
            event.preventDefault();
            showErrorModal("Oops! It seems like you didn't type the name of your database.");
        } else if (!filename.endsWith(".csv") && !filename.endsWith(".xlsx")) {
            event.preventDefault();
            showErrorModal("Oops! It seems like your file is not a CSV or XLSX file.");
        }
    });
    document.getElementById("table_view_form").addEventListener("submit", function(event) {
        let tableinput = document.getElementById("table_input").value;
        let parts = tableinput.split(/[/\\]/);
        let filename = parts[parts.length - 1];
        if (!tableinput) {
            event.preventDefault();
            showErrorModal("Oops! It seems like you didn't upload a file.");
        } else if (!filename.endsWith(".csv") && !filename.endsWith(".xlsx")) {
            event.preventDefault();
            showErrorModal("Oops! It seems like your file is not a CSV or XLSX file.");
        }
    })
});

// Function to show error modal
function showErrorModal(message) {
    document.getElementById("modal_paragraph").innerText = message;
    $("#reg-modal").modal("show");
}
