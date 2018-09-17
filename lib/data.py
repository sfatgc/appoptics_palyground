import json
import appoptics_metrics

def load_data_from_file(sFileName):
    with open(sFileName, "r") as oDataFile:
        return json.load(oDataFile)

def submit_data(aoApiConnection, ahData):
    with aoApiConnection.new_queue(auto_submit_count=1000) as oQueue:
        for sTimestamp in ahData:
            # Handle any exceptions in probe enqueuing
            # Excetions on invalid probe data will be
            # handled inside probes cycle instead.
            try:
                aProbes = ahData[sTimestamp]
                for hProbe in aProbes:
                    # This block should catch only errors on
                    # probe missing required fields.
                    try:
                        fValue  = hProbe['sample_ms']
                        sSource = hProbe['source']
                        sTarget = hProbe['target']
                        oQueue.add('sample_ms', fValue, time=sTimestamp, tags={'source': sSource, 'target': sTarget})
                    except KeyError as E:
                        print("Malformed probe in probes stream: " + str(E))
                    except appoptics_metrics.exceptions.ClientError as E:
                        # 429 code means we are rate limited by the API service
                        if E.code == 429:
                            print("Rate limited while enqueuing.\nTrying resubmit queue after timeout.\n\n" + str(E))
                            sleep(5)
                            oQueue.submit()
                        else:
                            print("Some 4xx error got while submitting queue:\n\n" + str(E))
            # Here we go only after handling same exception's 429 response
            # in inner cycle, if timeout wasn't enough to pass rate limit.
            except appoptics_metrics.exceptions.ClientError as E:
                print("No luck with resubmitting queue after been rate limited by API service. " + str(E))
            except Exception as E:
                print("Exception caught while processing probes couple in submit_data: " + str(E))
