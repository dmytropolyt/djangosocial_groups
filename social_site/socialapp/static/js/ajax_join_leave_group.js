$('#joinGroup').on('click', function() {
    $.ajax({
        type: 'POST',
        url: `groups/join/${$(this).data('group-slug')}/`,
        dataType: 'json',
        data:
        success: (data) => {
            $('#memberCount').innerHTML = 'Member count: ' + json['members_count'];
            console.log('yes');
        },
        error: (error) => {
            console.log(error);
            console.log('no');
        }
    })
});

$('#leaveGroup').on('click', function() {
    $.ajax({
        type: 'POST',
        url: `groups/leave/${$(this).data('group-slug')}/`,
        dataType: 'json',
        success: (data) => {
            $('#memberCount').innerHTML = 'Member count: ' + data['members_count'];
        },
        error: (error) => {
            console.log(error)
        }
    })
});