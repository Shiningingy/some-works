<!DOCTYPE html>
<html lang="en">
<!-- Zili Luo -->	
	<head>
		<?php include_once "functions.php" ?>
		<?php include_once "search.php" ?>
		<?php print_head("Search Result",False) ?>
	</head>
	<body>
		<?php include_once "header.php" ?>

		<!--Search Content-->
		<article class="mainContent">
			<div class="content">
				<?php 
				$searchInput = $_GET["Search"];
				$data = filter_var(trim($searchInput), FILTER_SANITIZE_STRING);
				$result = search_for_term($data);
				print_searchResults($result,$searchInput);
				?>
			</div>
		</article>

		<?php include_once "footer.php" ?>
	</body>
</html>