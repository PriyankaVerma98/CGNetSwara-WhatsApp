<?php
// send back status of stories

$request_body = file_get_contents('php://input'); 
$arr = explode(",",$request_body); 

$user = explode(":",$arr[0])[1];			
$user= str_replace("\"","",$user); // removes spaces 
$no = substr($user, -10); // remove 91

// $owner = explode(":",$arr[1])[1];			// add checks whether user not typed extra characters
// $owner= str_replace("\"","",$owner);


// echo "\n user=".$no ;
// echo "\n owner=".($owner) ;

//include database stuff and functions
include "loudblog/custom/config.php";
include "loudblog/inc/database/adodb.inc.php";
include "loudblog/inc/connect.php";
include "loudblog/inc/functions.php";

//create some important globals
if (!isset($db['host'])) {
    die("<br /><br />Cannot find a valid configuration file!");
}

$GLOBALS['prefix']     = $db['pref'];
$GLOBALS['path']       = $lb_path;
$GLOBALS['audiopath']  = $lb_path . "/audio/";
$GLOBALS['uploadpath'] = $lb_path . "/upload/";


// $status_values = array("" => "", "ON AIR" => 3, "DRAFT" => 1, "ES" => 5, "MODENC" => 6, "NTR" => 7, "STR" => 4,"FINISHED" => 2 );
$status_values = array(1  => "DRAFT", 2 => "FINISHED" , 3 => "ON AIR", 4 => "STR", 5 =>"ES" , 6 => "MODENC", 7 =>"NTR"  );


// //entries for Videos
$dosql = "SELECT * FROM ".$GLOBALS['prefix']."lb_postings WHERE user = '".$no."' AND status <> 3 order by posted DESC";
$result = $GLOBALS['lbdata']->GetArray($dosql);

$rows_total = count($result);
$k = 5 ;
$rows = min($k, $rows_total);

for ($row = 0; $row < $rows; $row++) {
	if($row==0) echo "\n \nStatus: \n" ;
	$entry_num=$row+1 ;
	echo $entry_num.") ";
	if(is_null($result[$row]['video_file']) || $result[$row]['video_file']== "" ){ // it is audio story
		$audio_id= $result[$row]['id'];
		echo "Audio posted on ".$result[$row]['posted']." has status: ".$status_values[$result[$row]['status']];
    	echo "\n";
	}
	else{ // video story
		echo "Video posted on ".$result[$row]['posted']." has status: ".$status_values[$result[$row]['status']];
    	echo "\n";
	}
}
if($rows== 0)
	echo "No stories have been received from your number!\n";


?>
