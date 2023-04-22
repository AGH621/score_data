# TO DO #


### Summary ###

* Streams for family scores (new branch)
* About data modules
* Clean data & error handling


### About Data Module ###

* Set up spreadsheet & define data to be captured
* 1 entry per family
* Upload to dictionary with PyExcel

### Driving Code ###

* Mongo db schema
* Code for loading into db

### Clean Data ###

* Add musicxml files to directory one letter at a time
* Write debugging/error handling code for each problem
* Do above for any errors thought of but not found

### Data Validation/File Info###

* New git branch
* Figure out how to add file information for a single score to an existing score dictionary.
* Figure out how to add/modify individual entries to an existing score dictionary when a cache is rebuilt

### Pitch Data ###

* Handle the error of a score part being a blank staff. Generate another musicxml from "Astonishing" musx for the test case.

### Other Data ###

* Rebuild the repeats module using parsed.parts[0].recurse().getElementsByClass(repeat.RepeatMark) to get the repeats.




