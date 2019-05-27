function tablepage(tableid,pageid,data,name,size){
    this.row=size;
    this.currpage=1;
    this.starpage=1;
    this.lastpage=0;
    this.table=tableid;
    this.page=pageid;
    this.data=data;
	this.name=name;
    this.setpage=function(){
        var item=this.currpage-2;
        var ps="<li><a href='javascript:void(0)' onClick=\""+this.name+".gopage("+this.name+".currpage-1)\">&laquo;</a></li>";
        if(this.currpage-3<0)
            item=1;
        for(var i=item;i<=item+7;i++){
            if(i>this.lastpage)
                break;
            else{
                if(i==this.currpage)
                    ps+="<li class=\"active\"><a href='javascript:void(0)' onClick=\""+this.name+".gopage("+i+")\">"+i+"</a></li>";
                else
                    ps+="<li><a href='javascript:void(0)' onClick=\""+this.name+".gopage("+i+")\">"+i+"</a></li>";
            }
        }
		ps+="<li><a href='javascript:void(0)' onClick=\""+this.name+".gopage("+this.name+".currpage+1)\">&raquo;</a></li>"
        $(this.page).html(ps);
    }
    this.getItem=function(dataitem){
        var s="<tr><td>"+dataitem.course_name+"</td><td>"+dataitem.batch+"</td><td>"+
        dataitem.start_time+"</td><td>"+dataitem.end_time+
        "</td><td><a href=\"/course?id="+dataitem.course_id+"&type=2\" target=\"_blank\">提交</a></td></tr>";
        return s;
    }
    this.loaddata=function(){
        var j=(this.currpage-1)*this.row;
        var ts="";
        for(var t=j;t<=j+this.row-1;t++){
            if(t>=this.data.length)
                break;
            else{
                ditem=this.data[t];
                ts+=this.getItem(ditem);
            }
        }
        $(this.table).html(ts);
    }
    this.gopage=function(index){
		if(index<1)
			index=1;
		if(index>this.lastpage)
			index=this.lastpage;
        if(this.currpage==index);
        else{
            this.currpage=index;
            this.setpage();
            this.loaddata();
        }
    }
    this.divpage=function(){
        if(this.data.length==0);
        else{
            this.lastpage=parseInt(this.data.length/this.row);
            if(this.lastpage*this.row!=this.data.length)
                this.lastpage+=1;
            this.setpage();
            this.loaddata();
        }
    }
}
function tablepage1(tableid,pageid,data,name,size){
	tablepage.call(this,tableid,pageid,data,name,size);
	this.getItem=function(dataitem){
		var s="<tr><td>"+dataitem.course_name+"</td><td>"+dataitem.batch+"</td><td>"+
        dataitem.start_time+"</td><td>"+dataitem.end_time+"</td><td>"+
        dataitem.score+"</td><td><a href=\"/course?id="+dataitem.course_id+"&type=2\" target=\"_blank\">查看</a></td></tr>";
        return s;
	}
}
function tablepage2(tableid,pageid,data,name,size){
    tablepage.call(this,tableid,pageid,data,name,size);
    this.getItem=function(dataitem){
        var s="<div class=\"row buildnael\"><div class=\"col-xs-4\"><img src=\"/img/cor.png\" alt=\"通用的占位符缩略图\"style='width:240px'></div>"
        +"<div class=\"col-xs-3\"><div class=\"h3\" style=\"margin-top:30px\">"+dataitem.course_name+"</div><span style='margin-top:20px'>任课教师:"
        +dataitem.creator_name+"</span></div>"
        +"<div class=\"col-xs-5\"><a role=\"button\" href=\"/course?id="+dataitem.id+"&type=1\" target=\"_blank\" class=\"btn btn-primary\"style=\"margin-top: 35px; width: 85px\">进入课程"
        +"</a><br><a role=\"button\" href=\"/course?id="+dataitem.id+"&type=2\" target=\"_blank\" class=\"btn btn-default\"style=\"margin-top:20px;width: 85px;\">查看作业</a></div></div>";
        return s;
    }
}
function tablepage3(tableid,pageid,data,name,size){
     tablepage.call(this,tableid,pageid,data,name,size);
     this.getItem=function(dataitem){
        var s="<div class=\"row buildnael\"><div class=\"col-xs-4\"><img src=\"/img/cor.png\" alt=\"通用的占位符缩略图\"style='width:240px'></div>"
        +"<div class=\"col-xs-3\"><div class=\"h3\" style=\"margin-top:30px\">"+dataitem.course_name+"</div><span style='margin-top:20px'>任课教师:"
        +dataitem.creator_name+"</span></div>";
        if(!dataitem.in_out)
            s+="<div class=\"col-xs-5\"><a role=\"button\" href='javascript:void(0)'onClick=\"openinput('"+dataitem.id+"')\" class=\"btn btn-primary\"style=\"margin-top: 50px; width: 85px\">申请加入</a><br></div></div>";
        else
            s+="<div class=\"col-xs-5\"><a role=\"button\" href='course?id="+dataitem.id+"&type=1'target=\"_blank\" class=\"btn btn-primary\"style=\"margin-top: 50px; width: 85px\">已加入</a><br></div></div>";
        return s;
    }
}
function openinput(id){
    $("#myModalinput").modal('show');
    $("#varitify").val("");
    $("#varitify").attr("placeholder","");
    $("#id_text").text(id);
}
function infotable(data){
    this.infodata=data;
    this.currp=1;
    this.lastp=1;
    this.loadd=function(){
        var s="";
        for(var j=(this.currp-1)*4;j<(this.currp)*4;j++){
            if(j>=this.infodata.length)
                break;
            else{
            s+="<tr><td>"+this.infodata[j].time+" "+this.infodata[j].msg+"</td></tr>";
            }
        }
        $("#infotable").html(s);
    }
    this.divp=function(){
        if(this.infodata.length==0){
        }
        else{
            this.lastp=parseInt(this.infodata.length/4);
            if(this.lastp*4!=this.infodata.length)
                this.lastp+=1;
            this.loadd();
        }
    }
    this.gop=function(index){
		if(index<1)
			index=1;
		if(index>this.lastp)
			index=this.lastp;
        if(this.currp==index);
        else{
            this.currp=index;
            this.loadd();
        }
    }
}
function sendvar(){
    if($("#varitify").val()==''){
        $("#varitify").attr("placeholder","请输入验证码");
    }
    else{
        d={course_id:$("#id_text").text(),
            varitify:$("#varitify").val()}
        $.ajax({
            type:"post",
            dataType:"json",
            url:"/add_course",
            contentType: 'application/json',
            data:JSON.stringify(d),
            success:function(data){
                if(data.code=='100'){
                    $("#myModalinput").modal('hide');
                    $("#dialogtext").text("加入成功");
                    $("#myModal").modal("show");
                    setTimeout(function(){location.reload();},1500);
                }
                else{
                     $("#myModalinput").modal('hide');
                     $("#dialogtext").text("加入失败，验证码错误");
                     $("#myModal").modal("show");
                }
            }
        });
    }
}
$(document).ready(function(){
    if(unfinishworks.length==0)
        $("#unfinish").html("<p class=\"h3\"style=\"margin:30px\">无未完成作业!</p>");
    else{
        tp=new tablepage("#unfinishworks","#itempage1",unfinishworks,"tp",8);
        tp.divpage();
    }
    if(finishworks.length==0)
        $("#finish").html("<p class=\"h3\"style=\"margin:30px\">无已提交作业!</p>");
    else{
        ts=new tablepage1("#finishworks","#itempage2",finishworks,"ts",8);
        ts.divpage();
    }
    if(my_class.length==0)
        $("#class_msg").html("<p class=\"h2\" style=\"margin:50px\">您还没有加入任何课程！</p>");
    else{
         tc=new tablepage2("#my_class_list","#itempage3",my_class,"tc",4);
         tc.divpage();
    }

    if(info==null)
        $("#infomsg").text("暂无通知!");
    else{
        itf=new infotable(info);
        itf.divp();
    }
    $("#mchange").click(function(){
        if($("#mchange").text()=="修 改"){
            $("#mchange").text("取 消");
            $("#mybirth").removeAttr("readOnly");
            $("#mygrade").removeAttr("readOnly");
            $("#myschool").removeAttr("readOnly");
            $("#mycollage").removeAttr("readOnly");
            $("#mymajor").removeAttr("readOnly");
            $("#msubmit").removeAttr("disabled");
        }else{
            $("#mchange").text("修 改");
            $("#myname").val(user.username);
            $("#mybirth").val(additional_info.birthday);
            $("#mygrade").val(additional_info.enrollment_year);
            $("#myschool").val(additional_info.university);
            $("#mycollage").val(additional_info.college);
            $("#mymajor").val(additional_info.major);
            $("#mybirth").attr("readOnly",true);
            $("#mygrade").attr("readOnly",true);
            $("#myschool").attr("readOnly",true);
            $("#mycollage").attr("readOnly",true);
            $("#mymajor").attr("readOnly",true);
            $("#msubmit").attr("disabled",true);
        }
    });
    $("#msubmit").click(function(){
        var d={
            id:user.id,
            university:$("#myschool").val(),
            college:$("#mycollage").val(),
            major:$("#mymajor").val(),
            username:$("#myname").val(),
            birthday:$("#mybirth").val(),
            enrollment_year:$("#mygrade").val(),
        };
        $.ajax({
            type:"post",
            dataType:"json",
            url:"/changemsg",
            contentType: 'application/json',
            data:JSON.stringify(d),
            success:function(data){
                user=data.user;
                additional_info=data.student_additional_info;
                if(data.code=="101"){
                    $("#dialogtext").text("修改失败");
                    $("#myModal").modal("show");
                }
                else{
                    $("#dialogtext").text("修改成功");
                    $("#myModal").modal("show");
                    $("#mchange").text("修 改");
                    $("#myname").val(user.username);
                    $("#mybirth").val(additional_info.birthday);
                    $("#mygrade").val(additional_info.enrollment_year);
                    $("#myschool").val(additional_info.university);
                    $("#mycollage").val(additional_info.college);
                    $("#mymajor").val(additional_info.major);
                    $("#mybirth").attr("readOnly",true);
                    $("#mygrade").attr("readOnly",true);
                    $("#myschool").attr("readOnly",true);
                    $("#mycollage").attr("readOnly",true);
                    $("#mymajor").attr("readOnly",true);
                    $("#msubmit").attr("disabled",true);
                }
            }
        });
    });
    $("#cpchange").click(function(){
        if($("#cpchange").text()=="修 改"){
            $("#cpchange").text("取 消");
            $("#old_password").removeAttr("readOnly");
            $("#new_password").removeAttr("readOnly");
            $("#new_password1").removeAttr("readOnly");
            $("#cpsubmit").removeAttr("disabled");
         }else{
            $("#cpchange").text("修 改");
            $("#old_password").val("");
            $("#new_password").val("");
            $("#new_password1").val("");
            $("#old_password").attr("readOnly",true);
            $("#new_password").attr("readOnly",true);
            $("#new_password1").attr("readOnly",true);
            $("#cpsubmit").attr("disabled",true);
         }
    });
    $("#cpsubmit").click(function(){
        var op=$("#old_password");
        var np=$("#new_password");
        var np1=$("#new_password1");
        if(op.val()==""||np.val()==""||np1.val()==""){
             $("#dialogtext").text("请将信息填写完整");
             $("#myModal").modal("show");
        }
        else if(np.val()!=np1.val()){
            $("#dialogtext").text("密码确认失败");
            $("#myModal").modal("show");
        }
        else{
            var d={
            oldpassword:$("#old_password").val(),
            newpassword:$("#new_password").val(),
            };
            $.ajax({
            type:"post",
            dataType:"json",
            url:"/changepw",
            contentType: 'application/json',
            data:JSON.stringify(d),
            success:function(data){
                if(data.code=="101"){
                    $("#dialogtext").text("修改失败");
                    $("#myModal").modal("show");
                }else{
                    $("#dialogtext").text("修改成功");
                    $("#myModal").modal("show");
                    $("#cpchange").text("修 改");
                    $("#old_password").val("");
                    $("#new_password").val("");
                    $("#new_password1").val("");
                    $("#old_password").attr("readOnly",true);
                    $("#new_password").attr("readOnly",true);
                    $("#new_password1").attr("readOnly",true);
                    $("#cpsubmit").attr("disabled",true);
                    setTimeout(function(){location.reload();},1500);
                }
               }
            });
        }
    });
    $("#first_menu").click(function(){
        $("#collapseTwo").removeClass("in");
        $("#collapseTwo").addClass("out");
        $("#collapseThree").removeClass("in");
        $("#collapseThree").addClass("out");
        if($("#my_class").hasClass("active"))
            $("#m1_my_class").addClass("active");
        else if($("#search_class").hasClass("active"))
            $("#m1_search_class").addClass("active");
        else{
             $("#m1_my_class").removeClass("active");
              $("#m1_search_class").removeClass("active");
        }
    });
    $("#second_menu").click(function(){
        $("#collapseOne").removeClass("in");
        $("#collapseOne").addClass("out");
        $("#collapseThree").removeClass("in");
        $("#collapseThree").addClass("out");
        if($("#my_homework").hasClass("active"))
            $("#m2_my_work").addClass("active");
        else{
             $("#m2_my_work").removeClass("active");
         }
    });
    $("#third_menu").click(function(){
        $("#collapseTwo").removeClass("in");
        $("#collapseTwo").addClass("out");
        $("#collapseOne").removeClass("in");
        $("#collapseOne").addClass("out");
        if($("#mymessage").hasClass("active"))
            $("#m3_my_msg").addClass("active");
        else if($("#changepw").hasClass("active"))
             $("#m3_change_pw").addClass("active");
        else{
             $("#m3_my_msg").removeClass("active");
             $("#m3_change_pw").removeClass("active");
        }
    });
    $("#search_course").click(function(){
        var text=$("#search").val();
        if(text==""){
            $("#dialogtext").text("请输入内容再搜索");
            $("#myModal").modal("show");
        }
        else{
            var d={search_text:text};
            $.ajax({
                type:"post",
                dataType:"json",
                url:"/searchcourse",
                contentType: 'application/json',
                data:JSON.stringify(d),
                success:function(data){
                    if(data.course==null)
                        $("#search_class_list").html("<p class=\"h2\" style=\"margin:50px\">未找到班级！</p>");
                    else{
                        var tab1=new tablepage3("#search_class_list","#itempage4",data.course,"tab1",4);
                        tab1.divpage();
                    }
                }
            });
        }
    });
});