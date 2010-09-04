function appendNote(note)
{
	var s = "<tr id='" + note.key + "'>" +
	            "<td><input type='checkbox' name='keys[]' value='" + note.key + "'></td>" +
	            "<td class='title_field'>" + note.title + "</td>" +
	            "<td class='priority_field'></td>" +
	            "<td class='progress_field'></td>" +
	            "<td class='due_time_field'>" + note.due_time + "</td>" +
	        "</tr>";

	var trnode = $(s);

	var priority_node = trnode.children("td.priority_field")[0];
	var select = "<select class='priority'>";
	for(var i = 0; i <= 10; i++) {
		if (note.priority == i) {
			select += "<option value='" + i + "' selected>" + i + "</option>";
		} else {
			select += "<option value='" + i + "'>" + i + "</option>";
		}
	}
	select += "</select>";
	priority_node.innerHTML = select;

	var progress_node = trnode.children("td.progress_field")[0];
	select = "<select class='progress'>";
	for(var i = 0; i <= 100; i += 10) {
		if (note.progress == i) {
			select += "<option value='" + i + "' selected>" + i + "%</option>";
		} else {
			select += "<option value='" + i + "'>" + i + "%</option>";
		}
	}
	select += "</select>";
	progress_node.innerHTML = select;

	$("#tasksTable").append(trnode);
}

function refresh()
{
	url = '/rpc?action=read';

	url += '&sort=' + $("#sort_method").attr('value');
	url += '&hide_complete=' + $("#hide_complete").attr('checked');

	$.get(url, function(data) {
		$("#tasksTable").children().remove();
		for(key in data.notes) {
			appendNote(data.notes[key]);
		}

		$("select.priority").bind('change', update_priority);
		$("select.progress").bind('change', update_progress);
	});
}

function deleteSelected()
{
	$("input[name='keys[]']").each(function(){
		if ($(this).attr('checked')) {
			var key = $(this).attr('value');
			$('#' + key).remove();
			$.get('/rpc?action=delete&key=' + key);
		}
	});
}

function addNote()
{
	tmp = window.prompt("Title of new note", "");
	if (tmp) {
		url = "/rpc?action=create&title=" + tmp;
		$.get(url, refresh);
	}
}

function update_priority()
{
	var key = $(this).parent().parent().attr('id');
	var priority = $(this).attr('value');
	var url = "/rpc?action=update&key=" + key + "&priority=" + priority;
	$.get(url, refresh);
}

function update_progress()
{
	var key = $(this).parent().parent().attr('id');
	var progress = $(this).attr('value');
	var url = "/rpc?action=update&key=" + key + "&progress=" + progress;
	$.get(url, refresh);
}

$(document).ready(function() {  
	$("#add").bind('click', addNote);
	$("#delete").bind('click', deleteSelected);
	$("#refresh").bind('click', refresh);

	$("#sort_method").bind('change', refresh)
	$("#hide_complete").bind('change', refresh)

	refresh();
});
