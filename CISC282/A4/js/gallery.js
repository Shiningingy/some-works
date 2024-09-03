$(document).ready(function() {
  $('.thumbnail-gallery').magnificPopup({
	  delegate: 'a', // child items selector, by clicking on it popup will open
	  type: 'image',
	  gallery:{
	    enabled:true
	  },
	  image:{
	  	titleSrc: function(item){
	  		return $(item.el["context"]).children()[0].alt
	  	}
	  }
	  // other options
	});
});

