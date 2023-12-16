$(document).ready(function () {
    $(".card-img").click(function () {
        var checkbox = $(this).siblings('.card-checkbox');
        checkbox.prop("checked", !checkbox.prop("checked"));
        checkbox.change();
    });

    $("#nextTry").click(function () {
        $("input:checkbox").prop('checked', false);
        $("#cardSelectionForm").submit();
    });
});
