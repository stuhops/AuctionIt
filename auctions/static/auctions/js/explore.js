// var acc = document.getElementsByClassName("accordion");
// var i;

// for (i = 0; i < acc.length; i++) {
//   acc[i].addEventListener("click", function() {
//     /* Toggle between adding and removing the "active" class,
//     to highlight the button that controls the panel */
//     this.classList.toggle("active");

//     /* Toggle between hiding and showing the active panel */
//     var panel = this.nextElementSibling;
//     if (panel.style.display === "block") {
//       panel.style.display = "none";
//     } else {
//       panel.style.display = "block";
//     }
//   });
// } 

function handleAuctionClick(inputAuctionID) {
    var headingID = "auction_heading_" + inputAuctionID;
    console.log("Looking for ID: " + headingID);
    var auctionHeading = document.getElementById(headingID);
    auctionHeading.setAttribute("style", "background-color: red;");

    var auctionListingID = "auction_" + inputAuctionID;
    var auctionListing = document.getElementById(auctionListingID);
    auctionListing.setAttribute("style", "visiblility: visible;")
}