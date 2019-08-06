$(function(){
    //为#aa绑定
    $('#aa').blur(function(){
        $.ajax({
            url:'/uphone_blur/',
            type:'get',
            data:'uphone=' + $(this).val(),
            dataType:'html',
            success:function(data){
                $('#pp').html(data)
            }

        })
    });
});