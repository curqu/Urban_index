# Urban & Suburban Development Index
A python script for ArcMap 10.6 classifying urban, suburban and rural areas, based on the Global Human Settlement Layer.

- - - -
# Dependencies
 - ArcMap 10 (tested with version 10.6) with Spatial Analyst License
 - Designed for use with GHSL population and built-up layers at 250m resolution, data available at:
   http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GPW4_GLOBE_R2015A/
   http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_LDSMT_GLOBE_R2015B/ 
   and Accessibility layer from the MAP, available here:
   https://map.ox.ac.uk/research-project/accessibility_to_cities/

- - - - 
# Instructions for Use
  ## Purpose & Usage
  This script is designed to compute a GHSL-based raster layer, with increased resolution and an added suburban class. This is useful for applications requiring knowledge about the nature of human settlements at a larger spatial scale, and to analyze urban / suburban / rural populations without relying on municipal boundaries. The script is currently designed to be run from the Python interactive window in ArcMap, but could be modified to be used as a toolbox script with a graphical interface.
  ## Executing the Program
  While using the program does not require any knowledge of Python, the user will be required to adjust variable inputs to match their working environment and application, as described below. These edits should be made in an IDE or text editor of the user's choice, such as IDLE or Notepad++. 
  Before execution, environment variables and inputs should be set:
  
- - - -  
# Background Information
The program uses the same criteria as the Global Human Settlement Layer developed by the European Commission's Joint Research Council. The GHSL classifies pixels into 4 categories: Urban center, Urban cluster, rural and uninhabited. This program adds a suburban class, created by sub-classifying "rural" cells based on their accessibility to urban centers.
## About the GHSL
The GHSL uses a global population dataset with satellite derived building footprint data to classify human settlement at a global scale. The original GHSL with 1km resolution is available for download at: https://ghsl.jrc.ec.europa.eu/data.php. 

## About the MAP Accessibility Dataset

## Classification Criteria
### Urban Centers
### Urban Clusters
### Rural
### Suburban
### Uninhabited

- - - - 
# Potential Applications & Modifications
