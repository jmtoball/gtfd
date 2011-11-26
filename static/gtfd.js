$(document).ready(function($){
	$("a.view").click(function(){
		$(this).parent().next("h3").nextUntil("h3", "p").slideToggle();
	});
	var mapping = Object();
	var count = 0;
	$(".tag").each(function(){
		var tag = $(this).text();
		if(!mapping[tag]){
			count++;
			mapping[tag] = -1;
		}
	});
	var i = 0;
	var step = 360/count;
	$(".tag").each(function(){
		var tag = $(this).text();
		var hue = 0;
		if(mapping[tag] == -1){
			mapping[tag] = step * (i++);
		}
		$(this).css("background", "hsl("+mapping[tag]+", 100%, 25%)");
	});
	var todo_count = $("#tasks_todo li").length;
	$("#todo_toggle").text($("#todo_toggle").text()+" ["+todo_count+"]");
	var done_count = $("#tasks_done li").length;
	$("#done_toggle").text($("#done_toggle").text()+" ["+done_count+"]");
	$("#todo_toggle").click(function(){
		$("#tasks_todo").slideToggle();
	});
	$("#done_toggle").click(function(){
		$("#tasks_done").slideToggle();
	});
});

