<?php
// api/index.php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

include_once '../config/db.php';
include_once '../classes/TrainTracking.php';

$database = new Database();
$db = $database->getConnection();
$train = new TrainTracking($db);

$method = $_SERVER['REQUEST_METHOD'];
$action = isset($_GET['action']) ? $_GET['action'] : '';

switch($method) {
    case 'GET':
        switch($action) {
            case 'all':
                $trains = $train->getTrains();
                echo json_encode($trains);
                break;

            case 'location':
                $train_id = isset($_GET['train_id']) ? $_GET['train_id'] : die();
                $location = $train->getTrainLocation($train_id);
                echo json_encode($location);
                break;

            case 'predict':
                $schedule_id = isset($_GET['schedule_id']) ? $_GET['schedule_id'] : die();
                $prediction = $train->predictDelay($schedule_id);
                echo json_encode($prediction);
                break;

            default:
                echo json_encode(array("message" => "Invalid action"));
        }
        break;

    case 'POST':
        switch($action) {
            case 'update':
                $data = json_decode(file_get_contents("php://input"));
                
                if(
                    !empty($data->tracking_id) &&
                    !empty($data->latitude) &&
                    !empty($data->longitude)
                ) {
                    if($train->updateLocation(
                        $data->tracking_id,
                        $data->latitude,
                        $data->longitude,
                        $data->delay_minutes ?? 0
                    )) {
                        echo json_encode(array("message" => "Location updated"));
                    } else {
                        echo json_encode(array("message" => "Unable to update location"));
                    }
                } else {
                    echo json_encode(array("message" => "Missing required data"));
                }
                break;

            default:
                echo json_encode(array("message" => "Invalid action"));
        }
        break;

    default:
        echo json_encode(array("message" => "Invalid method"));
        break;
}
?>