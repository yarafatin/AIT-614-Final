$(document).ready(function () {
    console.log('loaded script');

    $('#question-submit').click(function () {
        var questionText = $('#question').val();
        var postData = JSON.stringify({'question_text': questionText});
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: postData,
            contentType: 'application/json',
            success: function (response) {
                console.log('successfully submitted');
                $('#result').text('Your question has been submitted. A moderator will review it before publishing.');
            },
            error: function (xhr, status, error) {
                console.log('failure calling service' + xhr.responseText);
            }
        });
    });

});