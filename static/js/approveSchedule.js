
function approveBtn(ev){
  let container = document.getElementById("main-schedule");
  let newSchedule = container.querySelectorAll(".drag_item_fill");
  //console.log(newSchedule);

  let myCourses = [];

  newSchedule.forEach((item, index) => {
    let elements = (item.id).split("-");
    let course_code = elements[0];
    let semester = elements[1];
    let year = elements[2];

    myCourses.push({"course_code":course_code, "semester":semester, "year":year});

  });

  $.ajax
    ({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/studentSchReview/',
        dataType: 'json',
        contentType: "application/json",
        //json object to sent to the authentication url
        data: JSON.stringify(myCourses),
        success: function (data) {
          //alert("Data: " + data);


          console.log("Made it through ajax");
        }
    })
}
