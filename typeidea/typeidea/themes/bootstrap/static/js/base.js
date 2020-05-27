// 这是返回顶部标签的js
$(document).ready(function () {
    //为当前窗口添加滚动条滚动事件（适用于所有可滚动的元素和 window 对象（浏览器窗口））
    var window_height = $(window).height();  // 窗口的高度
    var content_top = $('.content-col').offset().top;  // 右侧内容区距离窗口顶部的距离
    var content_height = $('.content-col').height();  // 右侧内容区高度
    content_height = content_height + content_top;  // 实际需要的高度是内容区底部距离窗口顶部的距离
    var side_height = $('.sidebar-left').height(); // 侧边栏高度
    var side_width = $('.sidebar-left').width();  //侧边栏宽度
    var side_left = $('.sidebar-left').offset().left;  // 侧边栏左边距
    var side_top = $('.sidebar-left').offset().top;   // 侧边栏上边距
    side_height = side_height + side_top;  // 实际需要的高度是侧边栏底部距离窗口的高度
    var w_height = window_height / 2;  //下拉窗口高度的一半就可以显示返回顶部按钮
    $(window).scroll(function () {
        //创建一个变量存储当前窗口下移的高度
        var scroTop = $(window).scrollTop();
        var s_height = scroTop + window_height;  //获取滚动条滚动距离+窗口高度
        //判断当前窗口滚动高度
        //如果大于设置值，则显示顶部元素，否则隐藏顶部元素
        if (scroTop > w_height) {
            $('.return_top').show();
        } else {
            $('.return_top').hide();
        }

        // 侧边栏 如果侧边栏的滑到了底部 设置为绝对定位 不让其再滑动
        // 如果窗口滑动距离大于侧边栏距离窗口顶部高度(前提是右侧内容区高于左侧侧边栏)
        if (content_height > side_height) {
            if (s_height > side_height) {
                $('.sidebar-left').addClass('sidebar-left-to-bottom');
                $('.sidebar-left-to-bottom').css({
                    'left': side_left,
                    'width': side_width

                })
            } else {
                $('.sidebar-left-to-bottom').css({
                    'left': '',
                    'width': '',
                });
                $('.sidebar-left').removeClass('sidebar-left-to-bottom')
            }
        }

    });

    //为返回顶部元素添加点击事件
    $('.return_top').click(function () {
        //将当前窗口的内容区滚动高度改为0，即顶部
        $("html,body").animate({scrollTop: 0}, "normal");
    });
});

// $(function (){ var divW=$("div").width(); var divH = $("div").height();divW=divH;})
function show_reply_form(this_button, comment_id, reply_id, reply_type, to_name) {
    let form_div;
    $('.reply_form').hide();
    $('.reply_form_form').empty();
    if (reply_type == 1) {
        // 1代表回复的对象是一个回复
        form_div = $(this_button).parent('div').parent('div').parent('div').next('.reply_form');
    } else {
        // 0 代表回复的对象是一个评论
        form_div = $(this_button).parent('div').parent('div').next('div').children('.reply_form');
    }
    const rp_form = $('#reply_form_base > .form-group').clone();
    $(rp_form).children('input[name="commentid"]').attr('value', comment_id);
    $(rp_form).children('input[name="reply_id"]').attr('value', reply_id);
    $(rp_form).children('input[name="reply_type"]').attr('value', reply_type);
    $(rp_form).children('input[name="to_name"]').attr('value', to_name);

    $(rp_form).prependTo(form_div.children('.reply_form_form'));
    form_div.show()
}

function cancel_reply() {
    $('.reply_form').hide();
    $('reply_form_form').empty();
}


$(document).ready(function () {
    // $("button").click(function(){
    //   $("#test").hide();
    // });
    //   const img_width = $('.user_image').width();
    //   $('.user_image').height(img_width);
    function show_reply_form(v1) {
        alert(v1);
    }

});
