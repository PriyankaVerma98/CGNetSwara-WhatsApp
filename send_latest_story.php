<?php
//sends latest story
	$request_body = file_get_contents('php://input'); 

	//include database stuff and functions
	include "loudblog/custom/config.php";
	include "loudblog/inc/database/adodb.inc.php";
	include "loudblog/inc/connect.php";
	include "loudblog/inc/functions.php";

	if (!isset($db['host'])) {
	    die("<br /><br />Cannot find a valid configuration file!");
	}

	$GLOBALS['prefix']     = $db['pref'];

	echo "Enjoy this latest story!\n";
	$rows_total = 7 ; 
	$dosql = "SELECT * FROM ".$GLOBALS['prefix']."lb_postings WHERE status = '3' and posted < now() order by posted DESC limit ".$rows_total;
	$result = $GLOBALS['lbdata']->GetArray($dosql);
	$row = rand(0,$rows_total-1) ;
	
	// $dosql = "SELECT * FROM ".$GLOBALS['prefix']."lb_postings WHERE id = '187600'"; // testing done for YouTube video
	// $result = $GLOBALS['lbdata']->GetArray($dosql);
	// $row = rand(0,0) ;

	if($result[$row]['video_link']!= "" and !is_null($result[$row]['video_link'])){ // sends the YouTube link
		echo $result[$row]['video_link'];
	}
	else {
		echo "http://cgnetswara.org/index.php?id=".$result[$row]['id'];
	}
	
?>
