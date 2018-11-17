################## URBAN / SUBURBAN / RURAL INDEX ###############

## Import Modules:

import arcpy
from arcpy.sa import *

#################################################################

## VARIABLES (USER DEFINED)

#################################################################

## SET WORKSPACE:

arcpy.env.workspace = "c:/temp/GEOB370_final"

#################################################################

## INPUT LAYERS: (see README for appropriate inputs)

## Input Accessibility Layer
in_access = "accessibility0.tif"

## Input Population Layer
in_pop = "GHS_POP_2015"

## Input Built-Up Layer
in_built = "GHS_BUILT2014"

## Input Regional Extent Projection  Layer
in_region = "EBC_REG_DT_polygon"

#################################################################

## REPROJECT DATA LAYERS (tested)

## Reproject Accessibility Layer
arcpy.ProjectRaster_management(in_access, "region_access.tif",\
                               in_region, "BILINEAR")

## Reproject Population Layer
arcpy.ProjectRaster_management (in_pop, "region_pop.tif",\
			       in_region, "BILINEAR")

## Reproject Built-Up Layer
arcpy.ProjectRaster_management(in_built, "region_built.tif",\
                               in_region, "BILINEAR")

#################################################################

## CLIP DATASETS TO REGION EXTENT


#################################################################

## RECLASSIFY PIXELS (tested)

## POPULATION CLASSIFICATION
## Categorizes population parameter:
##  - 0 is uninhabited
##  - 1 is between 1 - 75 people / pixel
##  - 3 is between 75 - 374 people / pixel
##  - 5 is greater than 375 people / pixel
pop_rules = RemapRange([[0, 0, 0], [0, 74, 1], [74, 374, 3], [374, 3566, 5]])
pop_classes = Reclassify("region_pop.tif", "Value", pop_rules)

## BUILT-UP CLASSIFICATION
## Categorizes % built up:
##  - 0 is 0-50%
##  - 1 is 50-100%
bu_rules = RemapRange([[0, 0.49, 0], [0.49, 1, 1]])
bu_classes = Reclassify("region_built.tif", "Value", bu_rules)

## COMBINE OUTPUTS
## adds values from each "classes" layer:
##  - 0 is 0 pop and 0-49% built up
##  - 1-2 is RURAL or SUBURBAN
##  - 3-5 is potential URBAN CLUSTER
##  - 6 is potential URBAN CENTRE
pixel_classes = Raster("pop_classes") + Raster("bu_classes")

#################################################################

## DEFINE URBAN CENTERS

## ISOLATE URBAN CENTERS PIXELS
## Categorizes all urban center pixels, other classes are NODATA
ucenter_rules = RemapRange([[0, 5, 'NODATA'], [5, 6, 1]])
ucenter_pixels = Reclassify("pixel_classes", "Value", ucenter_rules)

## CREATE URBAN CENTER REGIONS
## Groups urban center pixels into regions
ucenter_pgroups = RegionGroup("ucenter_pixels", "FOUR", "WITHIN")

## DETERMINE REGIONS WITH > 50,000 POPULATION
## Sum population within regions
arcpy.SummarizeRasterWithin_ra('ucenter_pgroups', 'Value', 'region_pop',\
                               'ucenter_sum', 'SUM')

#################################################################

## REMOVE TEMPORARY FILES

#arcpy.Delete_management("region_access")
#arcpy.Delete_management("region_pop")
#arcpy.Delete_management("region_built")
arcpy.Delete_management("pop_classes")
arcpy.Delete_management("bu_classes")
arcpy.Delete_management("pixel_classes")
arcpy.Delete_management("ucenter_pixels")
