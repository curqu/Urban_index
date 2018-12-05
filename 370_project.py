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

## ACCESSIBILITY THRESHOLD (see README for appropriate Values)

suburban_thresh = 40

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

## RECLASSIFY PIXELS 

## POPULATION CLASSIFICATION
## Categorizes population parameter:
##  - 0 is uninhabited
##  - 1 is between 1 - 75 people / pixel
##  - 2 is between 75 - 374 people / pixel
##  - 3 is greater than 375 people / pixel
pop_rules = RemapRange([[0, 0.8, 0], [0, 74, 1], [74, 374, 2],
                        [374, 3566, 3]])
pop_classes = Reclassify("region_pop.tif", "Value", pop_rules)

## BUILT-UP CLASSIFICATION
## Categorizes % built up:
##  - 0  is 0-50%
##  - 10 is 50-100%
bu_rules = RemapRange([[0, 0.49, 0], [0.49, 1, 10]])
bu_classes = Reclassify("region_built.tif", "Value", bu_rules)

## COMBINE OUTPUTS FOR URBAN CENTER CLASSIFICATION
## adds values from each "classes" layer:
##  - 0 is 0 pop and 0-49% built up
##  - 1-2 is RURAL or SUBURBAN or URBAN CLUSTER
##  - >= 3 is potential URBAN CENTRE
pixel_classes = Raster("pop_classes") + Raster("bu_classes")

#################################################################

## DEFINE URBAN CENTERS (tested)***

## ISOLATE URBAN CENTERS PIXELS *** EDIT TO "OR" CASE
## Categorizes all urban center pixels, other classes are NODATA
ucenter_rules = RemapRange([[0, 2, 'NODATA'], [2, 13, 1]])
ucenter_pixels = Reclassify("pixel_classes", "Value", ucenter_rules) #check if rules correct!

## CREATE URBAN CENTER REGIONS
## Groups urban center pixels into regions
ucenter_pgroups = RegionGroup("ucenter_pixels", "FOUR", "WITHIN")

## DETERMINE REGIONS WITH > 50,000 POPULATION
## Convert regions to polygons in order to sum
arcpy.RasterToPolygon_conversion("ucenter_pgroups",\
                                 "ucenter_poly",\
                                 "NO_SIMPLIFY", "VALUE")
## Fill gaps (all enclosed pixel areas are incorporated into polygons)
arcpy.Union_analysis(["ucenter_poly"],\
                     "ucenter_polyfill", "ALL",\
                     0.01, "NO_GAPS")
arcpy.Dissolve_management("ucenter_polyfill", "ucenter_polyfd", "", "", \
			  "SINGLE_PART")

## Convert population layer to integer type, build attribute table
arcpy.Int_3d("region_pop.tif", "region_pop_int")

## Sum population over polygons
pop_sum_uce = ZonalStatistics("ucenter_polyfd", "OBJECTID",\
                          "region_pop_int", "SUM", "NODATA")

## Reclassify summed population raster:
## - 0 = less than 50,000
## - 4 = 50,000 or more
rules = RemapRange([[0,49999,0],[50000, 10000000, 4]])
ucenter_class = Reclassify ("pop_sum_uce", "Value", rules)


## Set urban center pixels to null in pop_class layer
con_uce = Con(IsNull("ucenter_class"),0, "ucenter_class")
forucl_mod = SetNull ("con_uce", "pop_classes", "VALUE = 4")

#################################################################

## DEFINE URBAN CLUSTERS (tested) ***

## ISOLATE URBAN CLUSTER PIXELS 
## Categorizes all urban cluster pixels, other classes are NODATA
ucluster_rules = RemapRange([[0, 1, 'NODATA'], [2, 3, 1]])
ucluster_pixels = Reclassify("forucl_mod", "Value", ucluster_rules)

## CREATE URBAN CLUSTER REGIONS
## Groups urban cluster pixels into regions
ucluster_pgroups = RegionGroup("ucluster_pixels", "EIGHT", "WITHIN")

