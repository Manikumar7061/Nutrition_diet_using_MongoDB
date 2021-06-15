
window.onload = function(){
	$(document).on("click",".transferrows",function(){
		var getselectedvalues=$(".maintable input:checked").parents("tr").clone().appendTo($(".secondtable tbody").add(getselectedvalues));
	})