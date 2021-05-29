$(document).ready(function () {
    $(".launch-modal").click(function () {
      var radio_value = $('input[name="choosed"]:checked').val();

      console.log(radio_value);
      console.log(variables.explanation);
      console.log(variables.answer);
      if (radio_value == variables.answer) {
        $(".modal-title").html(
          ' Correct<i class="fas fa-check-circle px-1 "></i>'
        );
        $(".modal-title").css("color", "green");
        $(".explanation").html("Explanation: "+ variables.explanation);
        $("input[name=result]").val("correct");
      } else {
        $(".modal-title").html(
          'Incorrect<i class="fas fa-times-circle px-1 "></i>'
        );
        $(".modal-title").css("color", "red");
        $(".explanation").html("Explanation:"+ variables.explanation);
        $("input[name=result]").val("incorrect");
      }
      $("#myModal").modal({
        backdrop: "static",
      });
    });
  });