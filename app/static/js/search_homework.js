//作业
//创建课程
function search_homework(homework_id) {

    $.ajax({
        url: "/search_homework",
        async: true,
        type: "POST",
        data: {"homework_id": homework_id},

        dataType: "json",
        success: function (data) {

            if (data) {
                s = '';
                for (i in data.homework_info) {


                    s += '<tr data-toggle="modal" data-target="#myModal2" onclick = "fill_form()"><td class = "student_id">' + data.homework_info[i].student_id + '</td><td>' +
                        data.homework_info[i].user_name + '</td><td>' +
                        data.homework_info[i].complete_time + '</td><td><button type="button" class="btn btn-default btn-xs" onclick="window.open(\'' + data.homework_info[i].attach + '\')"><span class=" glyphicon glyphicon-download-alt" aria-hidden="true"></span>下载附件</button></td><td class="score">' +
                        data.homework_info[i].score + '</td><td class="comment">' +
                        data.homework_info[i].comment + '</td></tr>';

                }
                $(".homework_info").html(s);
            }
        },
        error: function (data, type, err) {
            console.log("ajax错误类型：" + type);
            console.log(err);
        }
    })
}




