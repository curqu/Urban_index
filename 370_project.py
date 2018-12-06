################## URBAN / SUBURBAN / RURAL INDEX ###############

## Import Modules:

import arcpy
from arcpy.sa import *

#################################################################

## VARIABLES (USER DEFINED)

#################################################################

## SET WORKSPACE:

arcpy.env.workspace = "c:/mydirectory/myworkingenvironment"

#################################################################

## INPUT LAYERS: (see README for appropriate inputs)

## Input Accessibility Layer
in_access = "clipped_projected_accessibility.tif"

## Input Population Layer
in_pop = "clipped_projected_population.tif"

## Input Built-Up Layer
in_built = "clipped_projected_builtup.tif"

#################################################################

## ACCESSIBILITY THRESHOLD (see README for appropriate Values)

suburban_thresh = 40

#################################################################

## RECLASSIFY PIXELS 

## POPULATION CLASSIFICATION
## Categorizes population parameter:
##  - 0 is uninhabited
##  - 1 is between 1 - 75 people / pixel
##  - 2 is between 75 - 374 people / pixel
##  - 3 is greater than 375 people / pixel
pop_rules = RemapRange([[0, 0.8, 0], [0.8, 74, 1], [74, 374, 2],
                        [374, 3566, 3]])
pop_classes = Reclassify(in_pop, "Value", pop_rules)
pop_classes.save("pop_classes")

## BUILT-UP CLASSIFICATION
## Categorizes % built up:
##  - 0  is 0-50%
##  - 10 is 50-100%
bu_rules = RemapRange([[0, 0.49, 0], [0.49, 1, 10]])
bu_classes = Reclassify(in_built, "Value", bu_rules)
bu_classes.save("bu_classes")

## COMBINE OUTPUTS FOR URBAN CENTER CLASSIFICATION
## adds values from each "classes" layer:
##  - 0 is 0 pop and 0-49% built up
##  - 1-2 is RURAL or SUBURBAN or URBAN CLUSTER
##  - >= 3 is potential URBAN CENTRE
pixel_classes = Raster("pop_classes") + Raster("bu_classes")
pixel_classes.save("pixel_classes")

#################################################################

## DEFINE URBAN CENTERS

## ISOLATE URBAN CENTERS PIXELS
## Categorizes all urban center pixels, other classes are NODATA
ucenter_rules = RemapRange([[0, 2, 'NODATA'], [2, 13, 1]])
ucenter_pixels = Reclassify("pixel_classes", "Value", ucenter_rules)
ucenter_pixels.save("ucenter_pixels.tif")

## CREATE URBAN CENTER REGIONS
## Groups urban center pixels into regions
ucenter_pgroups = RegionGroup("ucenter_pixels.tif", "FOUR", "WITHIN")
ucenter_pgroups.save("ucenter_pgroups.tif")

## DETERMINE REGIONS WITH > 50,000 POPULATION
## Convert regions to polygons in order to sum
arcpy.RasterToPolygon_conversion("ucenter_pgroups.tif",\
                                 "ucenter_poly",\
                                 "NO_SIMPLIFY", "VALUE")
## Fill gaps (all enclosed pixel areas are incorporated into polygons)
arcpy.Union_analysis(["ucenter_poly"],\
                     "ucenter_polyfill", "ALL",\
                     0.01, "NO_GAPS")
arcpy.Dissolve_management("ucenter_polyfill", "ucenter_polyfd", "", "", \
			  "SINGLE_PART")

## Convert population layer to integer type, build attribute table
arcpy.Int_3d("region_pop.tif", "rpop_int")

## Sum population over polygons
pop_sum_uce = ZonalStatistics("ucenter_polyfd", "FID",\
                          "rpop_int", "SUM", "NODATA")
pop_sum_uce.save("pop_sum_uce")

## Reclassify summed population raster:
## - 0 = less than 50,000
## - 4 = 50,000 or more
uce_rules = RemapRange([[0,49999,0],[50000, 10000000, 4]])
ucenter_class = Reclassify ("pop_sum_uce", "Value", uce_rules)
ucenter_class.save("ucenter_class")

## Set urban center pixels to null in pop_class layer
con_uce = Con(IsNull("ucenter_class"),0, "ucenter_class")
con_uce.save("con_uce")
forucl_mod = SetNull ("con_uce", "pop_classes", "VALUE = 4")
forucl_mod.save("forucl_mod")

#################################################################

## DEFINE URBAN CLUSTERS

## ISOLATE URBAN CLUSTER PIXELS 
## Categorizes all urban cluster pixels, other classes are NODATA
ucluster_rules = RemapRange([[0, 1, 'NODATA'], [2, 3, 1]])
ucluster_pixels = Reclassify("forucl_mod", "Value", ucluster_rules)
ucluster_pixels.save("ucluster_pixels.tif")

