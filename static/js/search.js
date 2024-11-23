// static/js/search.js

$(document).ready(function () {
    // Initialize the DataTable (even though we don't populate yet)
    let dataTable = $('#resultsTable').DataTable({
        columns: [
            { title: "Entity Name" },
            { title: "EIN" },
            { title: "Total Revenue" },
            { title: "Total Expenses" },
            { title: "Net Income" },
            { title: "Compensation (Top Employees)" }
        ]
    });
    console.log("DataTable initialized:", dataTable); // Debug: Verify initialization

    // Handle Search Form Submission (First Button)
    $('#search-form').on('submit', function (e) {
        e.preventDefault();
        let entityName = $('#entity_name').val().trim();

        if (entityName === "") {
            alert("Please enter a non-profit name.");
            return;
        }

        // Indicate loading state for Search button
        let searchButton = $(this).find('button[type="submit"]');
        searchButton.prop('disabled', true)
            .html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Searching...');

        $('#json-feedback').empty();
        $('#status-indicator').hide();
        $('#extract-info-btn').prop('disabled', true);

        // Make AJAX call to search endpoint
        $.ajax({
            url: '/search/', // Backend endpoint for searching
            type: 'POST',
            data: JSON.stringify({ 'entity_name': entityName }),
            contentType: 'application/json',
            success: function (response) {
                searchButton.prop('disabled', false).html('Search');
                console.log("Search response:", response); // Debug: Check backend response

                if (response.message === 'Search and parsing completed successfully.') {
                    $('#status-indicator').show(); // Show a success indicator
                    $('#json-feedback').html('<div class="alert alert-success">Search completed successfully.</div>');
                    $('#extract-info-btn').prop('disabled', false); // Enable the second button
                } else {
                    $('#json-feedback').html('<div class="alert alert-warning">' + response.message + '</div>');
                }
            },
            error: function (xhr, status, error) {
                searchButton.prop('disabled', false).html('Search');
                console.error("Search failed:", error); // Debug: Log the error
                let errorMessage = xhr.responseJSON && xhr.responseJSON.message ? xhr.responseJSON.message : error;
                $('#json-feedback').html(`<div class="alert alert-danger">Search failed: ${errorMessage}</div>`);
            }
        });
    });

    // Handle Extract Key Information Button Click (Second Button)
    $('#extract-info-btn').on('click', function () {
        console.log('Extract Key Information button clicked'); // Debug log
        let button = $(this);
        button.prop('disabled', true)
            .html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Extracting...');

        $('#json-feedback').html(`
            <div class="alert alert-info">
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Extracting key information...
            </div>
        `);

        // Make AJAX call to extraction endpoint
        $.ajax({
            url: '/gpt_handler/', // Backend endpoint for extracting data
            type: 'POST',
            contentType: 'application/json',
            success: function (response) {
                console.log('Extraction response:', response); // Debug log
                if (response.success) {
                    // Populate the DataTable with extracted data
                    dataTable.clear();
                    response.extracted_data.forEach(data => {
                        dataTable.row.add([
                            data.name || '',
                            data.ein || '',
                            (data.revenue || 0).toLocaleString(),
                            (data.expenses || 0).toLocaleString(),
                            (data.net_income || 0).toLocaleString(),
                            data.compensation || 'N/A'
                        ]);
                    });
                    dataTable.draw();

                    // Update success feedback
                    $('#json-feedback').html(`
                        <div class="alert alert-success">
                            Key information extracted successfully.
                            <a href="${response.download_url}" class="btn btn-sm btn-info ml-2">View Detailed Report</a>
                        </div>
                    `);
                    $('#status-indicator').show();
                } else {
                    $('#json-feedback').html(`<div class="alert alert-danger">${response.message}</div>`);
                }
                button.prop('disabled', false)
                    .html('Extract Key Information');
            },
            error: function (xhr, status, error) {
                console.error('Error during extraction:', error); // Debug log
                let errorMessage = xhr.responseJSON && xhr.responseJSON.message ? xhr.responseJSON.message : error;
                $('#json-feedback').html(`<div class="alert alert-danger">Extraction failed: ${errorMessage}</div>`);
                button.prop('disabled', false)
                    .html('Extract Key Information');
            }
        });
    });
});
