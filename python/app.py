import boto3
import botocore.config
import json

from datetime import datetime

def descripcion_generate_using_bedrock(descripciontopic:str)-> str:
    prompt=f"""<s>[INST]Human: Write a 100 words descripcion on the topic {descripciontopic} in Spanish
    Assistant:[/INST]
    """

    body={
        "prompt":prompt,
        "max_gen_len":512,
        "temperature":0.5,
        "top_p":0.9
    }

    try:
        bedrock=boto3.client("bedrock-runtime",region_name="us-east-1",
                             config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3}))
        response=bedrock.invoke_model(body=json.dumps(body),modelId="meta.llama2-13b-chat-v1")

        response_content=response.get('body').read()
        response_data=json.loads(response_content)
        print(response_data)
        descripcion_details=response_data['generation']
        return descripcion_details
    except Exception as e:
        print(f"Error generating the descripcion:{e}")
        return ""

def save_descripcion_details_s3(s3_key,s3_bucket,generate_descripcion):
    s3=boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body =generate_descripcion )
        print("Code saved to s3")

    except Exception as e:
        print("Error when saving the code to s3")



def lambda_handler(event, context):
    # TODO implement
    event=json.loads(event['body'])
    descripciontopic=event['descripcion_topic']

    generate_descripcion=descripcion_generate_using_bedrock(descripciontopic=descripciontopic)

    if generate_descripcion:
        current_time=datetime.now().strftime('%H%M%S')
        s3_key=f"descripcion-output/{current_time}.txt"
        s3_bucket='aws_bedrock_course1'
        save_descripcion_details_s3(s3_key,s3_bucket,generate_descripcion)


    else:
        print("No descripcion was generated")

    return{
        'statusCode':200,
        'body':json.dumps('Blog Generation is completed')
    }
