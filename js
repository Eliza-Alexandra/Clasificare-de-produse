$(document).ready(function() {
    $("#uploadForm").on("submit", function(event) {
        event.preventDefault();
        
        var fileInput = $("#fileInput")[0].files[0];
        if (!fileInput) {
            $("#result").text("Please select a file.");
            return;
        }
        else {
            $('#result').removeClass('changed');  
            setTimeout(function() {
                $('#result').addClass('changed'); 
            }, 500);
        }

        var formData = new FormData();
        formData.append("file", fileInput);

        $.ajax({
            url: "/predict",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.predicted_class) {
                    $("#result").text("Category: " + response.predicted_class);
                } else {
                    $("#result").text("Error: " + response.error);
                }
            },
            error: function() {
                $("#result").text("File upload failed.");
            }
        });
    });
});
