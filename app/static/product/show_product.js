
$(".mb-2.btn.btn-md.btn-info.mr-1").on("click", function () {
    var currentRow = $(this).closest("tr");

    var productId = currentRow
        .find("td")
        .eq(0)
        .text();

    var brandRow = currentRow
        .find("td")
        .eq(3);

    let brandName = brandRow.text();
    let brandId = brandRow.data("brandId");

    getCategoryByBrand(brandId);

    var productDetail = currentRow
        .find("td")
        .eq(1)
        .text();


    $("#product-edit").val(productDetail);
    $("#brand_edit option:contains(" + brandName + ")").prop("selected", true);
    $("#id_edit").val(productId);
});

var getCategoryByBrand = (brandId) => {
    if (brandId == undefined) {

        brandId = $("#brand_edit :selected").val();
    }

    $.ajax({
        url: '/product/category' + `?brand_id=${brandId}`,
        method: 'GET',
        contentType: 'application/json',
        beforeSend: function () {
            $("#category_edit").empty();
            $('#category_edit').prop("disabled", false);
        },
        success: function (data) {

            if (data.length > 0) {
                $('#category_edit').prop("disabled", false);

                for (let i = 0; i < data.length; i++) {
                    $('#category_edit').append($('<option>', {
                        value: data[i]['id'],
                        text: data[i]['name'],
                    }));
                }

            } else {
                $("#category_edit").attr("disabled", true);
            }
        }
    });
}