## CREATE URBAN CLUSTER REGIONS
## Groups urban cluster pixels into regions
ucluster_pgroups = RegionGroup("ucluster_pixels.tif", "EIGHT", "WITHIN")
ucluster_pgroups.save("ucluster_pgroups.tif")

## DETERMINE REGIONS WITH > 5,000 POPULATION
## Convert regions to polygons in order to sum
arcpy.RasterToPolygon_conversion("ucluster_pgroups.tif",\
                                 "ucluster_poly",\
                                 "NO_SIMPLIFY", "VALUE")
## Sum population over polygons
pop_sum_ucl = ZonalStatistics("ucluster_poly", "FID",\
                          "rpop_int", "SUM", "NODATA")
pop_sum_ucl.save("pop_sum_ucl")

## Reclassify summed population raster:
## - 0 = less than 5,000
## - 3 = 5,000 or more
ucl_rules = RemapRange([[0,4999,0],[5000, 10000000, 3]])
ucluster_class = Reclassify ("pop_sum_ucl", "Value", ucl_rules)
ucluster_class.save("ucluster_class.tif")

## Set urban cluster pixels to null in pixel_class layer
con_ucl = Con(IsNull("ucluster_class.tif"),0, "ucluster_class.tif")
con_ucl.save("con_ucl")
forrs_mod = SetNull ("con_ucl", "forucl_mod", "VALUE = 3")
forrs_mod.save("forrs_mod")

#################################################################

## DEFINE RURAL / SUBURBAN

## ISOLATE RURAL/SUBURBAN PIXELS 
## Categorizes all rural and suburban pixels, other classes are NODATA
rs_rules = RemapRange([[0, 0, 'NODATA'], [1, 3, 1]])
rs_pixels = Reclassify("forrs_mod", "Value", rs_rules)
rs_pixels.save("rs_pixels")

## RESAMPLE ACCESSIBILITY LAYER
## Changes accessibility layer to 250m cells
arcpy.Resample_management (in_access, "access_250", 250, \
			   "NEAREST")

## CLASSIFY SUBURBAN AND RURAL
## Changes value of pixels within accessibility threshold
## - 1 = RURAL
## - 2 = SUBURBAN
sub_class = (Raster("access_250") < suburban_thresh ) & ( Raster("rs_pixels") == 1)
sub_class.save("sub_class")
subrur_class = (Raster("sub_class") + 1)
subrur_class.save("subrur_class")

## CLASSIFY UNINHABITED
## Sets all Remaining Pixels to 0
con_sr = Con(IsNull("subrur_class"),0, "subrur_class")
con_sr.save("con_sr")
			 
#################################################################

## COMBINE CLASSES INTO A SINGLE RASTER FILE

## ADD VALUES IN EACH con CLASS LAYER
## sum all values to produce a raster where:
##  - 0 is uninhabited
##  - 1 is rural
##  - 2 is suburban
##  - 3 is urban cluster
##  - 4 is urban center
settlement_index = (Raster("con_sr") + Raster("con_ucl") + Raster("con_uce"))

## SAVE OUTPUT 
settlement_index.save('settlement_index.tif')

##################################################################

## REMOVE TEMPORARY FILES

arcpy.Delete_management("pop_classes")
arcpy.Delete_management("bu_classes")
arcpy.Delete_management("pixel_classes")
arcpy.Delete_management("ucenter_pixels.tif")
arcpy.Delete_management("ucenter_pgroups.tif")
arcpy.Delete_management("ucenter_poly")
arcpy.Delete_management("ucenter_polyfill")
arcpy.Delete_management("rpop_int")                       
arcpy.Delete_management("ucenter_polyfd")
arcpy.Delete_management("pop_sum_uce")
arcpy.Delete_management("ucenter_class") 
arcpy.Delete_management("con_uce") 
arcpy.Delete_management("forucl_mod") 
arcpy.Delete_management("ucluster_pixels.tif") 
arcpy.Delete_management("ucluster_pgroups.tif") 
arcpy.Delete_management("ucluster_poly") 
arcpy.Delete_management("pop_sum_ucl") 
arcpy.Delete_management("ucluster_class.tif") 
arcpy.Delete_management("con_ucl") 
arcpy.Delete_management("forrs_mod") 
arcpy.Delete_management("rs_pixels") 
arcpy.Delete_management("access_250")
arcpy.Delete_management("sub_class") 
arcpy.Delete_management("subrur_class") 
arcpy.Delete_management("con_sr")
