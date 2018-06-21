/********************************

Zenith's JavaScript Document for Custom Scripts
Created By: Amazyne Themes

*********************************/

function localStorageSupported() {
	try {
		return "localStorage" in window && window["localStorage"] !== null;
	} catch (e) {
		return false;
	}
}