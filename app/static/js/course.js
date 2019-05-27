function tablestudent(tableid,pageid,data,name,size){
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
        var rate;
        if(parseInt(homework_num)==0)
            rate=1;
        else
            rate=parseInt(dataitem.commit_num)/parseInt(homework_num);
        var s="<tr><td>"+dataitem.id+"</td><td>"+
        dataitem.username+"</td><td>"+homework_num+
        "</td><td>"+dataitem.commit_num+"</td><td>"+parseInt(rate*100)+"%</td></tr>";
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
function tablehomework(tableid,pageid,data,name,size){
	tablestudent.call(this,tableid,pageid,data,name,size);
	this.getItem=function(dataitem){
		var s="<tr><td>"+dataitem.batch+"</td><td>"+
        dataitem.start_time+"</td><td>"+dataitem.end_time+
        "</td><td>"+(student_num-dataitem.upload_num)+"</td><td>"+
        dataitem.upload_num+"</td><td><a href=\"javascript:void(0)\" onClick=\"view_homework('"+dataitem.id+"')\">";
        if(dataitem.completion)
            s+="已完成</a></td></tr>";
        else
            s+="未完成</a></td></tr>";
        return s;
	}
}
function view_homework(id){
    $("#change_img").text("修改");
    $('#browsetreaminput').val("");
    $("#send_img").attr("disabled",true);
    d={work_id:id}
    $("#work_id").text(id);
    $.ajax({
            type:"post",
            dataType:"json",
            url:"/get_homework",
            contentType: 'application/json',
            data:JSON.stringify(d),
            success:function(data){
                $("#dialoglable").text('第'+data.homework.batch+'次作业');
                $("#question_text").text(data.homework.homework_describe);
                if(data.homework.attach){
                    var t_f=data.homework.attach.split('.')[1];
                    if(t_f=='jpeg'||t_f=='jpg'||t_f=='png'||t_f=='gif')
                        $("#question_img").html("<img src=\"_uploads/files/"+data.homework.attach+"\" alt=\"通用的占位符缩略图\" style=\"width:600px\">");
                    else
                        $("#question_img").html("<a class=\"btn btn-default\" href='/pics/"+data.homework.attach+"'download='"+data.homework.attach+"'><span class='glyphicon glyphicon-arrow-down'></span>下载附件</a>");
                }
                else
                    $("#question_img").html('');
                if(data.completion!=null){
                    $("#change_img").show();
                    $("#select_img").hide();
                    $("#download_img").html("<a class=\"btn btn-default\" href='/homeworks/"+data.completion.address+"'download='"+data.completion.address+"'><span class='glyphicon glyphicon-arrow-down'></span>下载附件</a>");
                    var d_f=data.completion.address.split('.')[1];
                    if(d_f=='jpeg'||d_f=='jpg'||d_f=='png'||d_f=='gif')
                        $("#answer_img").html("<img src=\"/homeworks/"+data.completion.address+"\" alt=\"通用的占位符缩略图\" style=\"width:600px\">");
                    else
                        $("#answer_img").html("");
                    if(data.completion.score!=null)
                        $("#score_text").text(data.completion.score+"分");
                    if(data.completion.comment!=null)
                        $("#comment_text").text(data.completion.comment);
                }
                else{
                    $("#score_text").text('暂无！');
                    $("#comment_text").text('暂无！');
                    $("#select_img").show();
                    $("#answer_img").html("");
                    $("#download_img").html("");
                    $("#change_img").hide();
                }
                $("#homeworkModal").modal('show');
            }
        });
}
$(document).ready(function(){
    var file;
    var font;
    if(student_list.length==0)
        $("#student_list").html("<p class=\"h3\"style=\"margin:30px\">暂无学生!</p>");
    else{
        ts=new tablestudent("#student_text","#itempage1",student_list,"ts",10);
        ts.divpage();
    }
    if(homework_list.length==0)
        $("#homework_list").html("<p class=\"h3\"style=\"margin:30px\">暂无作业!</p>");
    else{
         th=new tablehomework("#homeword_text","#itempage2",homework_list,"th",10);
         th.divpage();
    }
    if(type=="1"){
        $("#s_l").addClass("active");
        $("#student_list").addClass("active");
    }
    else{
        $("#h_l").addClass("active");
        $("#homework_list").addClass("active");
    }
    $("#file_select").click(function(){
        $("#treamitemFile").click();
    });
    $('#treamitemFile').change(function () {
        $('#browsetreaminput').val($(this).val());
        var filepath=$(this).val();
        if(filepath==''){
            $("#send_img").attr("disabled",true);
            $("#answer_img").html("");
        }
        else{
            var spls=filepath.split('.');
            file=this.files[0];
            font=spls[spls.length-1];
            if(font=='jpeg'||font=='jpg'||font=='png'||font=='gif'){
                $("#answer_img").html("<img id=\"imags\" src=\"\" alt=\"通用的占位符缩略图\" style=\"width:600px\">");
                $("#imags").attr("src",window.URL.createObjectURL(file));
            }
            $("#send_img").removeAttr("disabled");
        }
    });
    $("#send_img").click(function(){
        var reader=new FileReader();
        var imgFile;
        reader.onload=function(e){
            imgFile=e.target.result;
             var d={work_id:$("#work_id").text(),
             img:imgFile,
             font:font}
            $.ajax({
                type:"post",
                dataType:"json",
                url:"/summit_homework",
                contentType: 'application/json',
                data:JSON.stringify(d),
                success:function(data){
                    if(data.code=='100'){
                        $("#homeworkModal").modal("hide");
                        $("#dialogtext").text("提交成功")
                        $("#myModal").modal("show");
                        setTimeout(function(){location.reload();},1500);
                    }else{
                        $("#homeworkModal").modal("hide");
                        $("#dialogtext").text("提交失败")
                        $("#myModal").modal("show");
                    }
                }
            });
        }
        reader.readAsDataURL(file);
    });
    $("#change_img").click(function(){
        if($("#change_img").text()=="修改"){
            $("#change_img").text("取消")
            $("#answer_img").html("");
            $("#download_img").html("");
            $("#select_img").show();
        }
        else{
            $("#change_img").text("修改");
            $("#homeworkModal").modal("hide");
        }
    });
});
