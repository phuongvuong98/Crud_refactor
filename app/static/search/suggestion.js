$('#user_input').on('input', function (e) {

    var user_input = $('#user_input').val();

    console.log(user_input);

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "/search/suggestion",
        "method": "POST",
        "headers": {
            "cache-control": "no-cache",
            "Content-Type": "application/json"
        },
        "processData": false,
        data: "q=" + user_input
    }

    $.ajax(settings).done(function (response) {
        console.log(response);
        var data = response.data;
        console.log(data.length);

        titles = [];
        for (var i = 0; i < data.length; i++) {
            field_name = data[i]["_source"]["name"] || data[i]["_source"]["detail"] || data[i]["_source"]["value"] || data[i]["_source"]["store_name"] || data[i]["_source"]["price"];
            titles.push(field_name);
        }
        console.log(titles);
        $("#user_input").autocomplete({
            source: titles
        });

    });
});



