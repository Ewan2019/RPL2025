<?php
class TrainTracking {
    private $conn;

    public function __construct($db) {
        $this->conn = $db;
    }

    // Get all trains with their current location
    public function getTrains() {
        $query = "SELECT t.train_id, t.train_number, t.train_name, 
                         s.schedule_id, s.departure_time, s.arrival_time, s.status,
                         tr.tracking_id, tr.latitude, tr.longitude, tr.delay_minutes,
                         st.station_name as current_station
                  FROM trains t
                  LEFT JOIN schedules s ON t.train_id = s.train_id
                  LEFT JOIN tracking tr ON s.schedule_id = tr.schedule_id
                  LEFT JOIN stations st ON tr.current_station_id = st.station_id
                  WHERE s.departure_time >= CURDATE()
                  ORDER BY s.departure_time";

        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    // Get specific train location
    public function getTrainLocation($train_id) {
        $query = "SELECT t.train_id, t.train_number, t.train_name,
                         tr.latitude, tr.longitude, tr.delay_minutes,
                         st.station_name as current_station,
                         s.status, s.departure_time, s.arrival_time
                  FROM trains t
                  LEFT JOIN schedules s ON t.train_id = s.train_id
                  LEFT JOIN tracking tr ON s.schedule_id = tr.schedule_id
                  LEFT JOIN stations st ON tr.current_station_id = st.station_id
                  WHERE t.train_id = ?
                  AND s.departure_time >= CURDATE()
                  LIMIT 1";

        $stmt = $this->conn->prepare($query);
        $stmt->execute([$train_id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }

    // Update train location
    public function updateLocation($tracking_id, $latitude, $longitude, $delay_minutes = 0) {
        $query = "UPDATE tracking 
                 SET latitude = ?, longitude = ?, delay_minutes = ?,
                     last_update = CURRENT_TIMESTAMP
                 WHERE tracking_id = ?";

        $stmt = $this->conn->prepare($query);
        return $stmt->execute([$latitude, $longitude, $delay_minutes, $tracking_id]);
    }

    // Predict delay based on historical data and current conditions
    public function predictDelay($schedule_id) {
        // Simple delay prediction based on current delay
        $query = "SELECT delay_minutes, 
                        CASE 
                            WHEN delay_minutes > 30 THEN delay_minutes + 15
                            WHEN delay_minutes > 15 THEN delay_minutes + 10
                            WHEN delay_minutes > 0 THEN delay_minutes + 5
                            ELSE 0
                        END as predicted_delay
                 FROM tracking 
                 WHERE schedule_id = ?";

        $stmt = $this->conn->prepare($query);
        $stmt->execute([$schedule_id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }
}
?>