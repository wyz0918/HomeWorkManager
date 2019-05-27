
//课程

//创建课程
function fill_form(){

    $(".input_score").val($(".score").text());
    $(".input_comment").val($(".comment").text());

}

function score_comment(){

    score = $(".input_score").val();
    comment = $(".input_comment").val();
    student_id = $(".student_id").text();
    homework_id = $("#hiding").text();


    $.ajax({
        url : "/score_comment",
        async : true,
        type : "POST",
        data : {"score" : score,
                "comment" : comment,
                "student_id" : student_id,
                "homework_id" : homework_id,
                },

        dataType : "json",
        success : function(data){

        if(data){
            $(".reminder").show();
            $(".reminder").text("SUCCESS: "+data);
            $(".summit").hide();
            $(".score").text(score);
            $(".comment").text(comment);


         }

        },
        error:function(data,type, err){
	         console.log("ajax错误类型："+type);
	         console.log(err);
	    }

        })
}

function close_modal(){

    $(".reminder").hide();
    $(".reminder").text("");
    $(".summit").show();
}




