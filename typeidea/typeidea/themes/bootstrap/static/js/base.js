// $(function (){ var divW=$("div").width(); var divH = $("div").height();divW=divH;})
function show_reply_form(this_button,comment_id, reply_id, reply_type, to_name) {
        $('.reply_form').hide();
        $('.reply_form_form').empty();
        const form_div = $(this_button).parent('div').parent('div').parent('div').next('.reply_form');
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

$(document).ready(function(){
  // $("button").click(function(){
  //   $("#test").hide();
  // });
  //   const img_width = $('.user_image').width();
  //   $('.user_image').height(img_width);
    function show_reply_form(v1) {
        alert(v1);
    }

});