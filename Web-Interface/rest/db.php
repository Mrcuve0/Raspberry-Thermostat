
<?php

class DbManager {

    //Database configuration
    private $dbhost = '127.0.0.1';//'thermostat.local';
    private $dbport = '27017';
    private $conn;

    function __construct() {
        //Connecting to MongoDB
        try {
            //Establish database connection
            $this->conn = new MongoDB\Driver\Manager('mongodb://'.$this->dbhost.':'.$this->dbport);
        } catch (MongoDB\Driver\Exception\Exception $e) {
            echo $e->getMessage();
            echo nl2br("n");
        }
    }

    function getConnection() {
        return $this->conn;
    }

}

?>