## DETERMINE REGIONS WITH > 5,000 POPULATION
## Convert regions to polygons in order to sum
arcpy.RasterToPolygon_conversion("ucluster_pgroups",\
                                 "ucluster_poly",\
                                 "NO_SIMPLIFY", "VALUE")
## Sum population over polygons
pop_sum_ucl = ZonalStatistics("ucluster_poly", "OBJECTID",\
                          "region_pop_int", "SUM", "NODATA")

## Reclassify summed population raster:
## - 0 = less than 5,000
## - 3 = 5,000 or more
rules = RemapRange([[0,4999,0],[5000, 10000000, 3]])
ucluster_class = Reclassify ("pop_sum_ucl", "Value", rules)

## Set urban cluster pixels to null in pixel_class layer
con_ucl = Con(IsNull("ucluster_class"),0, "ucluster_class")
forrs_mod = SetNull ("con_ucl", "forucl_mod", "VALUE = 3")

#################################################################

## DEFINE RURAL / SUBURBAN

## ISOLATE RURAL/SUBURBAN PIXELS 
## Categorizes all rural and suburban pixels, other classes are NODATA
rs_rules = RemapRange([[0, 0, 'NODATA'], [1, 3, 1]])
rs_pixels = Reclassify("forrs_mod", "Value", rs_rules)

## RESAMPLE ACCESSIBILITY LAYER
## Changes accessibility layer to 250m cells
arcpy.Resample_management ("region_access.tif", "access_250", 250, \
			   "NEAREST")

## CLASSIFY SUBURBAN AND RURAL
## Changes value of pixels within accessibility threshold
## - 1 = RURAL
## - 2 = SUBURBAN
sub_class = (Raster("access_250") < suburban_thresh ) & ( Raster("rs_pixels") == 1)
addrur_class = (Raster("sub_class") + 1)

## CLASSIFY UNINHABITED
## Sets all Remaining Pixels to 0
unin_rules = RemapRange([[0,0,0], [1,3, 'NODATA']])
unin_class = Reclassify("forrs_mod", "Value", unin_rules)
			 
#################################################################

## MOSAIC RESULTS ##UNTESTED
# urban center layer is con_uce (nodata is 0) or ucenter_class (has nodata)
# urban cluster layer is con_ucl (nodata is 0) or ucluster_class (has nodata)
# suburban/rural layer is subrur_class (nodata is 0) OR...
arcpy.MosaicToNewRaster_management("subrur_class;ucluster_class;ucenter_class;u\
				   nin_class","c:/temp/370_test1",\
				   "human_settlement_index.tif", "","","","1",\
				   "MAXIMUM","MATCH")		 	

##################################################################

## REMOVE TEMPORARY FILES

arcpy.Delete_management("region_access")
arcpy.Delete_management("region_pop")
arcpy.Delete_management("region_built")
arcpy.Delete_management("pop_classes")
arcpy.Delete_management("bu_classes")
arcpy.Delete_management("pixel_classes")
arcpy.Delete_management("ucenter_pixels")
arcpy.Delete_management("ucenter_pgroups")
arcpy.Delete_management("ucenter_poly")
arcpy.Delete_management("ucenter_polyfill")
arcpy.Delete_management("region_pop_int")                       
arcpy.Delete_management("ucenter_polyfd")
arcpy.Delete_management("pop_sum_uce")
arcpy.Delete_management("ucenter_class") 
arcpy.Delete_management("con_uce") 
arcpy.Delete_management("forucl_mod") 
arcpy.Delete_management("ucluster_pixels") 
arcpy.Delete_management("ucluster_pregroups") 
arcpy.Delete_management("ucluster_poly") 
arcpy.Delete_management("pop_sum_ucl") 
arcpy.Delete_management("ucluster_class") 
arcpy.Delete_management("con_ucl") 
arcpy.Delete_management("forrs_mod") 
arcpy.Delete_management("rs_pixels") 
arcpy.Delete_management("access_250")
arcpy.Delete_management("sub_class") 
arcpy.Delete_management("subrur_class") 
arcpy.Delete_management("uninclass")
