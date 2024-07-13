import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Access the table
table = dynamodb.Table('cloudresume-test')

def lambda_handler(event, context):
    try:
        # Get the item from the table
        response = table.get_item(
            Key={
                'id': '0'
            }
        )
        
        # Check if 'Item' exists in the response
        if 'Item' in response:
            views = response['Item']['views']
            views = views + 1
        else:
            # If the item does not exist, initialize views
            views = 1
        
        # Log the current view count
        logger.info(f"Current view count: {views}")

        # Update the item with the new views count
        table.put_item(Item={
            'id': '0',
            'views': views
        })

        return {
            'statusCode': 200,
            'body': views
        }
    
    except Exception as e:
        logger.error(f"Error updating views: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Error updating views'
        }
