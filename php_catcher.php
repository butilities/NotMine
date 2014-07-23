<?php
// Simple PHP catcher for naughty purposes
// Taken from this awesome work: http://sethsec.blogspot.co.uk/2014/07/crossdomain-bing.html

$data = file_get_contents("php://input");
$ret = file_put_contents('/tmp/yourfile.txt', $data, FILE_APPEND | LOCK_EX);
if($ret == false) {
	die('Error writing to file');
}
else {
	echo "$ret bytes written to file";
}
?>
