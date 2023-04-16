$.ajax({
    url: '/questions',
    dataType: 'json',
    success: function (data) {
        console.log('got response from service');
        // Loop through the questions data and generate HTML for each row
        for (let i = 0; i < data.length; i++) {
            const question = data[i].question_text;
            const prediction = data[i].target;
            const rowHtml = '<tr><td>' + question + '</td><td>' + prediction + '</td></tr>';
            $('#questions-table tbody').append(rowHtml);
        }
    },
    error: function (error) {
        console.log(error);
        const rowHtml = '<tr><td>unable to load questions</td><td></td></tr>';
        $('#questions-table tbody').append(rowHtml);
    }
});