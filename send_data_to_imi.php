<?php
// echo "Hello World\n" ;
// echo "\n".$_SERVER['SERVER_NAME'];
// echo "\n".$_SERVER['SERVER_ADDR'];
// echo "\n".$_SERVER['GATEWAY_INTERFACE'];
// echo "\n".$_SERVER['SERVER_PROTOCOL'];

// echo "\n  <br/> here are http deyails:";  // https://www.php.net/manual/en/reserved.variables.server.php 
// // // webs server creates these entries
// echo "\n <br/>HTTP_CONNECTION: ".$_SERVER['HTTP_CONNECTION'];
// echo "\n <br/>HTTP_ACCEPT: ".$_SERVER['HTTP_ACCEPT'];
// echo "\n <br/>REQUEST_METHOD: ".$_SERVER['REQUEST_METHOD'];
// echo "\n <br/>QUERY_STRING: ".$_SERVER['QUERY_STRING'];
// echo " <br/>HTTP_HOST: ".$_SERVER['HTTP_HOST'];
// echo " <br/>REQUEST_URI: ".$_SERVER['REQUEST_URI'];
// echo "<br/>";

//try to get all the headers  // WORKS !!! browser and imi are 2 clients both have diiferent headers
// // https://www.geeksforgeeks.org/how-to-read-any-request-header-in-php/
// echo "\n getting all headers <br/>";
// // foreach (getallheaders() as $name => $value) {
// // 	echo "$name: $value <br>";
// // }
// $header = apache_request_headers();
// foreach ($header as $headers => $value) {
// 	echo "$headers: $value <br />\n";
// }

$da = file_get_contents('php://input'); 
// echo "\n <br/>I received http body: " ;
$dat = explode(",",$da);
$data = explode(":",$dat[2]);
$trimmed = substr($data[1], 0, strlen($data[1])-3); //add a check to trim extra chars
// echo "\n data[1]= ".$trimmed;
$no = substr($trimmed, -10);
// echo "\n <br/>I received http data:";
// echo "\n user no= ".$no;


//include database stuff and functions
include "loudblog/custom/config.php";
include "loudblog/inc/database/adodb.inc.php";
include "loudblog/inc/connect.php";
include "loudblog/inc/functions.php";

//create some important globals
if (!isset($db['host'])) {
    die("<br /><br />Cannot find a valid configuration file! <a href=\"install.php\">Install Loudblog now!</a>");
}

$GLOBALS['prefix']     = $db['pref'];
$GLOBALS['path']       = $lb_path;
$GLOBALS['audiopath']  = $lb_path . "/audio/";
$GLOBALS['uploadpath'] = $lb_path . "/upload/";


// $status_values = array("" => "", "ON AIR" => 3, "DRAFT" => 1, "ES" => 5, "MODENC" => 6, "NTR" => 7, "STR" => 4,"FINISHED" => 2 );
$status_values = array(1  => "DRAFT", 2 => "FINISHED" , 3 => "ON AIR", 4 => "STR", 5 =>"ES" , 6 => "MODENC", 7 =>"NTR"  );
// //entries for Videos
$dosql = "SELECT * FROM ".$GLOBALS['prefix']."lb_postings WHERE user = '". $no ."' AND video_file IS NOT NULL order by id DESC";
$result = $GLOBALS['lbdata']->GetArray($dosql);

$rows_total = count($result);
$k = 3 ;
$rows = min($k, $rows_total);
// echo "\n".$rows."\n";
for ($row = 0; $row < $rows; $row++) {
	$entry_num=$row+1 ;
	echo $entry_num.") ";
	if(is_null($result[$row]['video_link']) || $result[$row]['video_link']== "" ){
		echo "Video not published!"." Received it on our server on: ".$result[$row]['posted'].". It has status= ".$status_values[$result[$row]['status']]." Contact team with reference id: ".$result[$row]['id'];
    	echo "\n";
	}
	else{
		echo "Your video has been published at: ".$result[$row]['video_link'];
    	echo "\n";
	}
}
if($rows== 0)
	echo "no videos received from this number\n";

