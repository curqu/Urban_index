# Urban Development Index
A python script for ArcMap 10.6 classifying urban, suburban and rural areas, based on the Global Human Settlement Layer (GHSL).

- - - -
# Dependencies
 - ArcMap 10 (tested with version 10.6) with Spatial Analyst License
 - Designed for use with GHSL population and built-up layers at 250m resolution, data available at:
   http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GPW4_GLOBE_R2015A/
   http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_LDSMT_GLOBE_R2015B/ 
   and Accessibility layer from the Malaria Atlas Project (MAP), available here:
   https://map.ox.ac.uk/research-project/accessibility_to_cities/

- - - - 
# Instructions for Use
  ## Purpose & Usage
  This script is designed to compute a GHSL-based raster layer, with increased resolution and an added suburban class. This is useful for applications requiring knowledge about the nature of human settlements at a larger spatial scale, and to analyze urban, suburban, and rural populations without relying on municipal boundaries. The script is currently designed to be run from the Python interactive window in ArcMap, but could be modified to be used as a toolbox script with a graphical interface.
  ## Executing the Program
  While using the program does not require any knowledge of Python, the user will be required to adjust variable inputs to match their working environment and application, as described below. These edits should be made in an IDE or text editor of the user's choice, such as IDLE or Notepad++. 
  
  Before execution, the following environment variables and inputs should be set.
  ### Environment workspace
  The environment needs to be set to the working directory, which should include all the files specified below as inputs, as well as a default geodatabase file. The workspace should *not* be the geodatabase file itself. The following line should be edited so that the directory in quotations matches the working directory. Note that "/" replaces "\\" in the path.
  
  ``arcpy.env.workspace = "c:/pathto/mydirectory/myworkspacefolder"``
  
  ### Input Layers
  Input layers from the datasets listed in the dependencies section include a population layer and a "built up" layer from the GHSL dataset; and an accessibility layer from MAP. The user should ensure that they data they select is at a 250m resolution, and from the correct year. All three input layers should be clipped to the study area and reprojected (if appropriate) before running the script. The user should change the following layer names (in quotations) to match their clipped inputs:

 `` ## Input Accessibility Layer
in_access = "accessibility.tif"``

``## Input Population Layer
in_pop = "GHS_POP_2015"``

``## Input Built-Up Layer
in_built = "GHS_BUILT2014"``

For example ``"accessibility.tif"`` would become ``my_clipped_accessibility_dataset.tif"``

