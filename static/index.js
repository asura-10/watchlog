$(document).ready(function(){
	$.ajax({
		type: "POST",
		url: "/get_ip_list",
		data: " ",
		success: function(msg){
			$("#ip").append("<option value =" + msg + ">" + msg +"</option>");
		}
	});
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('my response', function(msg) {
		var value_new = $('#log').val() + "\n" + msg.data;
		$('#log').val(value_new);
		//alert(msg.data);
		//$('#log').append(msg.data);

        //$('#log').append('<p>Received: ' + msg.data + '</p>');
    });
    $('form#select_form').submit(function(event) {
		$('#log').val("")
        socket.emit('my event', {ip: $('#ip').val(), dir: $('#dir').val(), file: $('#file').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });

	$('#log').scrollTop($('#log')[0].scrollHeight);

	$("#dir").click(function(){
		$.post(
			"/get_dir_list",
			{ip: $('#ip').val()},

			function(data, status){
				$("#dir").empty();
				var dirs = data.split(' ');
				dirs.forEach(function(e){
					$('#dir').append('<option value =' + e + '>' + e +'</option>');
				})
			}
		);
	});
	$("#file").click(function(){
		$.post(
			"/get_file_list",
			{
				ip: $('#ip').val(),
				dir: $('#dir').val()
			},

			function(data, status){
				$("#file").empty();
				var dirs = data.split(' ');
				dirs.forEach(function(e){
					$('#file').append('<option value =' + e + '>' + e +'</option>');
				})
			}
		);
	});
});