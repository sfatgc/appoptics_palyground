#!/usr/bin/env python3
import argparse
import sys
import appoptics_metrics
import lib.config
import lib.data
import lib.charts


ctx = {
'data': None,
'charts': None
}


oArgParser = argparse.ArgumentParser(description="Setup AppOptics dashboard, charts, and submit probes data.")
oArgParser.add_argument("api_token",            help="The AppOptics API token.")
oArgParser.add_argument("-s", "--space_name",   help="The name of space to setup charts in (default is 'test_space')",              default='test_space')
oArgParser.add_argument("-c", "--charts_yaml",  help="YAML-formated charts description file path. (default is 'conf/charts.yaml')", default='conf/charts.yaml')
oArgParser.add_argument("-d", "--data_json",    help="Probes data JSON-file path. (default is 'data/probes.json')",                 default='data/probes.json')
oArgParser.add_argument("-S", "--submit_data",  help="Submit Probes data to AppOptics.", action="store_true")
oArgParser.add_argument("-C", "--setup_charts", help="Setup charts in AppOptics.",       action="store_true")
ctx['args'] = oArgParser.parse_args()

try:
    if ctx['args'].charts_yaml:
        ctx['charts'] = lib.config.load_config_file(ctx['args'].charts_yaml)
#
# Exit if we have to setup charts,
# and charts YAML-file is not available
#
except (FileNotFoundError, PermissionError) as E:
    print(str(E))
    if ctx['args'].setup_charts:
        exit(1)


try:
    if ctx['args'].data_json:
        ctx['data'] = lib.data.load_data_from_file(ctx['args'].data_json)
#
# Exit if we hve tu submit probes data,
# and data JSON-file is not available.
#
except (FileNotFoundError, PermissionError) as E:
    print(str(E))
    if ctx['args'].submit_data:
        exit(1)



#
# All data processing cycles have their own
# exception handling fo non-fatal errors
# to aviod whole process interrupt in case of
# malformed data item, rate limit firing, etc.
#
try:

    #
    # Setup API service connection, and authenticate against it
    #
    oApiConnection = appoptics_metrics.connect(ctx['args'].api_token)


    #
    # If charts data loaded uccessfully,
    # and we have to setup charts -
    # get the space, and perform setup
    #
    if ctx['charts'] and ctx['args'].space_name and ctx['args'].setup_charts:
        oSpace = oApiConnection.find_space(ctx['args'].space_name) or oApiConnection.create_space(ctx['args'].space_name)
        lib.charts.setup_charts(oApiConnection, oSpace, ctx['charts'])


    #
    # Perform submission, if probes data loaded successfully,
    # and we have to submit it
    #
    if ctx['data'] and ctx['args'].submit_data:
        lib.data.submit_data(oApiConnection, ctx['data'])


#
# In case of any API errors we have an error message to display
#
except appoptics_metrics.exceptions.ClientError as E:
    print(E.error_message)
    exit(1)

#
# In other cases just show what happened, and where
#
except Exception as E:
    import traceback
    traceback.print_exc()
    exit(1)
