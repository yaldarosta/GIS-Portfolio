#--------------------------------------------------------------------------
# Point_Polygon.txt
# Author: Yalda Rostainajad 
# Student Number: a01076641
# Created on: March 5, 2025
# Usage: To determine the number of features within schools and neighborhoods
#--------------------------------------------------------------------------

import arcpy

# Define the Toolbox class
class Toolbox(object):
    def __init__(self):
        """Define the toolbox."""
        self.label = "Point to Polygon Toolbox"  # Toolbox name
        self.alias = "Point_Polygon"  # Alias for the toolbox

        # List of tools 
        self.tools = [PointtoPolygon]


# Define the PointtoPolygon tool
class PointtoPolygon(object):
    def __init__(self):
        """Define the tool."""
        self.label = "Point to Polygon"  # Tool name
        self.description = ""  # Tool description 
        self.canRunInBackground = False  # Tool cannot run in the background

    def getParameterInfo(self):
        """Define the input parameters for the tool."""
        
        # Input feature layer (polygon)
        feature_layer = arcpy.Parameter(
            displayName="Input Feature Layer",  # Label displayed in the tool interface
            name="feature_layer",  # Internal name
            datatype="Feature Layer",  # The type of data (feature layer)
            parameterType="Required",  # This parameter is required
            direction="Input"  # This parameter is an input to the tool
        )

        # Field from the input feature layer
        field_name = arcpy.Parameter(
            displayName="Field to Count",  # Label for the parameter
            name="field_name",  # Internal name
            datatype="Field",  # The type of data (field)
            parameterType="Required",  # This parameter is required
            direction="Input"  # This parameter is an input
        )

        field_name.parameterDependencies = [feature_layer.name]  # Field depends on feature layer input

        # Dropdown for unique value based on the selected field
        value_selection = arcpy.Parameter(
            displayName="Select Value",  # Label displayed in the tool interface
            name="value_selection",  # Internal name
            datatype="GPString",  # The type of data (string)
            parameterType="Required",  # This parameter is required
            direction="Input"  # This parameter is an input
        )
        
        # Set filter to create a value list for the dropdown
        value_selection.filter.type = "ValueList"
        value_selection.filter.list = []  # Empty list initially

        # Return the list of parameters
        return [feature_layer, field_name, value_selection]

    def isLicensed(self):
        """Check if the tool is licensed to run."""
        return True  # Tool is licensed

    def updateParameters(self, parameters):
        """Update the values of parameters before the tool runs."""
        if parameters[1].value:  # If a field is selected
            # Retrieve unique values from the field using a SearchCursor
            with arcpy.da.SearchCursor(parameters[0].valueAsText, parameters[1].valueAsText) as rows:
                # Populate the dropdown with unique values from the selected field
                parameters[2].filter.list = sorted(list(set([row[0] for row in rows])))

        else:
            # If no field is selected, clear the dropdown
            parameters[2].filter.list = []

        return

    def updateMessages(self, parameters):
        """Update the messages after internal validation."""
        return  # No custom message handling required

    def execute(self, parameters, messages):
        """Main execution logic of the tool."""
        
        # input values
        feature_layer = parameters[0].valueAsText
        selected_field = parameters[1].valueAsText
        selected_value = parameters[2].valueAsText

        # Build a query to select features based on the selected field and value
        query = f"{selected_field} = '{selected_value}'"

        # Count how many features taht match 
        feature_count = int(arcpy.management.GetCount(arcpy.management.SelectLayerByAttribute(feature_layer, "NEW_SELECTION", query)).getOutput(0))

        # Display how many features were found
        messages.addMessage(f"Found {feature_count} features matching the criteria.")

        if feature_count > 0:
            with arcpy.da.SearchCursor(feature_layer, [selected_field], query) as cursor:
                for row in cursor:
                    messages.addMessage(f"  - {row[0]}")  # Output the name of each feature

        return

    def postExecute(self, parameters):
        """Post-execution logic (after the tool runs)."""
        return 
