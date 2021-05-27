<?php
	$request_body = file_get_contents('php://input'); 
	$string = $request_body; //your string

	$start_sqb = strpos($string, "[");
	$end_sqb =  strrpos($string, "]");
	$contacts = substr($string, $start_sqb, $end_sqb-$start_sqb+1); //careful with index

	str_replace ('\n','', $contacts);
	str_replace (' ','', $contacts);

	// check if string is in valid utf-8 encoded
	// $isUTF8 = preg_match('//u', $contacts); yes
	// echo "\n isUTF ".$validUTF8 ; 

	// echo json_last_error(); //4 = JSON_ERROR_SYNTAX . Fixed!
	// check if string is in valid json format or not at https://jsonformatter.curiousconcept.com/#
	$output = json_decode($contacts, true) ; // output is an associate array
	// var_dump($output);


	//include database stuff and functions
	include "loudblog/custom/config.php";
	include "loudblog/inc/database/adodb.inc.php";
	include "loudblog/inc/connect.php";
	include "loudblog/inc/functions.php";
	$GLOBALS['prefix']     = $db['pref']; //defined in config as empty string
	
	$nos_arr=array();
	$total_nos = count($output[0]["phones"]); // no of phone numbers received in contact card 
	for ($i=0 ; $i<$total_nos ; $i++){
		$no = $output[0]["phones"][$i]["phone"];
		// clean up the number
		$no = str_replace(" ","",$no); // trim spaces
		$no = str_replace("(","",$no); // trim brackets
		$no = str_replace(")","",$no); // trim brackets
		$no = str_replace("-","",$no); 
		$no = substr($no, -10); // don't want +91
		// echo "\nno= ".$no;
		array_push($nos_arr, $no);
	}

	if($total_nos ==0){
		echo "No number was found in the contact card!\n";
	}
	else{
		$nos_query = $nos_arr[0];
		for($i= 1 ; $i<$total_nos ; $i++){
			$temp = "' OR user = '".$nos_arr[$i]; 
			$nos_query = $nos_query.$temp ; 
		}
		$dosql = "SELECT * FROM ".$GLOBALS['prefix']."lb_postings WHERE status = '3' AND (user = '".$nos_query."' ) order by posted DESC";
		// echo $dosql ;
		$result = $GLOBALS['lbdata']->GetArray($dosql);
		$rows_total = count($result);
		$k = 5 ;
		$rows = min($k, $rows_total);
		// echo "\nrows total".rows_total;

		for ($row = 0; $row < $rows; $row++) {
			if($row==0) echo "\nHere are the stories: \n" ;
			$entry_num=$row+1 ;
			echo $entry_num.") ";
			if(is_null($result[$row]['video_file']) || $result[$row]['video_file']== "" ){ //audio story
				$audio_id= $result[$row]['id'];
				echo "Audio at: http://cgnetswara.org/index.php?id=".$audio_id;
		    	echo "\n";
			}
			else{
				if(is_null($result[$row]['video_link']) || $result[$row]['video_link']== "" ){ // video is not on YT
					echo "Video on website at: http://cgnetswara.org/index.php?id=".$result[$row]['id'];
					echo " Contact our team to get the video published on YouTube! ";
					echo "\n";
				}
				else{
					echo "Video on YouTube at: ".$result[$row]['video_link']; //yt link is available
		    		echo "\n";
				}
		
			}
		}
		if($rows== 0)
		echo "No stories have been received from that number!\n";

	}

?>

