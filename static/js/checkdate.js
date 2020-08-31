$( document ).ready(function() {
    var is_checked = $('#no-date').is(":checked");
     if(is_checked) {
        prev_val = $("#date").val();
        $("#date").val("");
     } else {
        $("#date").val(prev_val);
     }
     $("#date").prop("readonly", is_checked);
});
$("#no-date").change(function() {
     var is_checked = $(this).is(":checked");
     if(is_checked) {
        prev_val = $("#date").val();
        $("#date").val("");
     } else {
        $("#date").val(prev_val);
     }
     $("#date").prop("readonly", is_checked);
});