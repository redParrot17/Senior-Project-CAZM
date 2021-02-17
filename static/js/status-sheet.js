function loadStatusSheet(reqs) {
	for (let value of Object.values(reqs)) {

		let fieldset = document.createElement("fieldset")
		fieldset.classList = "statusSheetSectionContainer container rounded"

		let legend = document.createElement("legend")
		legend.classList = "StatusSheetTitles"
		legend.innerText = value.title

		fieldset.appendChild(legend)

		let container = document.getElementById("req-list")
		container.appendChild(fieldset)

		let courselist = document.createElement("ol")
		let courseAry = value.classes

		for(let i in courseAry){
		
			let li = document.createElement("li")
			li.innerHTML = courseAry[i]
			courselist.appendChild(li)
		}
		fieldset.appendChild(courselist)
	}

}