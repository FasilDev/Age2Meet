import os
from django.http import HttpResponse, Http404
from django.conf import settings

class MediaFilesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si c'est une requête pour un fichier media
        if request.path.startswith('/media/'):
            return self.serve_media_file(request)
        
        response = self.get_response(request)
        return response

    def serve_media_file(self, request):
        try:
            # Construire le chemin du fichier
            file_path = request.path[7:]  # Enlever '/media/'
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            if os.path.exists(full_path):
                with open(full_path, 'rb') as f:
                    content = f.read()
                
                # Déterminer le type de contenu
                if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif file_path.endswith('.png'):
                    content_type = 'image/png'
                elif file_path.endswith('.gif'):
                    content_type = 'image/gif'
                else:
                    content_type = 'application/octet-stream'
                
                response = HttpResponse(content, content_type=content_type)
                response['Content-Length'] = len(content)
                return response
            else:
                raise Http404("Media file not found")
                
        except Exception as e:
            raise Http404(f"Error serving media file: {e}")
