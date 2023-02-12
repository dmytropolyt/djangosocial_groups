import '../sass/styles.scss';
import 'jquery';


$('#joinLeave').on('click', function() {

    var icon = $('.bi-check-circle');
    console.log(icon.text());
    if (icon.text() == 'Join') {
        var url = `/groups/join/${$(this).attr('data-group-slug')}/`;
        var text = 'Leave';
    } else {
        var url = `/groups/leave/${$(this).attr('data-group-slug')}/`;
        var text = 'Join';
    };
    console.log(url);

    $.ajax({
        type: 'POST',
        url: location.origin + url,
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: (json) => {
            $('#memberCount').html('Member count: ' + json['members_count']);
            icon.html(text);
            icon.toggleClass('bi bi-x-circle');
            console.log('yes');
        },
        error: (error) => {
            console.log(error);
            console.log('no');
        }
    })
});
