// 这是返回顶部标签的js
$(document).ready(function () {
    // 设置轮播图高是宽的一半
    var carosel_cont_height = $('#sticky_posts_carousel_container').width();
    $('.carousel-inner').height(carosel_cont_height * 0.4);
    $(window).resize(function () {
        $('.carousel-inner').height(carosel_cont_height * 0.4);
    });
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
    // 导航条显示和隐藏
    var nav_height = $('.navbar').outerHeight();  // 导航条的高度
    var nav_width = $('.navbar').outerWidth();  // 导航条的宽度
    var nav_top = $('.navbar').offset().top;  // 导航条到窗口的高度
    var nav_to_top_height = nav_height + nav_top;  // 导航条底部到窗口顶部的高度
    var scrollBefore = $(window).scrollTop();  // 滚动前的滑动条距离
    var down_or_up = 0;  // 记录滑动条的方向, 避免大量的js操作
    //固定布局
    $('#navbar_back').css({
        'height': nav_height,
        'width': nav_width,
    });
    $('.navbar').css({
        'position': 'fixed',
        'z-index': 9999,
        'left': 0,
        'top': 0,
        'width': '100%',
    });


    $(window).scroll(function () {
        //创建一个变量存储当前窗口下移的高度
        var doc_height = $(document).height();
        var scroTop = $(window).scrollTop();
        var s_height = scroTop + window_height;  //获取滚动条滚动距离+窗口高度
        //判断当前窗口滚动高度
        //如果大于设置值，则显示顶部元素，否则隐藏顶部元素
        // if (scroTop > w_height) {
        //     $('.little_tools').show();
        // } else {
        //     $('.little_tools').hide();
        // }

        // 侧边栏 如果侧边栏的滑到了底部 设置为绝对定位 不让其再滑动
        // 如果窗口滑动距离大于侧边栏距离窗口顶部高度(前提是右侧内容区高于左侧侧边栏)

        if (content_height > side_height) {
            if (s_height > (side_height + 120)) {
                $('.sidebar-left').addClass('sidebar-left-to-bottom');
                $('.sidebar-left-to-bottom').css({
                    'left': side_left,
                    'width': side_width,
                    'bottom': 120,

                })
            } else {
                $('.sidebar-left-to-bottom').css({
                    'left': '',
                    'width': '',
                    'bottom': '',
                });
                $('.sidebar-left').removeClass('sidebar-left-to-bottom')
            }
        }

        // 导航栏的显示和隐藏
        let scrollAfter = $(window).scrollTop();
        // 向下滑动时
        if (scrollBefore < scrollAfter) {
            //如果向下滑动距离超过了导航栏下边框位置
            if (scrollAfter > nav_to_top_height && down_or_up < 1) {
                //导航栏隐藏
                // console.log('导航条隐藏');
                // alert([scrollBefore,scrollAfter]);
                down_or_up = 1;  // 向下滑动状态设置为1
                $('.navbar').slideUp(300);
            }
            // 如果下滑动距离没有超过导航栏边框的位置
            if (scrollAfter <= nav_to_top_height) {
                // 导航栏透明
                // console.log('导航条透明');
                $('.navbar').css({'opacity': 0.9});
            }
        }else if (scrollBefore > scrollAfter) {

            // 如果滚动条距离大于导航栏高度
            if (scrollAfter > nav_to_top_height && down_or_up > -1) {
                // 导航条显示
                // console.log('导航条显示');
                // alert('show');
                // alert([scrollBefore,scrollAfter]);
                down_or_up = -1;  // 向上滑动状态设置为-1
                $('.navbar').slideDown(300);
            }
            //如果滚动条距离小于导航栏高度
            if (scrollAfter < nav_to_top_height) {
                //导航栏不透明
                // console.log('导航条不透明');
                $('.navbar').css({'opacity': 1});
            }
        }
        scrollBefore = scrollAfter  // 重定义起始位置
        // 向上滑动时
        // if (scrollBefore > scrollAfter) {
        //     // 如果滚动条距离大于导航栏高度
        //     if (scrollAfter > nav_to_top_height && down_or_up > -1) {
        //         // 导航条显示
        //         // console.log('导航条显示');
        //         down_or_up = -1;  // 向上滑动状态设置为-1
        //         $('.navbar').slideDown(300);
        //         return false;
        //     }
        //     //如果滚动条距离小于导航栏高度
        //     if (scrollAfter < nav_to_top_height) {
        //         //导航栏不透明
        //         // console.log('导航条不透明');
        //         $('.navbar').css({'opacity': 1});
        //     }
        // }

    });



    //为返回顶部元素添加点击事件
    $('.return_top').click(function () {
        //将当前窗口的内容区滚动高度改为0，即顶部
        $("html,body").animate({scrollTop: 1111}, "normal");
    });

    $('#return_top').click(function () {
        //将当前窗口的内容区滚动高度改为0，即顶部

        $("html,body").animate({scrollTop: 0}, "slow");
    });

    $('#return_bottom').click(function () {
        let s_h = $(document).height()-$(window).height();
        // alert([a, $(document).height(),$(window).height()]);
        $("html,body").animate({scrollTop: s_h}, "slow");
    });

    $('#contact_me').click(function () {
        $('#qrcode_img, #post_catalog').hide();
        $('#contact_me_img').toggle('fast')
    })
    // 显示联系我的微信二维码
    // $('#contact_me').hover(function () {
    //     // $('#contact_me_img').show('fast')
    // },function () {
    //     $('#contact_me_img').hide('fast')
    // });

     // 显示分享页面的二位码
    $('#share').click(function () {
        $('#contact_me_img, #post_catalog').hide();
        $('#qrcode_img').toggle('fast')
    });

    // $('#share').hover(function () {
    //     // $('#contact_me_img').show('fast')
    // },function () {
    //     $('#qrcode_img').hide('fast')
    // });






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

