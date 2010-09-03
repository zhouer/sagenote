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
		notes = data.notes.sort(function(x, y) {
			return x.order - y.order;
		});

		$("#tasksTable").children().remove();
		for(key in notes) {
			appendNote(notes[key]);
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
