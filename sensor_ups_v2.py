import sys
import json
from state_ups_v2 import get_state_ups
# get CustomSensorResult from paepy package
from paepy.ChannelDefinition import CustomSensorResult

if __name__ == "__main__":
    # interpret first command line parameter as json object
    data = json.loads(sys.argv[1]) # get sys arg number port
    host = data['host'] # get ip host
    
    port = int(data.get('params', 2065)) # default port 2065
    result = CustomSensorResult("This sensor is monitoring UPS " + host)
    try:
        state_ups = get_state_ups(host=host, port=port) # get status UPS sistem through ttelnet connection
    
        # add primary channel
        result.add_channel(channel_name="Main voltage", unit="Custom", value=state_ups.main_voltage, is_float=True, primary_channel=True,
                        is_limit_mode=True, limit_min_error=10, limit_max_error=285, limit_min_warning=160, 
                        limit_error_msg="No main voltage")

        # add additional channel   
        result.add_channel(channel_name="Temperage", unit="Temperature", value=state_ups.temperature, is_float=True,
                        is_limit_mode=True, limit_min_error=5, limit_max_error=60,
                        limit_error_msg="Temperage too high")

        result.add_channel(channel_name="Charge battaries", unit="Percent", value=state_ups.charge_battery, is_float=True)

        result.add_channel(channel_name="Capasity_battery", unit="Percent", value=state_ups.capasity_battery, is_float=True)

        result.add_channel(channel_name="Working hours", unit="Custom", value=state_ups.working_hours, is_float=True)

        result.add_channel(channel_name="Load", unit="Custom", value=state_ups.load, is_float=True)

    except Exception:
        result.add_error("Connection Err")


    # print sensor result to std
    print(result.get_json_result())

  
