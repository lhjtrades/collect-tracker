    // Wait for the DOM to be ready
$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("form[name='add']").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      account: "required",
      platform: "required",
      giving: "required",
      getting: "required"
    },
    // Specify validation error messages
    messages: {
      account: "Please enter an account name.",
      platform: "Please enter a platform.",
      giving: "Please enter what you're giving.",
      getting: "Please enter what you're getting."
    }
  });
});