$( document ).ready(function() {
    $('.statuses').hide();
    $('#' + $('#typeselect').val()).show();
});

$(function() {
        $('#typeselect').change(function(){
            $('.statuses').hide();
            $('#' + $(this).val()).show();
        });
    });