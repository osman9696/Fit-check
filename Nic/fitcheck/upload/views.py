import os
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import replicate  # External library for calling the API
import replicate
from django.conf import settings

# Example usage
replicate_client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)

# Upload Images View
def upload_images(request):
    if request.method == 'POST':
        # Get uploaded files
        garment_img = request.FILES.get('garment_img')
        human_img = request.FILES.get('human_img')
        description = request.POST.get('description', '')

        # Validate input
        if not garment_img or not human_img:
            return render(request, 'upload_form.html', {'error': 'Please upload both images.'})

        # Save images temporarily
        garment_path = default_storage.save('temp_garment_img.jpg', ContentFile(garment_img.read()))
        human_path = default_storage.save('temp_human_img.jpg', ContentFile(human_img.read()))

        garment_full_path = default_storage.path(garment_path)
        human_full_path = default_storage.path(human_path)

        try:
            # Call Replicate API
            output = replicate.run(
                "cuuupid/idm-vton:c871bb9b046607b680449ecbae55fd8c6d945e0a1948644bf2361b3d021d3ff4",
                input={
                    "garm_img": garment_full_path,
                    "human_img": human_full_path,
                    "garment_des": description,
                }
            )

            # Save API output as an image
            output_image_path = default_storage.save('output.jpg', ContentFile(output))

            # Clean up temporary files
            os.remove(garment_full_path)
            os.remove(human_full_path)

            # Render the result page
            return render(request, 'result.html', {'output_image': output_image_path})
        except Exception as e:
            return render(request, 'error.html', {'error': str(e)})

    return render(request, 'upload_form.html')  # Render the upload form

# Result View
def result(request):
    return render(request, 'result.html')
