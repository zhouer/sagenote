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

function refresh()
{
	$.get('/rpc?action=read', function(data) {
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

$(document).ready(function() {  
	$("#delete").bind('click', deleteSelected);
	$("#refresh").bind('click', refresh);
});  
