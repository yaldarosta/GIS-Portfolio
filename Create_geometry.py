#back up


#imports 
import csv 
import os
import arcpy
import traceback  # For detailed error reporting

# Add try-except for the main block of the script
try:
    info = arcpy.GetParameterAsText(0)

    # setting workspace 
    in_dirpt_gdb = r"Z:\GIST_8138\Module04\mod4_a01076641.gdb"  # workspace
    in_dirpt = "Z:\\GIST_8138\\Module04\\mod04-data\\"  # workspace
    csvFilept = "MVRDpoint2.csv"  # name of file provided
    fcpt = "MetroVan_Pts"  # name of shapefile that will be created 
    in_csvpt = os.path.join(in_dirpt, csvFilept)  # full path so script can find later
    srpt = arcpy.SpatialReference(4326)  # referencing the spatial coordinates (WGS 84)

    # setting up the output 
    arcpy.management.CreateFeatureclass(in_dirpt_gdb, fcpt, "POINT", csvFilept, "DISABLED", "DISABLED", srpt)
    out_feature_classpt = os.path.join(in_dirpt_gdb, fcpt)

    #commented out due to the above script creating the fields so the script below is unncessary. Just for future reference. 
    # Add fields 
    #arcpy.management.AddFields(out_feature_classpt, 
                              # [['name', 'TEXT', 'Name', 255, ''], 
                               # ['latitude', 'DOUBLE', 'Latitude', None, 15, ''],
                                #['longitude', 'DOUBLE', 'Longitude', None, 15, '']])

    with arcpy.da.InsertCursor(out_feature_classpt, ['SHAPE@', 'ID', 'Name', 'Latitude', 'Longitude']) as cursor:
        # empty point object to store xy
        point = arcpy.Point()

        with open(in_csvpt) as f:
            reader = csv.reader(f)
            next(reader)
            # read each line and write to shapefile
            for line in reader:
                try:
                    point.ID = int(line[0])  # you fill in the correct index number
                    point.X = float(line[3])  # you fill in the correct index number
                    point.Y = float(line[2])  # you fill in the correct index number
                    geom = arcpy.PointGeometry(point)
                    theName = str(line[1])  # you fill in the correct index number
                    cursor.insertRow((geom, point.ID, theName, point.Y, point.X))
                except Exception as e:
                    arcpy.AddMessage(f"Error processing line {line}: {e}")
                    arcpy.AddMessage("Detailed traceback:")
                    arcpy.AddMessage(traceback.format_exc())  # Prints the full traceback for debugging

except Exception as e:
    arcpy.AddMessage("An error occurred in the script:")
    arcpy.AddMessage(e)
    arcpy.AddMessage("Detailed traceback:")
    arcpy.AddMessage(traceback.format_exc())  # Prints the full traceback for debugging