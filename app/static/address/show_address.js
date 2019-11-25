
$(".mb-2.btn.btn-md.btn-info.mr-1").on("click", function () {
    var currentRow = $(this).closest("tr");

    var addressId = currentRow
        .find("td")
        .eq(0)
        .text();

    var cityRow = currentRow
        .find("td")
        .eq(3);

    let cityName = cityRow.text();
    let cityId = cityRow.data("cityId");

    getDistrictByCity(cityId);

    var addressDetail = currentRow
        .find("td")
        .eq(1)
        .text();


    $("#address-edit").val(addressDetail);
    $("#city_edit option:contains(" + cityName + ")").prop("selected", true);
    $("#id_edit").val(addressId);
});

var getDistrictByCity = (cityId) => {
    if (cityId == undefined) {

        cityId = $("#city_edit :selected").val();
    }

    $.ajax({
        url: '/address/district' + `?city_id=${cityId}`,
        method: 'GET',
        contentType: 'application/json',
        beforeSend: function () {
            $("#district_edit").empty();
            $('#district_edit').prop("disabled", false);
        },
        success: function (data) {

            if (data.length > 0) {
                $('#district_edit').prop("disabled", false);

                for (let i = 0; i < data.length; i++) {
                    $('#district_edit').append($('<option>', {
                        value: data[i]['id'],
                        text: data[i]['name'],
                    }));
                }

            } else {
                $("#district_edit").attr("disabled", true);
            }
        }
    });
}
