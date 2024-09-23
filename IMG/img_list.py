'''

# gallery/img_list.py

import os
from django.conf import settings

def get_images():
    image_folder = os.path.join(settings.MEDIA_ROOT, 'images')  # 使用 MEDIA_ROOT
    images = []
    try:
        for filename in os.listdir(image_folder):
            if filename.endswith('.png'):
                image_id = filename.split('.')[0]
                images.append({
                    'id': image_id,
                    'url': os.path.join(settings.MEDIA_URL, 'images', filename)
                })
    except FileNotFoundError:
        print(f"Error: The folder {image_folder} does not exist.")
    return images
'''