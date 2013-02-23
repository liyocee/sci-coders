$(document).ready(function() { 
	$('ul.menu').superfish({ 
		delay:       800,                            // one second delay on mouseout 
		animation:   {opacity:'show',height:'show'},  // fade-in and slide-down animation 
		speed:       'normal',                          // faster animation speed 
		autoArrows:  false,                           // disable generation of arrow mark-up 
		dropShadows: false                            // disable drop shadows 
	}); 
}); 

$(function () {					
	$('.menu li.active').find('span').css({width:'100%', left:'0'});
	$('.menu li').not('.active')
	.hover(function(){
		$(this).find('span')
		.stop().animate({width:'100%', left:'0'}, {duration:200})
	}, function(){
		$(this).not('.sfHover').find('span')
		.stop().animate({width:'0', left:'50%'}, {duration:200})
	});
	
	$('.link-1')
	.hover(function(){
		$(this).find('span')
		.css({left:'18px'}).stop().animate({left:'100%'}, {duration:200})
	}, function(){
		$(this).find('span')
		.css({left:'18px', width:'0'}).stop().animate({width:'100%'}, {duration:250})
	});
	
	$('.link-2')
	.hover(function(){
		$(this).find('span')
		.css({left:'18px'}).stop().animate({left:'100%'}, {duration:200})
	}, function(){
		$(this).find('span')
		.css({left:'18px', width:'0'}).stop().animate({width:'100%'}, {duration:250})
	});
	
	$('.link-3')
	.hover(function(){
		$(this).find('span')
		.css({left:'0'}).stop().animate({left:'100%'}, {duration:200})
	}, function(){
		$(this).find('span')
		.css({left:'0', width:'0'}).stop().animate({width:'100%'}, {duration:250})
	});
	
	$('.list-services a')
	.hover(function(){
		$(this).stop().animate({color:'#df3c4b'}, {duration:250})
	}, function(){
		$(this).stop().animate({color:'#6d6d6d'}, {duration:250})
	});
	
	$('.list-1 a')
	.hover(function(){
		$(this).stop().animate({color:'#df3c4b'}, {duration:200})
	}, function(){
		$(this).stop().animate({color:'#565656'}, {duration:200})
	});
	
	$('.footer-text a')
	.hover(function(){
		$(this).find('span')
		.stop().animate({width:'100%', left:0}, {duration:250})
	}, function(){
		$(this).find('span')
		.stop().animate({width:0, left:'50%'}, {duration:250})
	});
	
	$('.footer-menu a.active').find('span').css({width:'100%', left:'0'});
	$('.footer-menu a').not('.active')
	.hover(function(){
		$(this).find('span')
		.stop().animate({width:'100%', left:0}, {duration:200})
	}, function(){
		$(this).find('span')
		.stop().animate({width:0, left:'50%'}, {duration:200})
	});
});