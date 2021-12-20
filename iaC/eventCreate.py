import boto3
if __name__ == '__main__':
    event_client = boto3.client('events')
    lambda_client = boto3.client('lambda')
    lambda_arn = lambda_client.get_function(FunctionName='getWeatherData')['Configuration']['FunctionArn']


    event_client.put_rule(Name='weatherApiSchedule',
                                ScheduleExpression='rate(1 hour)',                                                                            
                                State='ENABLED')
    event_client.put_targets(Rule='weatherApiSchedule',
                                    Targets=[{'Arn': lambda_arn,
                                                'Id': '1'}])