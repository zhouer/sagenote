function appendNote(note)
{
	s = "<tr id='" + note.key + "'>" +
	    "<td><input type='checkbox' name='keys[]' value='" + note.key + "'></td>" +
	    "<td>" + note.create_time + "</td>" +
	    "<td>" + note.title + "</td>" +
	    "<td class='priority_field'>" + note.priority + "</td>" +
	    "<td class='progress_field'>" + note.progress + "</td>" +
	    "</tr>";
	$("#tasksTable").append(s);
}

function update()
{
	url = '/rpc?action=read';
	if (arguments.length == 1) {
		url += '&sort=' + arguments[0];
	}

	$.get(url, function(data) {
		$("#tasksTable").children().remove();
		for(key in data.notes) {
			appendNote(data.notes[key]);
		}

		$(".priority_field").bind('click', update_priority);
		$(".progress_field").bind('click', update_progress);
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

function refresh()
{
	// XXX: call update indirecttly to ignore click mouse event
	update();
}

function create_time()
{
	update('create_time');
}

function priority()
{
	update('priority');
}

function update_priority()
{
	key = $(this).parent().attr('id');
	tmp = window.prompt("Please input new priority", $(this).text());
	if (tmp) {
		url = "/rpc?action=update&key=" + key + "&priority=" + tmp;
		$.get(url, refresh);
	}
}

function update_progress()
{
	key = $(this).parent().attr('id');
	tmp = window.prompt("Please input new progress", $(this).text());
	if (tmp) {
		url = "/rpc?action=update&key=" + key + "&progress=" + tmp;
		$.get(url, refresh);
	}
}

$(document).ready(function() {  
	$("#delete").bind('click', deleteSelected);
	$("#refresh").bind('click', refresh);
	$("#create_time").bind('click', create_time);
	$("#priority").bind('click', priority);

	refresh();
});
