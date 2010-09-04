function appendNote(note)
{
	s = "<tr id='" + note.key + "'>" +
	    "<td><input type='checkbox' name='keys[]' value='" + note.key + "'></td>" +
	    "<td>" + note.create_time + "</td>" +
	    "<td>" + note.title + "</td>" +
	    "<td>" + note.priority + "</td>" +
	    "<td>" + note.progress + "</td>" +
	    "</tr>";
	$("#tasksTable").append(s);
}

function refresh(sort)
{
	url = '/rpc?action=read';
	if (sort != undefined) {
		url += '&sort=' + sort;
	}

	$.get(url, function(data) {
		$("#tasksTable").children().remove();
		for(key in data.notes) {
			appendNote(data.notes[key]);
		}
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

function create_time()
{
	refresh('create_time');
}

function priority()
{
	refresh('priority');
}

$(document).ready(function() {  
	$("#delete").bind('click', deleteSelected);
	$("#refresh").bind('click', refresh);
	$("#create_time").bind('click', create_time);
	$("#priority").bind('click', priority);
	refresh();
});