The script can be run in the Python interactive window by running ``execfile(c:/mydirectory/urban_index-master/urbanization_index.py``. Be sure to specify the full path to where the script is located in your system.

### Accessibility Threshold Parameter  
This variable defines the threshold used to classify suburban cells (vs. rural). It represents the time (in minutes) to travel to the nearest urban center from a given cell. The default value is set at 40 minutes, which is arbitrary and may not be meaningful for any particular application, but can be used if relevant data is not available. 
To obtain an output analogous to the original GHSL output at 250m, the accessibility threshold value can be set to a negative value, otherwise it should be defined based on local context and the application. 

For applications that wish to learn about exisitng patterns and relationships between urban, suburban, and rural space or populations, the threshold should reflect the time distance that people are willing to commute on a daily basis. One might find it reasonable to use data about commute times to work as a proxy for other social connections, as this data is typically available for metropolitan regions. For example, the user might choose to set it at +2 standard deviations from the mean daily commute time, in order to include the spread of commute times while excluding extreme outliers. When this type of data is not available, analysts could substitute a constant multiplied by the mean commute time to estimate a meaningful threshold value.

For applications assessing future development goals/locations: a threshold based on the mean commute time, desired commute time or relevant literature is more appropriate. 

The following line in the program should be editted to reflect the desired accessibility threshold value:
 
 ``suburban_thresh = 40``
- - - -  
# The Output Human Settlement Layer
In the output layer, classes are enumerated from 0 to 4, where 4 is urban center, 3 is urban cluster, 2 is suburban, 1 is rural and 0 is uninhabited. The output is based on the classes in the GHSL: urban center, urban cluster, rural and uninhabited. I have added the suburban class to account for areas with low population densities but that have significant connections to urban areas. The GHSL classes are based on EU statistical classifications, but as a number of datasets and modules are based on the GHSL, these classes are meaningful outside of that context as well. Here I will briefly describe how to interpret the output layer, class by class. The parameters used to define classes are explained in the next section.

## Urban Center (4)
These are regions with high population density or where man-made structures are prevalent. They represent the central parts of medium to large cities, and are regions that can be strongly associated with features of urban space. 

## Urban Cluster (3)
Urban clusters are areas that have a medium population density. They are closer to urban space than rural, although they may lack features typically associated with larger cities. Smaller towns that have a distinct core will often be urban clusters, as well as cores of what we might consider suburbs. It is important to note the distinction between how we think about "suburbs" in everyday language and the way this program treats the distinction between suburban and urban. Here, we consider population density and the presence of man-made objects, rather than municipal borders, as indicators of urban areas. The urban cluster class is useful for distinguishing "suburban" regions that are more urban than rural in their built form and population density.

## Suburban (2)
Suburban cells have a low population density, but are distinct from rural areas in that their inhabitants can access urban centers with relative ease. They will often be part of the urban center's municipal or metropolitan boundaries, but typically lack the features of urban space. This class is added because running the GHSL with its original parameters at a 250m resolution often results in rural-classed areas which are intricately connected to cities. This result may obscure studies that seek to establish differences between urban and rural populations.

## Rural (1)
Rural cells are those with a very low population density, and far enough removed from urban centers that the population does not have easy access to features of cities (such as specialty commercial areas, many types of employment, and urban spaces more generally). 

## Uninhabited (0)
These are cells which have no population. There could still be a human presence as infrastructure and industry are not accounted for in this class. It is worth noting that as the GHSL has a global scope, it does not exclude waterbodies which get classified as "uninhabited".

Here is an example of an output for the Pacific Northwest of North America. This image includes the Vancouver, Victoria and Seattle metropolitan areas.
Here, darker pink areas are urban centers, light pink are urban clusters, orange is suburban (with the accessibility threshold at the default value) and green are rural areas. All the white areas are uninhabited. 

![alt text](https://github.com/curqu/Urban_index/blob/master/Capture.PNG)

- - - -
# Classification Criteria
The classification criteria used for urban centers urban clusters, rural and uninhabited areas is analogous to the criteria used in the original GHSL procedure, adapted for a 250m resolution. The suburban layer is classified out of cells the GHSL procedure defines as rural, using the accessibility threshold as set by the user.

## Urban Centers
Urban centers are defined as continuous regions with a total population of at least 50,000. Regions consist of grid cells with a minimum population of 375 people per cell, or a minimum "built up" value of 50%. They are defined using 4-connectivity with gaps filled.
## Urban Clusters
Urban clusters are continuous regions with a total population of at least 5,000. The regions consist of grid cells with a minimum population of 75 people per cell.  They are defined using 8 connectivity, gaps are not filled.
## Suburban
Suburban cells have populations too low to be classed as urban center or urban cluster, but are within the accessibility threshold defined by the user. Suburban areas should be considered to be close enough to the nearest urban center so that residents likely work or shop there. See 'Executing the Program' above for a detailed discussion about setting an appropriate accessibility threshold value for classifying suburban cells.
## Rural
Rural cells are defined in the GHSL as any cells with population greater than 0 that are not part of an urban center or urban cluster. In this program, rural cells must also have an accessibility value greater than the defined threshold - they are considered too far from the nearest urban center to be part of its suburbs.
## Uninhabited
Grid cells with 0 population are defined as uninhabited.
- - - - 
# Additional Information
The above criteria are derived from the GHSL, a 1km resolution raster that classifies the entire globe into 4 categories: Urban center, Urban cluster, rural and uninhabited. The additional suburban class is created using an Accessibility layer created by the Malaria Atlas Project. 

## About the Global Human Settlement Layer 
The EU Joint Research Council's GHSL uses a global population dataset with satellite derived building footprint data to classify human settlement at a global scale. The original GHSL with 1km resolution is available for download at: https://ghsl.jrc.ec.europa.eu/data.php. The original GHSL categories are based on statistical classes of human settlement used by the EU. It was originally intended to be used in disaster response and mitigation, however has proved useful for many more applications and underlies a variety of other global data products.
More information about the GHSL, it's purpose and conext is available at:
https://ghsl.jrc.ec.europa.eu/degurba.php
https://ghsl.jrc.ec.europa.eu/documents/atlas2016_section2_4.pdf?t=1476110582
https://ghsl.jrc.ec.europa.eu/documents/atlas2016_section2_3.pdf?t=1476110581

## About the Malaria Atlas Project Accessibility Dataset
In order to classify the suburban class, we add an additional input dataset to quantify connectivity between cells with "rural" characteristics and cities. The MAP Accessibility layer represents the time in minutes to reach the nearest urban center from a given cell, and thus is appropriate for establishing connectivity. It is based on the GHSL outputs, so the urban centers used in the accessibility input layer should closely reflect those classified by the program.
To read more about the Malaria Atlas Project and their global Accessibility dataset, see:
https://map.ox.ac.uk/research-project/accessibility_to_cities/

- - - - 
# Potential Applications & Modifications
The program is designed for applications at a regional scale - analyzing a single metropolitan area, county, state/province or small country. Many of the applications suggested on the GHSL website, such as time-series analysis, quantifying urbanization, and measuring growth of informal settlements are made possible at larger spatial scales. The module helps remove bias in qualitiative classification of human settlements as well as make it possible when municipal planning data is not available/accurate. The addition of a suburban class makes it possible to compare urban, suburban and rural populations. One could use the output to analyze health outcomes, education, demographic changes, voting preference, social and economic wellbeing and other potential settlement-based disparities.

The program can be modified to work with alternative population and building footprint data. It can also be extended to run as an ArcToolbox script so variables could be defined in a graphical environment. 

Output analogous to the original GHSL output, at 250m resolution can be obtained by setting the accessibility threshold value to a negative value.
