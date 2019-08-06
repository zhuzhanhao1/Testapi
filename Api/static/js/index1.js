<!--按钮点击后改变按钮的显示状态-->
$(function() {
    $("button.layui-btn.layui-btn-warm.layui-btn-radius").click(function(){
        $(this).button('loading').delay(1000).queue(function() {
        });
    });
});
<!--新建用例完成后的提示框-->
function Ccase(){
    var showres = document.getElementById("myAlert");
    showres.style.display = "block";
};
function go_delete (obj) {
    // {#var id = document.getElementById("delbut").innerText;#}
    // {#console.log(id);#}
    var tr=$(obj).parent().parent();
    var uucaseid = tr.children("td#ucaseid").text();
    $('#show7').val(uucaseid);
    console.log(uucaseid);
    $.ajax({
            cache: false,
            url: "/delete_case/",
            dataType: 'text',
            type: 'POST',
            async: false,
            data: {
                "caseid":uucaseid
            },
            success: function (data) {
                alert('删除成功');
                window.location.reload()
            },
            error:function (data) {
                console.log(data);
                alert('删除失败')
            }
        })
};
