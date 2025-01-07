<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Train Tracking System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Train Tracking System</h1>
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        Active Trains
                    </div>
                    <div class="card-body">
                        <div id="trainList"></div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        Train Details
                    </div>
                    <div class="card-body">
                        <div id="trainDetails"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Fetch all trains
        fetch('api/index.php?action=all')
            .then(response => response.json())
            .then(data => {
                const trainList = document.getElementById('trainList');
                data.forEach(train => {
                    const div = document.createElement('div');
                    div.className = 'mb-3';
                    div.innerHTML = `
                        <h5>${train.train_name} (${train.train_number})</h5>
                        <p>Status: ${train.status}<br>
                        Current Station: ${train.current_station || 'N/A'}<br>
                        Delay: ${train.delay_minutes || 0} minutes</p>
                        <button class="btn btn-primary btn-sm" onclick="showDetails(${train.train_id})">
                            Show Details
                        </button>
                    `;
                    trainList.appendChild(div);
                });
            });

        // Show train details
        function showDetails(trainId) {
            fetch(`api/index.php?action=location&train_id=${trainId}`)
                .then(response => response.json())
                .then(train => {
                    const details = document.getElementById('trainDetails');
                    details.innerHTML = `
                        <h4>${train.train_name}</h4>
                        <p>
                            Current Location:<br>
                            Latitude: ${train.latitude || 'N/A'}<br>
                            Longitude: ${train.longitude || 'N/A'}<br>
                            Current Station: ${train.current_station || 'N/A'}<br>
                            Status: ${train.status}<br>
                            Departure: ${train.departure_time}<br>
                            Arrival: ${train.arrival_time}<br>
                            Delay: ${train.delay_minutes || 0} minutes
                        </p>
                    `;
                });
        }
    </script>
</body>
</html>