var classes;
document.getElementById("toggleBtn").click();

/**
 * Toggle Sidebar
 * @param {*} event 
 */
function toggleSideBar(event){
  let btn=document.getElementById("toggleBtn");
  if(btn.classList.contains("selected")){
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("middle").style.marginRight= "0";
    document.getElementById("nav").style.marginRight= "0";
    document.getElementById("middle").classList.remove('col-5');
    document.getElementById("middle").classList.add('col-8');
    btn.classList.remove("selected");

    btn.innerHTML='<i class="openbtn shaddow btn-secondary fas fa-arrow-circle-left rounded-circle"></i>';
  }
  else{
    btn.classList.add("selected");
    document.getElementById("mySidebar").style.width = "25%";
    document.getElementById("middle").style.marginRight = "25%";
    document.getElementById("nav").style.marginRight = "25%";
    document.getElementById("middle").classList.remove('col-8');
    document.getElementById("middle").classList.add('col-5');

    btn.innerHTML='<i class="openbtn shaddow btn-secondary fas fa-arrow-circle-right rounded-circle"></i>';
  }

}

/**
 * Runs tutorial Dialogue
 * @param {*} event 
 */
function openTutorial(event){
  introJs().setOptions({scrollToElement: false, disableInteraction: true}).start();
  let btn=document.getElementById("toggleBtn");
  btn.classList.add("selected");
  document.getElementById("mySidebar").style.width = "25%";
  document.getElementById("middle").style.marginRight = "25%";
  document.getElementById("nav").style.marginRight = "25%";
  document.getElementById("middle").classList.remove('col-8');
  document.getElementById("middle").classList.add('col-5');
  let myElement = document.getElementById('disclaimer');
  var topPos = myElement.offsetTop;
  document.getElementById('main-schedule').scrollTop = topPos - 110;

  btn.innerHTML='<i data-title="Toggle Side-Bar" data-step="8" data-intro="This button will toggle the right side bar" class="openbtn shaddow btn-secondary fas fa-arrow-circle-right rounded-circle"></i>';
}



function openNav() {
  document.getElementById("mySidebar").style.width = "50hw";
  document.getElementById("middle").style.marginRight = "50hw";
  document.getElementById("middle").classList.remove('col-8');
  document.getElementById("middle").classList.add('col-5');
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("middle").style.marginRight= "0";
  document.getElementById("middle").classList.remove('col-5');
  document.getElementById("middle").classList.add('col-8');
}

/**
 * Search classlist by what is in the search bar, and update the listed courses
 */
function searchClasses() {
  $.getJSON($SCRIPT_ROOT + '/searchClasses', {
      class_name: $('input[id="search-bar"]').val()
  }, function (data) {
      classes = data
      
      let container = document.getElementById("course-container");
      container.innerHTML = "";
      for (let i in classes) {
          let course = classes[i]
          let div = createCourseDiv(course)
          container.appendChild(div)

      }
  });
}
