var header = document.getElementsByTagName("head")[0];
var plausible = document.createElement("script");
var domain_name = window.location.hostname;

plausible.async = "";
plausible.defer = "";
plausible.dataset["domain"] = domain_name;
plausible.src = "https://plausible.io/js/plausible.js";
header.appendChild(plausible);
