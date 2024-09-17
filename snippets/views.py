from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from cryptography.fernet import Fernet, InvalidToken
from .models import Snippet
from .forms import SnippetForm
import base64
import hashlib

def derive_fernet_key(secret_key: str) -> bytes:
    """Derive a Fernet key from a user-provided secret key."""
   
    return base64.urlsafe_b64encode(hashlib.sha256(secret_key.encode()).digest())

def index(request):
    """Home page with form for creating snippets."""
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            secret_key = form.cleaned_data['secret_key']

            if secret_key:
                
                fernet_key = derive_fernet_key(secret_key)
                cipher_suite = Fernet(fernet_key)
                encrypted_text = cipher_suite.encrypt(text.encode())
                snippet = Snippet(content=encrypted_text, encrypted=True)
            else:
                snippet = Snippet(content=text.encode(), encrypted=False)

            snippet.save()
            return render(
                request,
                'index.html',  
                {'form': form, 'shareable_url': request.build_absolute_uri(f'/snippet/{snippet.id}/')}
            )

    else:
        form = SnippetForm()

    return render(request, 'index.html', {'form': form})  

def view_snippet(request, snippet_id):
    """View snippet page which handles decryption if needed."""
    snippet = get_object_or_404(Snippet, id=snippet_id)
    decrypted_text = None

    if request.method == 'POST':
        secret_key = request.POST.get('secret_key')
        if snippet.encrypted:
            try:
                
                fernet_key = derive_fernet_key(secret_key)
                cipher_suite = Fernet(fernet_key)
                decrypted_text = cipher_suite.decrypt(snippet.content).decode()
            except (InvalidToken, ValueError):
                return HttpResponse("Invalid Secret Key. Please try again.")
        else:
            decrypted_text = snippet.content.decode()

   
    context = {
        'snippet': snippet,
        'decrypted_text': decrypted_text if decrypted_text else None,
        'is_encrypted': snippet.encrypted,
    }

    return render(request, 'view_snippet.html', context)  