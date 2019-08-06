$(function(){
    //为#formReg绑定sumbit时间
    $('#formReg').submit(function(){
        if($('#upwd').val() == $('#upwd1').val()){
            return true;
        }else{
            alert('两次密码不一致，请重试')
            return false;
        };
    });
});