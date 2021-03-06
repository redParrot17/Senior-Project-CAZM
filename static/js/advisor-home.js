
let $table = $('#table')

const AWAITING_ADVISOR_APPROVAL = 1;
const AWAITING_STUDENT_CREATION = 2;
const AWAITING_STUDENT_APPROVAL = 3;
const APPROVED = 4;
const STATUS_MAP = {
    [APPROVED]: 'Approved',
    [AWAITING_STUDENT_APPROVAL]: 'Awaiting Student Approval',
    [AWAITING_STUDENT_CREATION]: 'Awaiting Student Creation',
    [AWAITING_ADVISOR_APPROVAL]: 'Awaiting Advisor Approval',
};

let allAdvisees = [];   // A list of all advisee objects.
let uniqueYears = [];   // A unique set of year values.

// values used to filter and sort the listed results
let selectedStatusFilter = 'all';
let selectedYearFilter = $('#filterYearSelection').find('option:selected').text();
let selectedSortFilter = $('#sortBySelection').find('option:selected').text();
let searchBarText = $('#search-text').val();


/**
 * Adds advisees to the list
 * @param {Object} json 
 */
function setAdvisees(json) {
    allAdvisees = json;
    uniqueYears = [];

    allAdvisees.forEach(advisee => {
        // update the set of unique years
        if (!uniqueYears.includes(advisee.year)) {
            uniqueYears.push(advisee.year);
        }
    });
}

/**
 * Sets Text for email Button
 * @param {String} text 
 */
function setEmailButtonText(text) {
    $('#message-btn').html(`<i class="fa fa-envelope" aria-hidden="true"></i> Message ${text}`);
}

// ADVISEE FILTERING METHODS //
/**
 * Filters list of advisees by schedule status
 * @param {*} advisees 
 * list of advisees
 * @returns 
 */
function filterByStatus(advisees) {
    if (selectedStatusFilter === 'all')
        return advisees;
    else if (selectedStatusFilter === 'approved')
        return advisees.filter(a => a.status === APPROVED);
    else if (selectedStatusFilter === 'awaiting-advisor-approval')
        return advisees.filter(a => a.status === AWAITING_ADVISOR_APPROVAL);
    else if (selectedStatusFilter === 'awaiting-student-approval')
        return advisees.filter(a => a.status === AWAITING_STUDENT_APPROVAL);
    else if (selectedStatusFilter === 'awaiting-creation')
        return advisees.filter(a => a.status === AWAITING_STUDENT_CREATION);
    else return [];
}

/**
 * Filters list of advisees by enrollment year
 * @param {*} advisees 
 * list of advisees
 * @returns 
 */
function filterByYear(advisees) {
    if (selectedYearFilter !== 'All years...')
        return advisees.filter(a => a.year == selectedYearFilter);
    return advisees;
}

/**
 * Filters list of advisees by text in the search bar
 * @param {*} advisees 
 * @returns 
 */
function filterBySearch(advisees) {
    let search = searchBarText.toLowerCase();
    return advisees.filter(a => {
        if (a.id.toString().includes(search)) return true;
        let name = a.name.toLowerCase();
        return search.split(" ").every(s => name.includes(s))
    });
}

/**
 * Applies filters to list of advisees
 * @returns filtered advisee list
 */
function getFilteredAdvisees() {
    let advisees = allAdvisees;
    advisees = filterByStatus(advisees);
    advisees = filterByYear(advisees);
    advisees = filterBySearch(advisees);
    return advisees;
}

/**
 * Sorts advisees by selected option
 * @param {*} advisees 
 * list of advisees
 * @returns sorted advisee list
 */
