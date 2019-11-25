var getCategoryByBrand = (e) => {

    var brandId = e.options[e.selectedIndex].value;

    $.ajax({
        url: '/product/category' + `?brand_id=${brandId}`,
        method: 'GET',
        contentType: 'application/json',
        beforeSend: function () {
            $("#select-category").empty();
            $('#select-category').prop("disabled", false);
        },
        success: function (data) {
            console.log(data.length);
            if (data.length > 0) {
                $('#select-category').prop("disabled", false);

                for (let i = 0; i < data.length; i++) {
                    $('#select-category').append($('<option>', {
                        value: data[i]['id'],
                        text: data[i]['name'],
                    }));
                }

            } else {
                $("#select-category").attr("disabled", true);
            }
            $('#foo').replaceWith(data);
        }
    });
}
