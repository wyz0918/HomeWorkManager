
//课程

//创建课程
function create_course(){

    course_name = $(".form-control").val();

    $.ajax({
        url : "/create_course",
        async : true,
        type : "POST",
        data : {"course_name" : course_name},

        dataType : "json",
        success : function(data){

        if(data){
            $(".reminder").show();
            $(".reminder").text("SUCCESS: 创建成功! 该课程的邀请码为 "+data);
            $(".summit").hide();
            $("#my_course").append('<li><a href="t_class_section?'+'course_id='+data+'"'+'class="secondmenu ">'+course_name+'</a></li>');



        }},
        error:function(data,type, err){
	         console.log("ajax错误类型："+type);
	         console.log(err);
	    }
})
}

//关闭提示
function close_tips(){


    $(".reminder").hide();
    $(".reminder").text("");
    $(".summit").show();


}