function sortAdvisees(advisees) {
    let newAdvisees = advisees;

    if (selectedSortFilter === 'Sort by name')
        newAdvisees.sort(function(a, b) {
            let aName = a.name.toLowerCase();
            let bName = b.name.toLowerCase();
            if (aName > bName) return 1;
            if (aName < bName) return -1;
            return 0;
        });
    else if (selectedSortFilter === 'Sort by major')
        newAdvisees.sort(function(a, b) {
            let aMajor = a.major.toLowerCase();
            let bMajor = b.major.toLowerCase();
            if (aMajor > bMajor) return 1;
            if (aMajor < bMajor) return -1;
            return 0;
        });
    else if (selectedSortFilter === 'Sort by status')
        newAdvisees.sort(function(a, b){ return a.status - b.status });
    return newAdvisees;
}

// CALLBACK FUNCTIONS //



/**
 * Sends an html POST request to the current location
 * @param {Object} object json being sent to the endpoint
 */
function httpPost(object) {
    let xhr = new XMLHttpRequest();
    let url = window.location.href;
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.readyState === xhr.DONE) {
            if (xhr.status === 200) {

            }
        }
    }
    xhr.send(JSON.stringify(object));
}

/**
 * Select user by ID
 * @param {Number} user_id 
 * selected user ID
 */
function onClickAdvisee(user_id) {
    $('#student_id').val(user_id)
    document.forms[1].submit();
}

/**
 * Logout user
 */
function onClickLogout() {
    window.location.href = '/'
}

/**
 * Open message all advisees
 */
function onClickMessage() {
    let advisees = getFilteredAdvisees();

    let emailList = ""

    advisees.forEach(a=>{ emailList += a.email + ";" })

    location.href = "mailto:" + emailList

}

// TEMPLATES //

/**
 * Builds advisee bootstrap card
 * @param {*} advisee 
 * @returns advisee card DOM element
 */
function buildAdviseeCard(advisee) {
    return [
        `<div class="advisee borderStudentElements shadow p-3 mb-4 bg-body rounded" value="${advisee.id}" onclick="onClickAdvisee(${advisee.id})">`,
        '<div class="row align-items-center">',
        `<div class="col"><h5>${advisee.name}</h5></div>`,
        `<div class="col"><h5>${advisee.id}</h5></div>`,
        '<div class="col">',
        `<strong>Credits Completed:</strong> ${advisee.credits}<br>`,
        `<strong>Status:</status> ${STATUS_MAP[advisee.status] || 'Unknown'}`,
        '</div></div></div>'
    ].join('')
}

function buildYearOption(text, selected) {
    if (selected) return `<option selected>${text}</option>`;
    return `<option>${text}</option>`;
}

// SETUP FUNCTIONS //

function refreshTable() {
    $table.html('');
    let advisees = sortAdvisees(getFilteredAdvisees());
    advisees.forEach(advisee => {
        $table.html($table.html() + buildAdviseeCard(advisee));
    });
}

function refreshYears() {
    let $yearSelector = $('#filterYearSelection');
    $yearSelector.html(buildYearOption('All years...', true));  // reset the inner html
    uniqueYears.forEach(year => $yearSelector.html($yearSelector.html() + buildYearOption(year, false)));
}

function addListeners() {
    $('#filterStatusSelection').change(function() {
        let selection = $(this).find('option:selected');
        selectedStatusFilter = selection.val();
        setEmailButtonText(selection.text())
        refreshTable();
    });
    $('#filterYearSelection').change(function() {
        selectedYearFilter = $(this).find('option:selected').text();
        refreshTable();
    });
    $('#sortBySelection').change(function() {
        selectedSortFilter = $(this).find('option:selected').text();
        refreshTable();
    });
    $('#search-btn').click(function() {
        searchBarText = $('#search-text').val();
        refreshTable();
    });
    $('#search-text').on('keyup', function (e) {
        // Disabling textbox to avoid multiple submits.

        searchBarText = $(this).val();
        refreshTable();

        // Re-enabling textbox

    });
}

$(document).ready(function() {
    refreshYears();
    addListeners();
    refreshTable();

    $('#emailRichText').richText();
});
