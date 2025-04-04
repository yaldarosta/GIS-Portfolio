#a01076641
#Yalda Rostainajad
#the purpose of this script is to query the pogram to select provinces in the canadian prarie
#using the census 2021 data, this script will find the population of the 2021 census data 
#and the private dwellings in each prairies from the 2021 census data. Once that is done, a script 
#will run where it will reference the 2021 census data SRID/ geom data then export a pdf layout. 

# reset all variables in the notebook
%reset -f

# import ArcPy site package
import arcpy

# Set data
# data added from the Living Atlas
lyr = "Province_21"

# Get layer object from current project
aprx = arcpy.mp.ArcGISProject('Current')
Province_21 = aprx.listMaps()[0].listLayers(lyr)[0]

chartbar = arcpy.charts.Bar(x='PRNAME', y='Population2021', 
                     title="Population by Province",
                     xTitle="Province", yTitle="Population",
                     dataSource= Province_21)


# Show the chart in the cell output
chartbar

# add the chart to the layer 
chartbar.addToLayer(Province_21)

chartbar = arcpy.charts.Bar(x='PRNAME', y='TotPrivDwellings2021', 
                     title="Total Dwelling by Province",
                     xTitle="Province", yTitle="Total Dwelling",
                     dataSource= Province_21)

# add the chart to the layer 
chartbar.addToLayer(Province_21)

# select the prarie provinces
ne = arcpy.management.SelectLayerByAttribute("Province_21", "NEW_SELECTION", 
                                             "PRNAME = 'Alberta' Or PRNAME = 'Saskatchewan' Or PRNAME = 'Manitoba'")

# Summarize prairie provinces 
with arcpy.da.SearchCursor(lyr, ["Population2021", "SHAPE@"]) as rows:
    pop, geoms = 0, arcpy.Array()
    for row in rows:
        population = row[0]
        polygons = row[1]
        
        pop += population
        for polygon in polygons:
            geoms.append(polygon)  # Indentation fixed
    geom = arcpy.Polygon(geoms)

# summarize the private dwellings 
with arcpy.da.SearchCursor(lyr, ["TotPrivDwellings2021", "SHAPE@"]) as rows:
    dwellings, geoms = 0, arcpy.Array()
    for row in rows:
        dwellings += row[0]

# display the total population for Prarie provinces
print(f"Population:{pop:> 19,}")
print(f"Area (sq. mi):{geom.getArea('PLANAR', 'SQUAREMILES'):> 15,.0f}")
# display the outline onthe praries
geom

# Create a feature class with a spatial reference of GCS WGS 1984
result = arcpy.management.CreateFeatureclass(
    arcpy.env.scratchGDB, "Praries", "POLYGON", spatial_reference=3857 )
feature_class = result[0]

# Write feature to new feature class
with arcpy.da.InsertCursor(feature_class, ["SHAPE@"]) as cursor:
    cursor.insertRow([geom])

# find path to open project
print("Project open: ", aprx.filePath)

# display the plot of PRIVATE DWELLINGS in a notebook cell
%matplotlib inline
 
# Import libaries
import matplotlib.pyplot as plt
import pandas as pd
import arcgis
 
# Create spatially enabled data frame (SEDF)
sedf = pd.DataFrame.spatial.from_featureclass("Province_21")
 
# Create plot
plt.bar(sedf.PRNAME, sedf.TotPrivDwellings2021)
 
# Update plot elements
plt.suptitle("Private Dwellings by in the Praries", fontsize=28)
plt.ylabel("Private Dwellings (in millions)")
plt.xticks(rotation=45)
 

#save the graph as an image
plt.savefig(r"Z:\GIST_8138\Module02\M02_a01076641\privprovplot2.png")

# Draw the plot
plt.show()

# display the plot of POPULATION IN PROVINCES in a notebook cell
%matplotlib inline
 
# Import libaries
import matplotlib.pyplot as plt
import pandas as pd
import arcgis
 
# Create spatially enabled data frame (SEDF)
sedf = pd.DataFrame.spatial.from_featureclass("Province_21")
 
# Create plot
plt.bar(sedf.PRNAME, sedf.Population2021)
 
# Update plot elements
plt.suptitle("Populations in the Praries", fontsize=28)
plt.ylabel("Population in 2021 (in millions)")
plt.xticks(rotation=45)
 

#save the graph as an image
plt.savefig(r"Z:\GIST_8138\Module02\M02_a01076641\popofprariesPLOT.png")

# Draw the plot
plt.show()

# Reference the layout
lyt = aprx.listLayouts("Layout1")[0]

# esport to PDF - use your path
lyt.exportToPDF(r"Z:\GIST_8138\Module02\M02_a01076641\Lab2_a01076641.pdf")


