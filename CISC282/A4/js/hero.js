$(document).ready(function(){
    var index = 0
	setInterval(Heroimg,5000);

	function Heroimg(){
		var urls = ["bee-collecting-pollen.jpg","field-and-tractors.jpg","dew-on-grass.jpg"]
		var next = (index+1)%3
		$('.HeroContainer').css('background-image','url(../a4/img/'+ urls[index] +')').fadeOut("slow",function(){
			$('.HeroContainer').css('background-image','url(../a4/img/'+ urls[next] +')').fadeIn("slow");
		});
		index = next
	}
});