<?php
// send 1 media at a time

// Find details about the User and what is wanted
$request_body = file_get_contents('php://input'); 
$arr = explode(",",$request_body); 

$user = explode(":",$arr[0])[1];			
$user= str_replace("\"","",$user);
$user= str_replace("\n","",$user);
$user = substr($user, -10); // remove 91

$owner = explode(":",$arr[1])[1];			
$owner= str_replace("\"","",$owner);
$owner= str_replace(" ","",$owner);  // replace any extra spaces typed by user
$owner= str_replace("\n","",$owner);
$owner = substr($owner, -10); // remove 91


// echo "\n user=".$user ;
// echo "\n owner=".($owner) ;


// find what we have in Database

//include database stuff and functions
include "loudblog/custom/config.php";
include "loudblog/inc/database/adodb.inc.php";
include "loudblog/inc/connect.php";
include "loudblog/inc/functions.php";

$GLOBALS['prefix']     = $db['pref']; //defined in config as empty string
$GLOBALS['path']       = $lb_path;
$GLOBALS['audiopath']  = $lb_path . "/audio/";
$GLOBALS['uploadpath'] = $lb_path . "/upload/";


$dosql = "SELECT * FROM ".$GLOBALS['prefix']."lb_postings WHERE user = '".$owner."'". "AND status = '3' order by posted DESC";
$result = $GLOBALS['lbdata']->GetArray($dosql);
$rows_total = count($result);
$k = 5 ;
$rows = min($k, $rows_total);

for ($row = 0; $row < $rows; $row++) {
	if($row==0) echo "\n \nHere are the stories: \n" ;
	$entry_num=$row+1 ;
	echo $entry_num.") ";
	if(is_null($result[$row]['video_file']) || $result[$row]['video_file']== "" ){ //audio story
		$audio_id= $result[$row]['id'];
		echo "Audio has been published at: http://cgnetswara.org/index.php?id=".$audio_id;
    	echo "\n";
	}
	else{
		if(is_null($result[$row]['video_link']) || $result[$row]['video_link']== "" ){ // video is not on YT
			echo "Video has been published on Website at: http://cgnetswara.org/index.php?id=".$result[$row]['id'];
			echo " Contact our team to get the video published on YouTube! ";
			echo "\n";
		}
		else{
			echo "Video has been published on YouTube at: ".$result[$row]['video_link']; //yt link is available
    		echo "\n";
		}
		
	}
}
if($rows== 0)
	echo "No stories have been received from that number!\n";


?>
