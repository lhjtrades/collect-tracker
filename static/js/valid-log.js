    // Wait for the DOM to be ready
$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("form[name='log']").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      username: "required",
      password: {
          required: true
      }
    },
    // Specify validation error messages
    messages: {
      username: "Please enter a username.",
      password: {
        required: "Please enter a password."
      }
    }
  });


});