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
  This script is designed to compute a GHSL-based raster layer, with increased resolution and an added suburban class. This is useful for applications requiring knowledge about the nature of human settlements at a larger spatial scale, and to analyze urban / suburban / rural populations without relying on municipal boundaries. The script is currently designed to be run from the Python interactive window in ArcMap, but could be modified to be used as a toolbox script with a graphical interface.
  ## Executing the Program
  While using the program does not require any knowledge of Python, the user will be required to adjust variable inputs to match their working environment and application, as described below. These edits should be made in an IDE or text editor of the user's choice, such as IDLE or Notepad++. 
  Before execution, environment variables and inputs should be set:
  ### Environment workspace
  The environment needs to be set to the working directory, which should include all the files specified below as inputs, as well as a default geodatabase file. The workspace should *not* be the geodatabase file itself. The following line should be edited so that the directory in quotations matches the working directory. Note that "/" replaces "\" in the path.
  
  ``arcpy.env.workspace = "c:/pathto/mydirectory/myworkspacefolder"``
  
  ### Input Layers
  All input layers from the datasets above should be clipped to the study area extent before running the module. If datasets do not need reprojection, the projection layer can be set to an input, or can be deleted if reprojection block in the program is removed - this option will be discussed further in modification section below. There are four input layers required, the population & built up layers (from GHSL dataset), the accessibility layer (from MAP dataset) and a layer defining the desired projection for the study area. The user should change the following layer names (in quotations) to match their clipped inputs, for example ``"accessibility.tif"`` would become ``my_clipped_accessibility_dataset.tif"``:

 `` ## Input Accessibility Layer
in_access = "accessibility.tif"``

``## Input Population Layer
in_pop = "GHS_POP_2015"``

``## Input Built-Up Layer
in_built = "GHS_BUILT2014"``

The following projection layer is only used to reproject the above 3 datasets to an appropriate projection for the study area. It can be a raster, polygon, line or point layer - it must only be a projected layer and match the study area extent. It will not be used for any classification steps. Edit the following line of the program so that the file in quotes is the projection layer:

``## Input Regional Extent Projection  Layer
in_region = "my_projected_study_area"``

### Accessibility Threshold Parameter *** clarify why 2 SD is chosen, give better justification for default 
This variable defines the threshold used to classify suburban cells (vs. rural). The default value is 40, which reflects the author's idea of a "reasonable" time distance for daily travel to the nearest urban center. This variable should be defined based on local context and the application. 

For applications that wish to learn about exisitng patterns / relationships between urban / suburban / rural space and populations: the threshold should reflect the time distance that people are willing to commute - such as + 2 standard deviations from the average daily commute time. This criteria reflects the connectedness of pixels in question to an urban center, using employment as a proxy for all social connections. When this type of data is not available, analysts use a constant * the mean commute time to estimate 2 standard deviations.

For applications assessing future development goals/locations: a threshold based on the mean commute time, desired commute time or relevant literature is more appropriate. 

The default value can be used if relevant data is not available, but may reduce the quality of the outputs when it is inappropriate for local context.

To obtain an output analogous to the original GHSL output at 250m, the accessibility threshold value can be set to 0.
The following line in the program should be editted to reflect the desired accessibility threshold value:
 
 ``suburban_thresh = 40``
- - - -  
# The Output Human Settlement Layer
In the output layer, classes are enumerated from 0-4, where 4 is urban center, 3 is urban cluster, 2 is suburban, 1 is rural and 0 is uninhabited. Below is a guide 

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
