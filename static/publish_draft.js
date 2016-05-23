function publishDoc(evt) {
    $.post('/published', {}, function (data) {
    $('#publish-draft').text('You\'ve published your draft!');
    $('#publish').attr('disabled', true);
    });

}

$('#publish').on('click', publishDoct);