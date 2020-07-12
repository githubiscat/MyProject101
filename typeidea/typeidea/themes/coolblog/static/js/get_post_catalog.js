$(document).ready(function () {
    var catalog_list = [];
    var a_list = $('#post_text_content').children().children('a');
    for (i=0; i<a_list.length; i++){

        let elem_a = a_list[i];
        let a_id = elem_a.id;
        let a_name = elem_a.name;
        if (a_id == a_name && a_id.length > 0){
            catalog_list.push(a_name)
        }
    }
    if (catalog_list.length > 0){
        for (let i=0; i<catalog_list.length; i++){
            let c = catalog_list[i];
            let n = i + 1;
            $('#post_catalog_list>ul').append('<li><a href="'+'#'+c+'">'+c+'</a></li>')
        }
    }else {
        $('#post_catalog_list').text('博主有点懒,这个文章没有目录!')
    }

    $('#catalog').click(function () {
        $('#qrcode_img, #contact_me_img').hide();
        $('#post_catalog').slideToggle(500);
    });

    $('#post_catalog_button').click(function () {
        $('#post_catalog').slideUp(500);
    })


});