$(document).ready(function(){
	$("#theSearchForm").bind("submit",function(evevt){
		var inputText = $("#searchinput").val()
		if ((inputText.length==0)||(inputText.trim().length==0)) {
			alert("Search input invalied");
			event.preventDefault();
			// returnToPreviousPage();
		}
	}) 
})