# TO DO #


### Summary ###

* Driving code for data modules
* Streams for family scores (new branch)
* About data modules
* Clean data & error handling


### About Data Module ###

* Set up spreadsheet & define data to be captured
* 1 entry per family
* Upload to dictionary with PyExcel

### Driving Code ###

* One module which calls all the other data modules.  Class?
* Refactor data module code to make processing as efficient as possible.
* Mongo db schema
* Code for loading into db

### Clean Data ###

* Add musicxml files to directory one letter at a time
* Write debugging/error handling code for each problem
* Do above for any errors thought of but not found

### Family Score Streams ###

* New git branch
* Have an upload or filepath for each score in the family

### Pitch Data ###

* Handle the error of a score part being a blank staff. Generate another musicxml from "Astonishing" musx for the test case.

### Other Data ###
* Rebuild the repeats module using parsed.parts[0].recurse().getElementsByClass(repeat.RepeatMark) to get the repeats.