// // Audio entries
$dosql = "SELECT * FROM ".$GLOBALS['prefix']."lb_postings WHERE user = '". $no ."' AND video_file IS NULL order by id DESC";
$result = $GLOBALS['lbdata']->GetArray($dosql);
$rows_total = count($result);
$k = 3 ;
$rows = min($k, $rows_total);
echo "\n \nAudio entries: \n" ;
for ($row = 0; $row < $rows; $row++) {
	$entry_num=$row+1 ;
	echo $entry_num.") ";
	if($result[$row]['status'] != 3){
		echo "your audio is not published. It has status= ".$status_values[$result[$row]['status']];
    	echo "\n";
	}
	else{
		$audio_id= $result[$row]['id'];
		echo "Your audio has been published at: http://cgnetswara.org/index.php?id=".$audio_id;
    	echo "\n";
	}
}
if($rows== 0)
	echo "no audios received from this number\n";


 //    if(!is_null($result[$row]['video_link'])){
	// 	echo "posted on: ".$result[$row]['posted']."\treference id: ".$result[$row]['id']."\tvideo link:".$result[$row]['video_link'];
 //    	echo "\n";
	// }

// //nothing works below this 
// // // decode the body which is in JSON : not works
// $url = 'https://api.imiconnect.in/resources/v1/messaging';
// $response = curl_exec($curl);
// $header_size = curl_getinfo($response, CURLINFO_HEADER_SIZE);
// $header = substr($response, 0, $header_size);
// $body = substr($response, $header_size);
// $err = curl_error($curl);
// if($err){die("Connection Failure");}
// echo $response ; 
// $body = json_decode($body);
// echo $body ; 
// curl_close($curl);

// if(empty($_POST)){ // this is empty!!! 
// // https://stackoverflow.com/questions/58985247/how-can-i-properly-listen-to-http-json-post-requests-in-php
// 	echo "post is empty";
// }

// try post request : not works
// $request_json = $_POST["number"];
// $request = json_decode($request_json);
// print_r($request);

// $request_json2 = $_POST["time"];
// $request2 = json_decode($request_json2);
// print_r($request2);

// header('content-type:application/json');

// if (!empty($_POST)){
//  // Post was sent and you can do stuff with it and response
// 	$arr = array('a' => 1, 'b' => 2, 'c' => 3, 'd' => 4, 'e' => 5);
//  	echo json_encode($arr);
//  }

// define the URL to load
// $url = 'https://api.imiconnect.in/resources/v1/messaging';
// $url = 'https://e1d482c2e144966d3e2195d6d5fddb36.m.pipedream.net';
// // get headers and body from the https request
// $ch = curl_init();
// curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// curl_setopt($ch, CURLOPT_HEADER, 1);
// // ...

// $response = curl_exec($ch);

// // Then, after your curl_exec call:
// $header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
// $header = substr($response, 0, $header_size);
// $body = substr($response, $header_size);

// curl_close($ch);
// display the output
// echo "\nheader=".$header;
// echo "\n body=".$body;

// start cURL
// $ch = curl_init(); 
// // tell cURL what the URL is
// curl_setopt($ch, CURLOPT_URL, $url); 
// // tell cURL that you want the data back from that URL
// curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
// // run cURL
// $output = curl_exec($ch); 
// // end the cURL call (this also cleans up memory so it is 
// // important)
// curl_close($ch);
// // display the output
// echo $output;



// post request
// $handle = curl_init('https://eny6pk6ixhxnm.x.pipedream.net/');

// $data = [
//     'name' => 'Priyanka',
//     'location' => 'Balaji'
// ];

// $encodedData = json_encode($data);

// curl_setopt($handle, CURLOPT_POST, 1);
// curl_setopt($handle, CURLOPT_POSTFIELDS, $encodedData);
// curl_setopt($handle, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

// $result = curl_exec($handle);

// GET request 
// $curl = curl_init();

// curl_setopt_array($curl, array(
//   CURLOPT_URL => "https://eny6pk6ixhxnm.x.pipedream.net/",
//   CURLOPT_RETURNTRANSFER => true,
//   CURLOPT_TIMEOUT => 30,
//   CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
//   CURLOPT_CUSTOMREQUEST => "GET",
//   CURLOPT_HTTPHEADER => array(
//     "cache-control: no-cache",
//     "second header: Priyanka",
//     'Content-Type: application/json'
//   ),
// ));

// $response = curl_exec($curl);
// echo $response ; 
// // $response = json_decode($response);
// echo $response['id'] ; 
// $err = curl_error($curl);
// if($err){die("Connection Failure");}


// curl_close($curl);



?>
