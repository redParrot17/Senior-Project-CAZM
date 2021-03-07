function toggleSideBar(event){
  let btn=event.target.parentElement;
  if(btn.classList.contains("selected")){
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("middle").style.marginRight= "0";
    document.getElementById("nav").style.marginRight= "0";
    btn.classList.remove("selected");
    btn.innerHTML='<i class=" openbtn fas fa-arrow-circle-left rounded-circle" ></i>';
  }
  else{
    btn.classList.add("selected");
    document.getElementById("mySidebar").style.width = "25%";
    document.getElementById("middle").style.marginRight = "25%";
    document.getElementById("nav").style.marginRight = "25%";

    btn.innerHTML='<i class=" openbtn fas fa-arrow-circle-right rounded-circle" ></i>';
  }

}
function openNav() {
  document.getElementById("mySidebar").style.width = "50hw";
  document.getElementById("middle").style.marginRight = "50hw";
  //document.getElementById("nav").style.marginRight = "275px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("middle").style.marginRight= "0";
  //document.getElementById("nav").style.marginRight= "0";
}
