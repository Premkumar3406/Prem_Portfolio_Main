import os
import json
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from home.models import ContactMessage, Resume, Project


def About_Page(request):
    return HttpResponse("Hello World !")


def shopping_page(request):
    data = {"city": "Hyderabad"}
    return JsonResponse(data)


# html pages
def showing_html(request):
    projects = Project.objects.filter(is_active=True).order_by('order', '-created_at')
    return render(request, "home.html", {"projects": projects})


def download_resume(request):
    """
    Serves the resume PDF as a direct download.
    Checks for any active resume uploaded via Django Admin first,
    then falls back to static/files/Prem_Kumar_Resume.pdf.
    """
    # 1. Check for active database-uploaded resume
    active_resume = Resume.objects.filter(is_active=True).first()
    if active_resume and active_resume.file:
        try:
            if os.path.exists(active_resume.file.path):
                filename = os.path.basename(active_resume.file.name)
                return FileResponse(
                    open(active_resume.file.path, 'rb'),
                    as_attachment=True,
                    filename=filename,
                    content_type='application/pdf'
                )
        except Exception:
            pass

    # 2. Check static/files/Prem_Kumar_Resume.pdf
    fallback_path = settings.BASE_DIR / 'static' / 'files' / 'Prem_Kumar_Resume.pdf'
    if os.path.exists(fallback_path):
        return FileResponse(
            open(fallback_path, 'rb'),
            as_attachment=True,
            filename='Prem_Kumar_Resume.pdf',
            content_type='application/pdf'
        )

    return HttpResponse("Resume file is currently unavailable. Please contact directly.", status=404)


@require_http_methods(["POST"])
def contact_view(request):
    # Support both form data and JSON data
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            return JsonResponse({"status": "error", "message": "Invalid JSON data provided."}, status=400)
    else:
        data = request.POST

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('type', data.get('subject', 'General Inquiry')).strip()
    message = data.get('message', '').strip()

    errors = []
    if not name:
        errors.append("Please enter your name.")
    if not email:
        errors.append("Please enter your email address.")
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Please provide a valid email address.")

    if not message or len(message) < 6:
        errors.append("Please enter a message of at least 6 characters.")

    if errors:
        return JsonResponse({"status": "error", "message": " ".join(errors)}, status=400)

    try:
        # Save directly to database
        msg_obj = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject or 'General Inquiry',
            message=message
        )

        # Attempt email notification (fails silently if mailer is console or not configured)
        try:
            send_mail(
                subject=f"[Portfolio Contact] {subject} from {name}",
                message=f"Name: {name}\nEmail: {email}\nInterest: {subject}\n\nMessage:\n{message}\n\nReceived: {msg_obj.created_at}",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@portfolio.local'),
                recipient_list=['premkumar@example.com'],
                fail_silently=True
            )
        except Exception:
            pass

        return JsonResponse({
            "status": "success",
            "message": f"Thank you, {name}! Your message has been received successfully. I will get back to you soon!"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": "An error occurred while saving your message. Please try again."
        }, status=500)