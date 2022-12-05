import json
import boto3
import urllib.parse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

print('Loading function')

s3=boto3.client('s3')

def lambda_handler(event, context):
    bucket=event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(bucket)
    print(key)
    imgin=BytesIO()
    s3.download_fileobj(bucket,key,imgin)
    image=Image.open(imgin)
    font = ImageFont.load_default()
    image_draw = ImageDraw.Draw(image)  
    image_draw.text((10, 10), 'SAMPLESAMPLESAMPLESAMPLESAMPLESAMPLE', font=font, fill=(255,255,255,120))#可变化字体位置，字体深浅
    imgout=BytesIO()
    image.save(imgout,format=image.format,quality=95,subsampling=0)
    imgout.seek(0)
    s3.upload_fileobj(imgout,bucket,key,ExtraArgs={'ACL': 'public-read'})
