$(document).ready(function(){
    $.ajax({
        type: "POST",
        url: "/get_ip_list",
        data: " ",
        success: function(msg){
            var ips = msg.split(' ');
            ips.forEach(function(e){
                $("#ip").append("<option value =" + e + ">" + e +"</option>");
            })
        }
    });

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var textarea = document.getElementById('log_ol');
    var line_array = new Array();
    socket.on('my response', function(msg) {
        filter = $('#filter').val()
        line_array.push(msg.data);
        //alert(line_array.join());
        
        var new_array = new Array();
        $('#log_ol').empty();
        line_array.forEach(function(line){
            if (filter != '')
            {
                if (line.match(filter) != null)
                {
                    new_line = line.replace(filter, '<span style="color:red">' + filter + '</span>');
                    $('#log_ol').append('<li>' + new_line + '</li>');
                }
            }
            else
            {
                $('#log_ol').append('<li>' + line + '</li>');
            }
        })

        //$('#log_ol').val(value_new);
        if ($('#scroll').val() == "Stop scroll")
            {
                textarea.scrollTop = textarea.scrollHeight;
            }
    });
    $('form#select_form').submit(function(event) {
        $('#log_ol').val("")
        socket.emit('my event', {ip: $('#ip').val(), dir: $('#dir').val(), file: $('#file').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });

    $('#filter').keyup(function(){
        $('#log_ol').empty();
        line_array.forEach(function(e){
            var a = $('#filter').val();
            if (e.match(a) != null)
            {
                e = e.replace(a, '<span style="color:red">' + a + '</span>');
                $('#log_ol').append('<li>' + e + '</li>');
            }
            $('#log_ol')[0].scrollTop = $('#log_ol')[0].scrollHeight;
        })
    });

    $('#log_ol').scrollTop($('#log_ol')[0].scrollHeight);

    $('#scroll').click(function() {
        var a = $('#scroll').val();
        if (a == "Stop scroll")
            {
            $('#scroll').val("Start scroll");
            }
        else
            {
            $('#scroll').val("Stop scroll");
            }
    })

    $("#ip").change(function(){
        $.post(
            "/get_dir_list",
            {ip: $('#ip').val()},

            function(data, status){
                $("#dir").empty();
                $('#dir').append('<option selected disabled>Choose DIR</option>');
                var dirs = data.split(' ');
                dirs.forEach(function(e){
                    $('#dir').append('<option value =' + e + '>' + e +'</option>');
                })
            }
        );
    });
    $("#dir").change(function(){
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
