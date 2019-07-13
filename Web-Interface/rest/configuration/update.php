<?php

// Requests' required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// Db library
include_once '../db.php';

// Take config collection
$dbname = 'thermodb';
$collection = 'config_coll';

// Db connection
$db = new DbManager();
$conn = $db->getConnection();

// Take the request's body as input
$data = json_decode(file_get_contents("php://input", true));
// Extract the ID of the input configuration
$doc_id = $data->{'_id'}->{'$oid'};
$doc_id = new MongoDB\BSON\ObjectId($doc_id);
// Delete the ID field from the input configuration
unset($data->{'_id'});

// Update the configuration
$insert = new MongoDB\Driver\BulkWrite();
$insert->update(['_id' => $doc_id], $data, ['upsert' => false]);
$result = $conn->executeBulkWrite("$dbname.$collection", $insert);

// Verify the update
if ($result->getModifiedCount() == 1) {
    echo json_encode(
                array("message" => "Record successfully updated")
        );
} else {
    echo json_encode(
            array("message" => "Error while updating record")
    );
}

?>
