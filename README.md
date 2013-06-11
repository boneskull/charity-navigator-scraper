Charity Navigator Scraper
=====================================================================
Jeffrey Horn  
`<jrhorn424@gmail.com>`  
[@jrhorn424](http://twitter.com/jrhorn424)

## Overview
Charity Navigator (CN) provides only a Search API at the moment. This is useful for republishing charity information on another website, but does not offer backend access to charity data. Access to these data are important for statistical analysis. The scraper locates and stores these data in a human- and machine-readable form to facilitate this analysis.

Scrapy builds an alphabetical list of charities index by CN, then processes the URLs gathered to store information about each charity. User scripts can then be used to convert this data into friendlier formats, such as JSON or CSV.

## Post-processing
Scripts in the `bin` directory can be used to process the data output by Scrapy. `charitynav_json.py` converts the output data to `JSON`, and `charitynav_json2csv.rb` converts the `JSON` to `CSV`. Included is alse `names.rb` which only grabs the charity names from a JSON input.

## Dependencies
For the scraper:
- python 2.6.5 or later
- [Scrapy](http://scrapy.org/)

For the user scripts:
- python 2.6.5 or later
- ruby 1.9.3 or later

## License
This is free software. It is licensed under the [GNU General Public License](http://www.gnu.org/licenses/gpl.html).

The data is a public service of [Charity Navigator](http://www.charitynavigator.org), but the data is likely owned by individual charities. CN collects this data. We have simply recollected it in a format suitable to research.

## API
Read about the [Charity Navigator Search API](http://www.charitynavigator.org/index.cfm?bay=content.view&cpid=809) and learn how to apply for access.

## Responsible Use
CN is not associated with this project or its authors in any way. CN makes this data available as a public service. Please do not abuse their servers.

This project **[Powered by Charity Navigator](http://www.charitynavigator.org/)**.
