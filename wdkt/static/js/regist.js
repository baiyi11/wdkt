function bindCaptchaBtnClick() {
    $("#captcha-btn").click(function () {
        var $this=$(this);
        var email = $("input[name='email']").val();
        if (!email) {
            alert("请先输入邮箱");
            return;
        }
        // 异步获取验证码
        $.ajax({
            url: "/user/emailCaptcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res) {
                var code = res['code']
                if (code === 200) {
                    //获取验证码成功后取消button点击事件
                    $this.off("click");
                    //开始倒计时
                    var countDown=60;
                    var timer=setInterval(function(){
                        countDown -= 1;

                        if (countDown>0){
                            $this.text(countDown+"秒后重新发送");
                        }else{
                            //倒计时完毕
                            $this.text("获取验证码");
                            //重新绑定点击事件
                            bindCaptchaBtnClick();
                            //清除倒计时
                            clearInterval(timer);
                        }
                       
                    },1000)
                    alert("验证码发送成功");
                } else {
                    alert(res['message']);
                }

            }
        })
    });

}


// 等待网页文档所有元素都加载完成后再执行
$(function () {
    bindCaptchaBtnClick();
});