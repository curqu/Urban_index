# Urban & Suburban Development Index
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
  Before execution, environment variables and inputs should be set:
  ### Environment workspace
  The environment needs to be set to the working directory, which should include all the files specified below as inputs, as well as a default geodatabase file. The workspace should *not* be the geodatabase file itself. The following line should be edited so that the directory in quotations matches the working directory. Note that "/" replaces "\\" in the path.
  
  ``arcpy.env.workspace = "c:/pathto/mydirectory/myworkspacefolder"``
  
  ### Input Layers
  All input layers from the datasets above should be clipped to the study area and reprojected to an appropriate projection before running the module.  There are three input layers required, the population & built up layers (from GHSL dataset), and the accessibility layer (from MAP dataset). The user should change the following layer names (in quotations) to match their clipped inputs, for example ``"accessibility.tif"`` would become ``my_clipped_accessibility_dataset.tif"``:

 `` ## Input Accessibility Layer
in_access = "accessibility.tif"``

``## Input Population Layer
in_pop = "GHS_POP_2015"``

``## Input Built-Up Layer
in_built = "GHS_BUILT2014"``

The script can be run in the Python interactive window by running ``execfile(c:/mydirectory/urban_index-master/urbanization_index.py``. Be sure to specify the full path to where the script is located in your system.

### Accessibility Threshold Parameter *** clarify why 2 SD is chosen, give better justification for default 
This variable defines the threshold used to classify suburban cells (vs. rural). It represents the time (in minutes) to travel to the nearest urban center from a given cell. The default value is set at 40 minutes, which is arbitrary and may not be meaningful for any particular application, but can be used if relevant data is not available. 
To obtain an output analogous to the original GHSL output at 250m, the accessibility threshold value can be set to 0, otherwise it should be defined based on local context and the application. 

For applications that wish to learn about exisitng patterns and relationships between urban, suburban, and rural space or populations, the threshold should reflect the time distance that people are willing to commute on a daily basis. One might find it reasonable to use data about commute times to work as a proxy for other social connections, as this data is typically available for metropolitan regions. For example, the user might choose to set it at +2 standard deviations from the mean daily commute time, in order to include the spread of commute times while excluding extreme outliers. When this type of data is not available, analysts could substitute a constant times the mean commute time to estimate a meaningful threshold value.

For applications assessing future development goals/locations: a threshold based on the mean commute time, desired commute time or relevant literature is more appropriate. 

The following line in the program should be editted to reflect the desired accessibility threshold value:
 
 ``suburban_thresh = 40``
- - - -  
# The Output Human Settlement Layer
In the output layer, classes are enumerated from 0 to 4, where 4 is urban center, 3 is urban cluster, 2 is suburban, 1 is rural and 0 is uninhabited. The output is based on the classes in the GHSL: urban center, urban cluster, rural and uninhabited. I have added the suburban class to account for areas with low population densities but that have significant connections to urban areas. The GHSL classes are based on EU statistical classifications, but as a number of datasets and modules are based on the GHSL, these classes are meaningful outside of that context as well. Here I will briefly describe how to interpret the output layer, class by class.

## Uninhabited (0)
These are cells which have no population. There could still be a human presence as infrastructure and industry are not accounted for in this class. It is worth noting that as the GHSL has a global scope, it does not exclude waterbodies which get classified as "uninhabited".

## Rural (1)
Rural cells are those with a very low population density, and far enough removed from urban centers that the population does not have easy access to features of cities (such as specialty commercial areas, many types of employment, and urban spaces more generally). 

## Suburban (2)
These cells also have a low population density, but are distinct from rural areas in that their inhabitants can access urban centers without difficulty. These regions will often be part of the urban center's municipal or metropolitan boundaries, although they often will not have features of urban space. This class is added because running the GHSL with its original parameters at a 250m resolution often results in rural-classed areas which are intricately connected to cities. This result may obscure studies that seek to establish differences between urban and rural populations.

## Urban Cluster (3)
Urban clusters are areas that have a medium population density. They are closer to urban space than rural, althoigh may lack features typically associated with larger cities. Smaller towns that have a distinct core will often be urban clusters, as well as cores of what we might consider suburbs. It is important to note the distinction between how we think about "suburbs" in everyday language and the way this program treats the distinction between suburban and urban, as here we consider population density and the presence of man-made objects, and not municipal borders. The urban cluster class is useful for distinguishing "suburban" regions that are more urban than rural in their built form and population density.

## Urban Center (4)
These are regions with high population density or a dominance of man-made structures. They represent the central parts of medium to large cities. 

Here is an example of an output for the Pacific Northwest of North America. This image includes the Vancouver, Vicotia and Seattle metropolitan areas.
Here, darker pink areas are urban centers, light pink are urban clusters, orange is suburban (with the accessibility threshold at the default value) and green are rural areas. All the white areas are uninhabited. 

![alt text](https://github.com/curqu/Urban_index/blob/master/Capture.PNG)

- - - - 
# Background Information
The program uses the same criteria as the Global Human Settlement Layer developed by the European Commission's Joint Research Council. The GHSL classifies pixels into 4 categories: Urban center, Urban cluster, rural and uninhabited. This program adds a suburban class, created by sub-classifying "rural" cells based on their accessibility to urban centers.

## About the Global Human Settlement Layer *** explain urban center and urban cluster, make meaningful outside of context
The GHSL uses a global population dataset with satellite derived building footprint data to classify human settlement at a global scale. The original GHSL with 1km resolution is available for download at: https://ghsl.jrc.ec.europa.eu/data.php. The original GHSL categories are based on statistical classes of human settlement used by the EU. Outside of that framework, they may not be meaningful. By increasing the resolution of the output and adding an accessibility parameter, this program will extend the useability of the GHSL to a wider variety of applicaions.
The inputs for the original GHSL are a population raster and a layer they refer to as "built up": which represents the percentage of a pixel that contains human-made structures. To define the suburban class, we use accessibility data rom the Malaria Atlas Project.

## About the Malaria Atlas Project Accessibility Dataset
The MAP Accessibility layer represents the time in minutes to reach the nearest urban center from a given cell. It is based on the GHSL outputs, so the urban centers used in the accessibility input layer should closely reflect those classified by the program.

## Classification Criteria
### Urban Centers
Urban centers are defined as continuous areas of grid cells with a minimum population of 375 or a minimum "built up" value of 50%. Regions must have a minimum total population of 50,000. We use 4-connectivity with gaps filled.
### Urban Clusters
Urban clusters are continuous areas of grid cells with a minimum population of 75. Regions must have a minimum total population of 5,000. They are defined using 8 connectivity, gaps are not filled.
### Rural
Rural cells are defined in the GHSL as any cells with population greater than 0 that are not part of an urban center or urban cluster. In this program, rural cells are also defined by having an accessibility value greater than the defined threshold - they are considered too far from the nearest urban center to be part of it's suburbs.
### Suburban
Suburban cells have populations too low to be classed as urban center or urban cluster, but are within the defined accessibility threshold. Suburban areas should be considered as close enough to the nearest urban center so that residents likely work or shop there. See 'Executing the Program' above for a detailed discussion about setting an appropriate accessibility threshold value for classifying suburban cells.
### Uninhabited
Grid cells with 0 population are uninhabited.
- - - - 
# Potential Applications & Modifications
The program is designed for applications at a regional scale - analyzing a single metropolitan area, county, state/province or small country. Many of the applications suggested on the GHSL website, such as time-series analysis, quantifying urbanization, and measuring growth of informal settlements are made possible at larger spatial scales. The module helps remove bias in qualitiative classification of human settlements as well as make it possible when municipal planning data is not available/accurate. The addition of a suburban class makes it possible to compare urban, suburban and rural populations. One could use the output to analyze health outcomes, education, demographic changes, voting preference, social and economic wellbeing and other potential settlement-based disparities.

The program can be modified to work with alternative population and building footprint data. It can also be extended to run as an ArcToolbox script so variables could be defined in a graphical environment. 

To modify the program so that it does not reproject the input GHSL and MAP datasets, the reprojection module should be commented out or removed, and function arguments need to changed so that ``"region_pop.tif"`` becomes ``in_pop``, ``"region_built.tif"`` becomes ``in_built`` and ``region_access.tif`` becomes ``in_access``. 

Output analogous to the original GHSL output, at 250m resolution can be obtained by setting the accessibility threshold value to 0.
