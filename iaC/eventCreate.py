import boto3
if __name__ == '__main__':
    # connect to event bridge and lambda clients
    event_client = boto3.client('events')
    lambda_client = boto3.client('lambda')
    # get lambda arn
    lambda_arn = lambda_client.get_function(FunctionName='getWeatherData')['Configuration']['FunctionArn']

    # set one hour schedule event
    event_response = event_client.put_rule(Name='weatherApiSchedule',
                                ScheduleExpression='rate(1 hour)',                                                                            
                                State='ENABLED')
    event_client.put_targets(Rule='weatherApiSchedule',
                                    Targets=[{'Arn': lambda_arn,
                                                'Id': '1'}])
    lambda_client.add_permision(
        FunctionName=lambda_arn,
        StatementId='addPermisionForEventBridge',
        Action='lambda:InvokeFunction',
        Principal='events.amazonaws.com',
        SourceArn=event_response['RuleArn']
    )