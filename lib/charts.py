import sys
import appoptics_metrics
import lib.exceptions

# Go through a aoChartList looking the
# chart with name equal asChartName
def find_chart(aoChartList, asChartName):
    for oChart in aoChartList:
        if oChart.name == asChartName:
            return oChart
    return None


# Update existing chart aochart in space aoSpace
# Raise an exception if required fields missing in
# chart configuration.
def update_chart(aoApi, aoSpace, aoChart, ahChartConfig):
    try:
        sChartName    = ahChartConfig['name']
        sChartType    = ahChartConfig['type']
        aChartStreams = ahChartConfig['streams']
    except KeyError as E:
        raise lib.exceptions.ChartConfigValidationError()

    print("Updating a chart %s in space %s" % (sChartName, aoSpace.name))
    return aoApi.update_chart(aoChart, space=aoSpace, type=sChartType, streams=aChartStreams)


# Create new chart in space aoSpace with configuration
# described by ahChartConfig hash.
# Raise exception if chart configuration miss any of the
# required fields.
def create_chart(aoApi, aoSpace, aaChartsArray, ahChartConfig):
    try:
        sChartName    = ahChartConfig['name']
        sChartType    = ahChartConfig['type']
        aChartStreams = ahChartConfig['streams']
    except KeyError as E:
        raise lib.exceptions.ChartConfigValidationError()
    print("Creating a chart %s in space %s" % (sChartName, aoSpace.name))
    return aaChartsArray.append(aoApi.create_chart(sChartName, space=aoSpace, type=sChartType, streams=aChartStreams))


# Setup charts described by aoChartsConfig array.
# Update existing, and create missing charts in space aoSpace.
# Handle exceptions to avoid job interruption on first
# malformed item, IO error.
def setup_charts(aoApiConnection, aoSpace, aaChartsConfig):
    aCharts = aoSpace.charts()
    for hChartConfig in aaChartsConfig:
        sChartName = hChartConfig['name']
        # Here we will try to find existing chart
        # with such name in charts array, and update it.
        # Or create a new one unless it already exists.
        try:
            oChart = find_chart(aCharts, sChartName)
            if oChart:
                update_chart(aoApiConnection, aoSpace, oChart,  hChartConfig)
            else:
                create_chart(aoApiConnection, aoSpace, aCharts, hChartConfig)
        except lib.exceptions.ChartConfigValidationError as E:
            print("Malformed chart in config: " + str(E))
        except appoptics_metrics.exceptions.ClientError as E:
            # Here I will just avoid breaking the whole script execution
            # in case of single unsuccessful chart operation.
            print("Exception caught in setup_charts: " + str(E))
