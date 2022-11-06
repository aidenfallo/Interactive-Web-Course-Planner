function copyInput() {
  let dropdown1Element = document.getElementById("degreeName1")
  let dropdown2Element = document.getElementById("degreeName2")
  let major1 =
  dropdown1Element.options[dropdown1Element.selectedIndex].id;
  let major2 =       
  dropdown2Element.options[dropdown2Element.selectedIndex].id;
  let sendBackend = {"major1" : major1, "major2" : major2};
  
  ajaxPostRequest("/send", JSON.stringify(sendBackend), callback);
}

function callback(jsonData) {
  let data = JSON.parse(jsonData);
  let course1 = document.getElementById("courseTable1")
  course1['innerHTML'] = data["major1"]
  let course2 = document.getElementById("courseTable2")
  course2["innerHTML"] = data["major2"]
  let shared = document.getElementById("shared")
  shared["innerHTML"] = data["shared"]
}