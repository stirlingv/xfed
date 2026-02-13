import io
import shutil
import tempfile
import zipfile

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import IntakeFile, IntakeForm, IntakeSubmission
from .validators import (
    MAX_RESUME_FILE_SIZE_BYTES,
    normalize_and_validate_submission_email,
    validate_resume_upload,
)


class SubmissionValidationTests(TestCase):
    def _build_minimal_docx(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("[Content_Types].xml", "<Types></Types>")
            archive.writestr("word/document.xml", "<w:document></w:document>")
        return buffer.getvalue()

    def test_accepts_valid_pdf_resume(self):
        uploaded = SimpleUploadedFile(
            "resume.pdf",
            b"%PDF-1.7\n1 0 obj\n<<>>\n",
            content_type="application/pdf",
        )
        validate_resume_upload(uploaded)

    def test_rejects_unsupported_resume_extension(self):
        uploaded = SimpleUploadedFile(
            "resume.txt",
            b"plain text",
            content_type="text/plain",
        )
        with self.assertRaises(ValidationError):
            validate_resume_upload(uploaded)

    def test_rejects_spoofed_pdf_content(self):
        uploaded = SimpleUploadedFile(
            "resume.pdf",
            b"not really a pdf",
            content_type="application/pdf",
        )
        with self.assertRaises(ValidationError):
            validate_resume_upload(uploaded)

    def test_accepts_valid_docx_resume(self):
        uploaded = SimpleUploadedFile(
            "resume.docx",
            self._build_minimal_docx(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        validate_resume_upload(uploaded)

    def test_rejects_oversized_resume_file(self):
        oversized_content = b"%PDF-" + (b"0" * MAX_RESUME_FILE_SIZE_BYTES)
        uploaded = SimpleUploadedFile(
            "resume.pdf",
            oversized_content,
            content_type="application/pdf",
        )
        with self.assertRaises(ValidationError):
            validate_resume_upload(uploaded)

    def test_normalizes_valid_email(self):
        normalized = normalize_and_validate_submission_email("  Candidate@ExampleBusiness.com ")
        self.assertEqual(normalized, "candidate@examplebusiness.com")

    def test_rejects_disposable_email_domain(self):
        with self.assertRaises(ValidationError):
            normalize_and_validate_submission_email("candidate@mailinator.com")

    def test_rejects_placeholder_email_local_part(self):
        with self.assertRaises(ValidationError):
            normalize_and_validate_submission_email("test@realcompany.com")


class IntakeFileAdminPreviewTests(TestCase):
    def setUp(self):
        self.temp_media_root = tempfile.mkdtemp(prefix="xfed-test-media-")
        self.media_override = override_settings(MEDIA_ROOT=self.temp_media_root)
        self.media_override.enable()

        user_model = get_user_model()
        self.admin_user = user_model.objects.create_superuser(
            username="admin_preview",
            email="admin_preview@examplebusiness.com",
            password="strong-test-password",
        )
        self.client.force_login(self.admin_user)

        self.form = IntakeForm.objects.create(
            title="Resume Intake",
            slug="resume-intake",
            email_recipients="ops@examplebusiness.com",
            allow_file_uploads=True,
        )
        self.submission = IntakeSubmission.objects.create(
            form=self.form,
            data={"Email Address": "candidate@examplebusiness.com"},
        )
        self.uploaded_file = IntakeFile.objects.create(
            submission=self.submission,
            file=SimpleUploadedFile(
                "resume.pdf",
                b"%PDF-1.7\n1 0 obj\n<<>>\n",
                content_type="application/pdf",
            ),
            original_filename="resume.pdf",
        )

    def tearDown(self):
        self.media_override.disable()
        shutil.rmtree(self.temp_media_root, ignore_errors=True)

    def test_admin_preview_endpoint_returns_inline_content(self):
        url = reverse(
            "admin:main_intakesubmission_file_preview",
            args=[self.submission.pk, self.uploaded_file.pk],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("inline;", response["Content-Disposition"])
        self.assertEqual(response["Content-Type"], "application/pdf")


class IntakeFileCleanupTests(TestCase):
    def setUp(self):
        self.temp_media_root = tempfile.mkdtemp(prefix="xfed-cleanup-media-")
        self.media_override = override_settings(MEDIA_ROOT=self.temp_media_root)
        self.media_override.enable()

        self.form = IntakeForm.objects.create(
            title="Cleanup Intake",
            slug="cleanup-intake",
            email_recipients="ops@examplebusiness.com",
            allow_file_uploads=True,
        )

    def tearDown(self):
        self.media_override.disable()
        shutil.rmtree(self.temp_media_root, ignore_errors=True)

    def _create_submission_with_file(self, email, filename):
        submission = IntakeSubmission.objects.create(
            form=self.form,
            data={"Email Address": email},
        )
        intake_file = IntakeFile.objects.create(
            submission=submission,
            file=SimpleUploadedFile(
                filename,
                b"%PDF-1.7\n1 0 obj\n<<>>\n",
                content_type="application/pdf",
            ),
            original_filename=filename,
        )
        return submission, intake_file

    def test_deleting_intake_file_removes_blob_from_storage(self):
        _submission, intake_file = self._create_submission_with_file(
            "direct-delete@examplebusiness.com",
            "resume-direct.pdf",
        )
        storage = intake_file.file.storage
        file_name = intake_file.file.name

        self.assertTrue(storage.exists(file_name))
        intake_file.delete()
        self.assertFalse(storage.exists(file_name))

    def test_deleting_submission_removes_related_uploaded_blobs(self):
        submission, first_file = self._create_submission_with_file(
            "cascade-delete@examplebusiness.com",
            "resume-cascade-a.pdf",
        )
        second_file = IntakeFile.objects.create(
            submission=submission,
            file=SimpleUploadedFile(
                "resume-cascade-b.pdf",
                b"%PDF-1.7\n2 0 obj\n<<>>\n",
                content_type="application/pdf",
            ),
            original_filename="resume-cascade-b.pdf",
        )
        first_storage = first_file.file.storage
        second_storage = second_file.file.storage
        first_name = first_file.file.name
        second_name = second_file.file.name

        self.assertTrue(first_storage.exists(first_name))
        self.assertTrue(second_storage.exists(second_name))

        submission.delete()

        self.assertFalse(first_storage.exists(first_name))
        self.assertFalse(second_storage.exists(second_name))


class SetupHireXfedContentCommandTests(TestCase):
    def test_default_mode_preserves_existing_submissions(self):
        form = IntakeForm.objects.create(
            title="Existing Consultation",
            slug="client-consultation",
            email_recipients="team@examplebusiness.com",
            allow_file_uploads=True,
        )
        submission = IntakeSubmission.objects.create(
            form=form,
            data={"Email Address": "persist@examplebusiness.com"},
        )

        original_form_id = form.id
        original_submission_id = submission.id

        call_command("setup_hirexfed_content")

        self.assertTrue(IntakeSubmission.objects.filter(pk=original_submission_id).exists())
        self.assertEqual(IntakeSubmission.objects.count(), 1)
        self.assertEqual(
            IntakeForm.objects.get(slug="client-consultation").id,
            original_form_id,
        )

    def test_reset_mode_replaces_forms_and_cascades_submissions(self):
        form = IntakeForm.objects.create(
            title="Existing Consultation",
            slug="client-consultation",
            email_recipients="team@examplebusiness.com",
            allow_file_uploads=True,
        )
        IntakeSubmission.objects.create(
            form=form,
            data={"Email Address": "to-be-removed@examplebusiness.com"},
        )

        self.assertEqual(IntakeSubmission.objects.count(), 1)
        call_command("setup_hirexfed_content", reset=True, force=True)
        self.assertEqual(IntakeSubmission.objects.count(), 0)

    @override_settings(DEBUG=False)
    def test_reset_requires_force_when_debug_false(self):
        with self.assertRaises(CommandError):
            call_command("setup_hirexfed_content", reset=True)
