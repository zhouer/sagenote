(function() {

var update = function() {
	var request = {
		action: "update",
		key: $("#key").attr('value'),
		title: $("#title_field").attr('value'),
		content: $("#content_field").attr('value'),
	}
	$.post("/rpc", request, function(data) {
		window.location.href = "/";
	});
};

var cancel = function() {
	window.location.href = "/";
};

$(document).ready(function() {  
	$("#update").bind('click', update);
	$("#cancel").bind('click', cancel);
});

})();
