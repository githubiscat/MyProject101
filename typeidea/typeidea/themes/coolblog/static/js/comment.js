$(document).ready(function () {
    // 获取短信验证码
    $('.get_active_code_button').click(function () {
        let phone_num = $(this).parents('.form-row').find('input').get(0).value;
        if (phone_num.length == 11 && phone_num[0] == 1) {
            settime($(this));
            $.ajax({
                url: '/get_active_code/',
                type: 'GET',
                data: {'phone_num': phone_num},
                timeout: 5000,
                dataType: 'json',
                success: function (result) {
                    let return_code = result['code'];
                    if (return_code == 0) {
                        // 0 代表发送成功
                        $('#site_tip').attr('class', '').addClass('site_tip_success');
                        $('#site_tip_color_bar').attr('class', '').addClass('site_tip_color_bar_success');
                        $('#site_tip_icon').attr('class', '').addClass('site_tip_icon_success');
                        $('#site_tip_icon').html('<svg class="bi bi-check-circle-fill" width="35px" style="margin-bottom: 4px" height="35px"\n' +
                            'viewBox="0 0 16 16" fill="currentColor"\n' +
                            'xmlns="http://www.w3.org/2000/svg">\n' +
                            '<path fill-rule="evenodd"\n' +
                            'd="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>\n' +
                            '</svg>');
                        $('#side_tip_title_1').html('发送成功！');
                        $('#side_tip_title_2').html('验证码当日有效，请注意查收！');
                        $('#site_tip').fadeIn('fast');
                        // 3秒后消失
                        setTimeout(function () {
                            $('#site_tip').fadeOut(1000);
                        }, 2000)

                    } else if (return_code == 1 || return_code == 2) {
                        // 1 代表IP超过次数 失败
                        // 2 代表手机号超过次数 失败
                        $('#site_tip').attr('class', '').addClass('site_tip_error');
                        $('#site_tip_color_bar').attr('class', '').addClass('site_tip_color_bar_error');
                        $('#site_tip_icon').attr('class', '').addClass('site_tip_icon_error');
                        $('#site_tip_icon').html('<svg class="bi bi-x-circle-fill" width="35px"\n' +
                            'style="margin-bottom: 4px" height="35px"\n' +
                            'viewBox="0 0 16 16" fill="currentColor"\n' +
                            'xmlns="http://www.w3.org/2000/svg">\n' +
                            '<path fill-rule="evenodd"\n' +
                            'd="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>\n' +
                            '</svg>');
                        $('#side_tip_title_1').html('获取验证码失败！');
                        $('#side_tip_title_2').html('请使用最后一次的验证码！当日有效！');
                        $('#site_tip').fadeIn('fast');
                        // 3秒后消失
                        setTimeout(function () {
                            $('#site_tip').fadeOut(1000);
                        }, 2000)
                    } else if (return_code == 3) {
                        // 3 代表验证码短信发送失败
                        $('#site_tip').attr('class', '').addClass('site_tip_error');
                        $('#site_tip_color_bar').attr('class', '').addClass('site_tip_color_bar_error');
                        $('#site_tip_icon').attr('class', '').addClass('site_tip_icon_error');
                        $('#site_tip_icon').html('<svg class="bi bi-x-circle-fill" width="35px"\n' +
                            'style="margin-bottom: 4px" height="35px"\n' +
                            'viewBox="0 0 16 16" fill="currentColor"\n' +
                            'xmlns="http://www.w3.org/2000/svg">\n' +
                            '<path fill-rule="evenodd"\n' +
                            'd="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>\n' +
                            '</svg>');
                        $('#side_tip_title_1').html('获取验证码失败！');
                        $('#side_tip_title_2').html('很抱歉！ 短信系统发送失败！');
                        $('#site_tip').fadeIn('fast');
                        // 3秒后消失
                        setTimeout(function () {
                            $('#site_tip').fadeOut(1000);
                        }, 2000)
                    } else if (return_code == 4) {
                        // 4 代表用户守家号不合法 警告
                        $('#site_tip').attr('class', '').addClass('site_tip_warning');
                        $('#site_tip_color_bar').attr('class', '').addClass('site_tip_color_bar_warning');
                        $('#site_tip_icon').attr('class', '').addClass('site_tip_icon_warning');
                        $('#site_tip_icon').html('<svg class="bi bi-exclamation-circle-fill" width="35px"\n' +
                            'style="margin-bottom: 4px" height="35px"\n' +
                            'viewBox="0 0 16 16" fill="currentColor"\n' +
                            'xmlns="http://www.w3.org/2000/svg">\n' +
                            '<path fill-rule="evenodd"\n' +
                            'd="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>\n' +
                            '</svg>');
                        $('#side_tip_title_1').html('手机号格式不正确！');
                        $('#side_tip_title_2').html('请使用正确的11位中国大陆手机号码！');
                        $('#site_tip').fadeIn('fast');
                        // 3秒后消失
                        setTimeout(function () {
                            $('#site_tip').fadeOut(1000);
                        }, 2000)
                    }
                },
                error: function () {
                    $('#site_tip').attr('class', '').addClass('site_tip_error');
                    $('#site_tip_color_bar').attr('class', '').addClass('site_tip_color_bar_error');
                    $('#site_tip_icon').attr('class', '').addClass('site_tip_icon_error');
                    $('#site_tip_icon').html('<svg class="bi bi-x-circle-fill" width="35px"\n' +
                        'style="margin-bottom: 4px" height="35px"\n' +
                        'viewBox="0 0 16 16" fill="currentColor"\n' +
                        'xmlns="http://www.w3.org/2000/svg">\n' +
                        '<path fill-rule="evenodd"\n' +
                        'd="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-4.146-3.146a.5.5 0 0 0-.708-.708L8 7.293 4.854 4.146a.5.5 0 1 0-.708.708L7.293 8l-3.147 3.146a.5.5 0 0 0 .708.708L8 8.707l3.146 3.147a.5.5 0 0 0 .708-.708L8.707 8l3.147-3.146z"/>\n' +
                        '</svg>');
                    $('#side_tip_title_1').html('获取验证码失败！');
                    $('#side_tip_title_2').html('很抱歉！ 短信系统连接失败！');
                    $('#site_tip').fadeIn('fast');
                    // 3秒后消失
                    setTimeout(function () {
                        $('#site_tip').fadeOut(1000);
                    }, 2000)
                }
            })

        } else {
            $('#site_tip').attr('class', '').addClass('site_tip_warning');
            $('#site_tip_color_bar').attr('class', '').addClass('site_tip_color_bar_warning');
            $('#site_tip_icon').attr('class', '').addClass('site_tip_icon_warning');
            $('#site_tip_icon').html('<svg class="bi bi-exclamation-circle-fill" width="35px"\n' +
                'style="margin-bottom: 4px" height="35px"\n' +
                'viewBox="0 0 16 16" fill="currentColor"\n' +
                'xmlns="http://www.w3.org/2000/svg">\n' +
                '<path fill-rule="evenodd"\n' +
                'd="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>\n' +
                '</svg>');
            $('#side_tip_title_1').html('手机号格式不正确！');
            $('#side_tip_title_2').html('请使用正确的11位中国大陆手机号码！');
            $('#site_tip').fadeIn('fast');
            // 3秒后消失
            setTimeout(function () {
                $('#site_tip').fadeOut(1000);
            }, 2000)
        }

    });

    // 短信验证码刷新时间
    var countdown = 60;

    function settime(obj) { //发送验证码倒计时
        if (countdown == 0) {
            obj.attr('disabled', false);
            obj.html("获取验证码");
            countdown = 60;
            return;
        } else {
            obj.attr('disabled', true);
            obj.html("重新发送(" + countdown + ")");
            countdown--;
        }
        setTimeout(function () {
                settime(obj)
            }
            , 1000)
    }
});