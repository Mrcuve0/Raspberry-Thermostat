
<?php

// Requests' required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

// Db library
include_once '../db.php';

// Take roomdata collection
$dbname = 'thermodb';
$collection = 'roomData_coll';

// Db connection
$db = new DbManager();
$conn = $db->getConnection();

// Read all records
$filter = [];
$option = [];
$read = new MongoDB\Driver\Query($filter, $option);
$records = $conn->executeQuery("$dbname.$collection", $read);

// Return just the first element: this is equivalent to a mongodb find_one request
echo json_encode($records->toArray()[0]);

// Alternative to return all the records
//echo json_encode(iterator_to_array($records));

?>
