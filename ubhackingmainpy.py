import bottle
import csv
import json

@bottle.route("/")
def serve_html():
  return bottle.static_file("index.html", root=".")

@bottle.route("/ajax.js")
def serve_ajax():
  return bottle.static_file("ajax.js", root=".")

@bottle.route("/script.js")
def serve_script():
  return bottle.static_file("script.js", root=".")

@bottle.route("/style.css")
def serve_style():
  return bottle.static_file("style.css", root=".")

@bottle.post("/send")
def receive_message():
  message = {"major1" : "", "major2" : "", "shared" : ""}
  messageContents = json.loads(bottle.request.body.read().decode())
  if (messageContents["major1"] == "null" and messageContents["major2"] != "null"):
    message["major2"] = make_table(get_courses(messageContents["major2"]), "Exclusive Major 2")
    
  elif messageContents["major2"] == "null" and messageContents["major1"] != "null":
    message["major1"] = make_table(get_courses(messageContents["major1"]), "Exclusive Major 1")

  elif messageContents["major2"] == "null" and messageContents["major1"] == "null":
    pass
  else:
    courses = compare_courses(messageContents["major1"], messageContents["major2"])
    message["major1"] = make_table(courses[0], "Exclusive Major 1")
    message["major2"] = make_table(courses[1], "Exclusive Major 2")
    message["shared"] = make_table(courses[2], "Shared")
  return json.dumps(message)
  



def get_courses(major_csv):
  major_csv += ".csv"
  # open corresponding file
  with open(major_csv) as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    # iterate through each line
    for line in reader:
      line_dictionary = {}
      #assign correct values in dictionary
      course_description = line[0] + ' ' + line[1] + ' ' + line[2] + ' ' + line[3] 
      line_dictionary['Course Description'] = course_description
      line_dictionary['Credits'] = line[4]
      line_dictionary['Period'] = line[5]
      #append each dictionary (line) to list
      data.append(line_dictionary)
      #print(data)
  return data


def compare_courses(major1,major2):
  master_list = []
  major1Data = get_courses(major1)
  major2Data = get_courses(major2)
  major1dataCopy = major1Data.copy()
  major2dataCopy = major2Data.copy()
  shared_courses = []
  # iterate through major1, checking if course in major1 is in major2
  for i in major1Data:
    if i in major2Data:
      shared_courses.append(i)
      major1dataCopy.remove(i)
      major2dataCopy.remove(i)

  master_list.append(major1dataCopy)
  master_list.append(major2dataCopy)
  master_list.append(shared_courses)
  return master_list


def make_table(classes, major):
  table = "<h2><center>" + major + " Required Courses</center></h2><table id=\"courses\" class=\"center\">" 
  table += "<tr><th>Course Description</th><th>Credits</th><th>Periods</th></tr>"
  for line in classes:
      table += "<tr><td>" + line["Course Description"] + "</td><td>" + line["Credits"] + "</td><td>" + line["Period"] + "</tr>"
  table += "</table>" 
  return table

bottle.run(host="0.0.0.0", port=8080)

