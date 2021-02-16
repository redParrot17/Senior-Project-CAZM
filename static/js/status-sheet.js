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
	}

}