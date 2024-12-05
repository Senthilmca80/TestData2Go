document.getElementById('load-data').addEventListener('click', function() {
    // Simulate loading test data
    const dataContainer = document.getElementById('data-container');
    dataContainer.innerHTML = '<p>Loading test data...</p>';
    setTimeout(() => {
        dataContainer.innerHTML = '<p>Test data loaded successfully!</p>';
    }, 2000);
});
