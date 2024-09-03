<?php
function print_head($title,$permit_popUp=True){
	echo "	<meta charset=\"UTF-8\">\n";
	echo "	<meta name = \"author\" content =\"Zili Luo\"/>\n";
	echo "	<meta name = \"viewport\" content=\"width=device-width, initial-scale=1\"/>\n";
	echo "	<link rel=\"stylesheet\" type=\"text/css\" href=\"/~15zl35/a5/css/icons.css\">\n";
	echo "	<link rel=\"stylesheet\" type=\"text/css\" href=\"/~15zl35/a5/css/a5.css\">\n";
	echo "\n";
	echo "	<!-- jQuery 1.7.2+ or Zepto.js 1.0+ -->\n";
	echo "	<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\n";
	echo "\n";
	if($permit_popUp){
		echo "	<link rel=\"stylesheet\" href=\"/~15zl35/a5/css/magnific-popup.css\">\n";
		echo "	<script src=\"/~15zl35/a5/js/jquery.magnific-popup.js\"></script>";
		echo "	<script src=\"/~15zl35/a5/js/gallery.js\"></script>\n";
	}
	echo "	<script src=\"/~15zl35/a5/js/hero.js\"></script>\n";
	echo "	<script src=\"/~15zl35/a5/js/a5.js\"></script>\n";
	echo "	<title> $title </title>";
}

function print_searchResults($result_array,$searchInput){
	echo "<h1>Search result</h1>";
	$length = count($result_array);
	if($length == 0){
		echo "<p>Sorry,but there were no matches for \"{$searchInput}\".</p>";
		return;
	}else{
		echo "<p>Your search for \"{$searchInput}\" produced $length result(s).</p>";
	}
	echo "<ul>";
	foreach ($result_array as $result) {
		echo "<li><a href={$result[CONTENT_LINK]} target=\"_top\"><p class=\"blueLink\">{$result[CONTENT_TITLE]}</p></a></li>";
	}
	echo "</ul>";

}
?>