from pathlib import Path
import zipfile

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


MAX_RESUME_FILE_SIZE_MB = 5
MAX_RESUME_FILE_SIZE_BYTES = MAX_RESUME_FILE_SIZE_MB * 1024 * 1024
MAX_FILES_PER_SUBMISSION = 5

RESUME_FILE_ACCEPT_ATTRIBUTE = ".pdf,.doc,.docx"
ALLOWED_RESUME_EXTENSIONS = {".pdf", ".doc", ".docx"}
ALLOWED_RESUME_EXTENSIONS_DISPLAY = "PDF, DOC, DOCX"

ALLOWED_MIME_TYPES_BY_EXTENSION = {
    ".pdf": {
        "application/pdf",
        "application/x-pdf",
    },
    ".doc": {
        "application/msword",
        "application/doc",
        "application/vnd.ms-word",
        "application/octet-stream",
    },
    ".docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/zip",
        "application/x-zip-compressed",
        "application/octet-stream",
    },
}

DISPOSABLE_OR_TEST_EMAIL_DOMAINS = {
    "example.com",
    "example.net",
    "example.org",
    "mailinator.com",
    "guerrillamail.com",
    "sharklasers.com",
    "10minutemail.com",
    "temp-mail.org",
    "tempmail.com",
    "trashmail.com",
    "yopmail.com",
    "maildrop.cc",
    "getnada.com",
}

PLACEHOLDER_LOCAL_PARTS = {
    "test",
    "testing",
    "fake",
    "example",
    "noreply",
    "no-reply",
}

_DOC_SIGNATURE = b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1"


def normalize_and_validate_submission_email(value):
    """Normalize and validate a user-submitted email address."""
    email = (value or "").strip().lower()
    if not email:
        raise ValidationError("Email address is required.")

    if len(email) > 254:
        raise ValidationError("Email address is too long.")

    validate_email(email)

    if ".." in email:
        raise ValidationError("Please enter a valid email address.")

    local_part, _, domain = email.partition("@")
    if not local_part or not domain:
        raise ValidationError("Please enter a valid email address.")

    if domain in DISPOSABLE_OR_TEST_EMAIL_DOMAINS:
        raise ValidationError("Please use a permanent email address.")

    if local_part in PLACEHOLDER_LOCAL_PARTS:
        raise ValidationError("Please enter your real email address.")

    return email


def validate_resume_upload(uploaded_file):
    """
    Validate uploaded resume files using extension, MIME type, and magic bytes.
    This prevents extension spoofing (e.g., `malware.exe` renamed to `.pdf`).
    """
    extension = Path((uploaded_file.name or "")).suffix.lower()
    if extension not in ALLOWED_RESUME_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file format. Allowed formats: {ALLOWED_RESUME_EXTENSIONS_DISPLAY}."
        )

    if uploaded_file.size > MAX_RESUME_FILE_SIZE_BYTES:
        raise ValidationError(
            f'File "{uploaded_file.name}" is too large. '
            f"Maximum size is {MAX_RESUME_FILE_SIZE_MB}MB."
        )

    content_type = (getattr(uploaded_file, "content_type", "") or "").lower()
    allowed_mime_types = ALLOWED_MIME_TYPES_BY_EXTENSION[extension]
    if content_type and content_type not in allowed_mime_types:
        raise ValidationError(
            f'File "{uploaded_file.name}" does not match the expected file type.'
        )

    if not _file_signature_matches_extension(uploaded_file, extension):
        raise ValidationError(
            f'File "{uploaded_file.name}" content does not match its extension.'
        )


def _file_signature_matches_extension(uploaded_file, extension):
    if extension == ".pdf":
        return _is_pdf(uploaded_file)
    if extension == ".doc":
        return _is_doc(uploaded_file)
    if extension == ".docx":
        return _is_docx(uploaded_file)
    return False


def _is_pdf(uploaded_file):
    uploaded_file.seek(0)
    header = uploaded_file.read(5)
    uploaded_file.seek(0)
    return header == b"%PDF-"


def _is_doc(uploaded_file):
    uploaded_file.seek(0)
    header = uploaded_file.read(8)
    uploaded_file.seek(0)
    return header == _DOC_SIGNATURE


def _is_docx(uploaded_file):
    uploaded_file.seek(0)
    zip_signature = uploaded_file.read(4)
    uploaded_file.seek(0)
    if zip_signature != b"PK\x03\x04":
        return False

    try:
        with zipfile.ZipFile(uploaded_file) as zip_file:
            return "word/document.xml" in zip_file.namelist()
    except zipfile.BadZipFile:
        return False
    finally:
        uploaded_file.seek(0)
