def lambda_handler (event, context):
    temperature = event[ "temperature" ]
    voltage = event[ "voltage" ]
    if temperature > 100 or voltage < 5 :
        #do something
    else :
        #do nothing