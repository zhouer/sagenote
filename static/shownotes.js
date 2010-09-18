(function() {

var appendNote = function(note) {
	var s = ["<tr id='", note.key, "'>",
	             "<td><input type='checkbox' name='keys[]' value='", note.key, "'></td>",
	             "<td class='title_field'>", note.title, "</td>",
	             "<td class='priority_field'></td>",
	             "<td class='progress_field'></td>",
	             "<td class='due_time_field'>", note.due_time, "</td>",
	         "</tr>"];

	var trnode = $(s.join(""));

	var priority_node = trnode.children("td.priority_field");
	var select = ["<select class='priority'>"];
	for(var i = 0; i <= 10; i++) {
		select.push("<option value='", i, "'>", i, "</option>");
	}
	select.push("</select>");
	priority_node.html(select.join(""));
	priority_node.children().attr("selectedIndex", note.priority);

	var progress_node = trnode.children("td.progress_field");
	select = ["<select class='progress'>"];
	for(var i = 0; i <= 100; i += 10) {
		select.push("<option value='", i, "'>", i, "%</option>");
	}
	select.push("</select>");
	progress_node.html(select.join(""));
	progress_node.children().attr("selectedIndex", (note.progress / 10));

	$("#tasksTable").append(trnode);
};

var refresh = function() {
	url = ["/rpc?action=read"];

	url.push("&sort=", $("#sort_method").attr("value"));
	url.push("&hide_complete=", $("#hide_complete").attr("checked"));

	$.get(url.join(""), function(data) {
		$("#tasksTable").children().remove();
		for(key in data.notes) {
			appendNote(data.notes[key]);
		}
	});
};

var deleteSelected = function() {
	$("input[name='keys[]']").each(function(){
		if ($(this).attr("checked")) {
			var key = $(this).attr("value");
			$("#" + key).remove();
			$.get("/rpc?action=delete&key=" + key);
		}
	});
};

var onKeyup = function(keyEvent) {
	if (keyEvent.keyCode != 13) {
		return;
	}
	createNote();
};

var createNote = function() {
	var node = $("#new_note");
	var title = node.attr("value");
	node.attr("value", "");

	if (title) {
		var request = {
			action: "create",
			title: title
		};
		$.post("/rpc", request, refresh);
	}
};

var update_priority = function () {
	var request = {
		action: "update",
		key: $(this).parent().parent().attr("id"),
		priority: $(this).attr("value")
	}
	$.post("/rpc", request, refresh);
};

var update_progress = function() {
	var request = {
		action: "update",
		key: $(this).parent().parent().attr("id"),
		progress: $(this).attr("value")
	}
	$.post("/rpc", request, refresh);
};

var show_note_detail = function () {
	var url = "/editnote/";
	url += $(this).parent().attr("id");
	window.location.href = url;
};

$(document).ready(function() {  
	$("#delete").bind("click", deleteSelected);
	$("#refresh").bind("click", refresh);

	$("#sort_method").bind("change", refresh)
	$("#hide_complete").bind("change", refresh)

	$("#new_note").bind("keyup", onKeyup);
	$("#create").bind("click", createNote);

	$("select.priority").live("change", update_priority);
	$("select.progress").live("change", update_progress);
	$("td.title_field").live("dblclick", show_note_detail);

	refresh();
});

})();
