function create_course(){

    course_name = $(".form-control").val();

    $.ajax({
        url : "/create_course",
        async : true,
        type : "POST",
        data : {
            "course_name" : course_name},

        dataType : "json",
        success : function(data){

        if(data){
            $(".reminder").show();
            $(".reminder").text("SUCCESS: 创建成功! 该课程的邀请码为 "+data);
            $(".summit").hide();

        }},
        error:function(data,type, err){
	         console.log("ajax错误类型："+type);
	         console.log(err);
	    }
})
}

function close_tips(){


    $(".reminder").hide();
    $(".reminder").text("");
    $(".summit").show();


}