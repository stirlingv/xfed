import io
import shutil
import tempfile
import zipfile
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import IntakeField, IntakeFile, IntakeForm, IntakeSubmission
from .validators import (
    HONEYPOT_FIELD_NAME,
    INTAKE_RATE_LIMIT_MAX_SUBMISSIONS,
    MAX_RESUME_FILE_SIZE_BYTES,
    normalize_and_validate_submission_email,
    validate_resume_upload,
)
from .views import send_intake_notification


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


class SlackNotificationTests(TestCase):
    def _build_submission_payload(self, form_slug, form_title):
        form = IntakeForm.objects.create(
            title=form_title,
            slug=form_slug,
            allow_file_uploads=True,
        )
        submission = IntakeSubmission.objects.create(
            form=form,
            data={"Email Address": "candidate@examplebusiness.com"},
            ip_address="127.0.0.1",
        )
        form_data = {
            "Email Address": "candidate@examplebusiness.com",
            "First Name": "Alex",
        }
        return form, submission, form_data, []

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/test/webhook",
        OWNER_NOTIFICATION_FORM_SLUGS=["join-our-team", "client-consultation", "contact-us"],
        SLACK_NOTIFICATION_MENTION="<!here>",
    )
    @patch("main.views._post_slack_webhook")
    def test_every_form_sends_slack_alert(self, post_slack_webhook):
        payload = self._build_submission_payload("general-intake", "General Intake")
        send_intake_notification(*payload)

        post_slack_webhook.assert_called_once()
        webhook_url, slack_payload = post_slack_webhook.call_args.args
        self.assertEqual(webhook_url, "https://hooks.slack.com/services/test/webhook")
        self.assertIn("General Intake", slack_payload["text"])
        # Non-priority forms should not ping the channel.
        self.assertNotIn("<!here>", slack_payload["text"])

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/test/webhook",
        OWNER_NOTIFICATION_FORM_SLUGS=["join-our-team", "client-consultation", "contact-us"],
        SLACK_NOTIFICATION_MENTION="<!here>",
    )
    @patch("main.views._post_slack_webhook")
    def test_priority_forms_include_mention(self, post_slack_webhook):
        payload = self._build_submission_payload(
            "client-consultation",
            "Request a Free Consultation",
        )
        send_intake_notification(*payload)

        post_slack_webhook.assert_called_once()
        _webhook_url, slack_payload = post_slack_webhook.call_args.args
        self.assertIn("Request a Free Consultation", slack_payload["text"])
        self.assertIn("<!here>", slack_payload["text"])

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/test/webhook",
        OWNER_NOTIFICATION_FORM_SLUGS=["contact-us"],
        SLACK_NOTIFICATION_MENTION="<!here>",
    )
    @patch("main.views._post_slack_webhook")
    def test_contact_form_sends_priority_slack_alert(self, post_slack_webhook):
        # The contact-us form is seeded by migration 0015.
        form = IntakeForm.objects.get(slug="contact-us")
        submission = IntakeSubmission.objects.create(
            form=form,
            data={"Email Address": "visitor@examplebusiness.com"},
            ip_address="127.0.0.1",
        )
        form_data = {
            "Email Address": "visitor@examplebusiness.com",
            "Message": "I have a question about tax services.",
        }
        send_intake_notification(form, submission, form_data, [])

        post_slack_webhook.assert_called_once()
        _webhook_url, slack_payload = post_slack_webhook.call_args.args
        self.assertIn("Contact Us", slack_payload["text"])
        self.assertIn("<!here>", slack_payload["text"])

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/test/webhook",
        SITE_BASE_URL="https://hirexfed.com",
    )
    @patch("main.views._post_slack_webhook")
    def test_slack_alert_links_to_admin_submission(self, post_slack_webhook):
        form, submission, form_data, files = self._build_submission_payload(
            "general-intake", "General Intake"
        )
        send_intake_notification(form, submission, form_data, files)

        _webhook_url, slack_payload = post_slack_webhook.call_args.args
        rendered = str(slack_payload["blocks"])
        self.assertIn(
            f"https://hirexfed.com/admin/main/intakesubmission/{submission.id}/change/",
            rendered,
        )

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/general/intake",
        SLACK_FORM_WEBHOOK_URLS={"contact-us": "https://hooks.slack.com/services/contact/channel"},
    )
    @patch("main.views._post_slack_webhook")
    def test_contact_form_routes_to_dedicated_channel(self, post_slack_webhook):
        # The contact-us form is seeded by migration 0015.
        form = IntakeForm.objects.get(slug="contact-us")
        submission = IntakeSubmission.objects.create(
            form=form,
            data={"Email Address": "visitor@examplebusiness.com"},
            ip_address="127.0.0.1",
        )
        send_intake_notification(
            form, submission, {"Email Address": "visitor@examplebusiness.com"}, []
        )

        webhook_url, _payload = post_slack_webhook.call_args.args
        self.assertEqual(webhook_url, "https://hooks.slack.com/services/contact/channel")

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/general/intake",
        SLACK_FORM_WEBHOOK_URLS={"contact-us": "https://hooks.slack.com/services/contact/channel"},
    )
    @patch("main.views._post_slack_webhook")
    def test_other_forms_route_to_general_intake_channel(self, post_slack_webhook):
        payload = self._build_submission_payload(
            "client-consultation", "Request a Free Consultation"
        )
        send_intake_notification(*payload)

        webhook_url, _payload = post_slack_webhook.call_args.args
        self.assertEqual(webhook_url, "https://hooks.slack.com/services/general/intake")

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/general/intake",
        SLACK_FORM_WEBHOOK_URLS={"contact-us": ""},
    )
    @patch("main.views._post_slack_webhook")
    def test_contact_form_falls_back_when_dedicated_webhook_unset(self, post_slack_webhook):
        form = IntakeForm.objects.get(slug="contact-us")
        submission = IntakeSubmission.objects.create(
            form=form,
            data={"Email Address": "visitor@examplebusiness.com"},
            ip_address="127.0.0.1",
        )
        send_intake_notification(
            form, submission, {"Email Address": "visitor@examplebusiness.com"}, []
        )

        webhook_url, _payload = post_slack_webhook.call_args.args
        self.assertEqual(webhook_url, "https://hooks.slack.com/services/general/intake")

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="",
        SLACK_WEBHOOK_URL="",
        SLACK_FORM_WEBHOOK_URLS={},
    )
    @patch("main.views._post_slack_webhook")
    def test_missing_webhook_skips_without_error(self, post_slack_webhook):
        payload = self._build_submission_payload("general-intake", "General Intake")
        send_intake_notification(*payload)
        post_slack_webhook.assert_not_called()

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=False,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/test/webhook",
    )
    @patch("main.views._post_slack_webhook")
    def test_disabled_notifications_skip_webhook(self, post_slack_webhook):
        payload = self._build_submission_payload("general-intake", "General Intake")
        send_intake_notification(*payload)
        post_slack_webhook.assert_not_called()

    @override_settings(
        ENABLE_SLACK_NOTIFICATIONS=True,
        SLACK_INTAKE_WEBHOOK_URL="https://hooks.slack.com/services/test/webhook",
    )
    @patch("main.views._post_slack_webhook", side_effect=Exception("slack down"))
    def test_webhook_failure_does_not_raise(self, post_slack_webhook):
        payload = self._build_submission_payload("general-intake", "General Intake")
        # A Slack outage must never break the submission flow.
        send_intake_notification(*payload)
        post_slack_webhook.assert_called_once()


class ContactFormMigrationTests(TestCase):
    def test_contact_form_exists_with_expected_fields(self):
        form = IntakeForm.objects.get(slug="contact-us")
        self.assertTrue(form.is_active)
        self.assertFalse(form.allow_file_uploads)
        field_names = set(form.fields.values_list("field_name", flat=True))
        self.assertEqual(field_names, {"full_name", "email", "subject", "message"})


class SetAsidePivotMigrationTests(TestCase):
    """Migration 0016 seeds the 8(a)/set-aside pivot content."""

    def test_8a_landing_and_checklist_pages_exist(self):
        from .models import DynamicPage

        for slug in ("8a-tax-help", "8a-annual-review-tax-checklist"):
            page = DynamicPage.objects.get(slug=slug)
            self.assertTrue(page.is_published)

    def test_homepage_features_are_pivoted(self):
        from .models import Feature

        titles = set(Feature.objects.values_list("title", flat=True))
        self.assertIn("8(a) & SBA Compliance", titles)
        self.assertNotIn("Income Taxes (IRS)", titles)

    def test_8a_landing_page_renders(self):
        response = self.client.get("/8a-tax-help/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "8(a)")

    def test_setup_command_is_idempotent_with_pivot_content(self):
        call_command("setup_hirexfed_content")
        from .models import DynamicPage, Feature

        self.assertEqual(
            Feature.objects.filter(title="8(a) & SBA Compliance").count(), 1
        )
        self.assertEqual(DynamicPage.objects.filter(slug="8a-tax-help").count(), 1)


class IntakeSubmissionValidationFeedbackTests(TestCase):
    def setUp(self):
        self.form = IntakeForm.objects.create(
            title="Feedback Form",
            slug="feedback-form",
            allow_file_uploads=False,
        )
        IntakeField.objects.create(
            form=self.form,
            label="Full Name",
            field_name="full_name",
            field_type="text",
            is_required=True,
            order=1,
        )
        IntakeField.objects.create(
            form=self.form,
            label="Email Address",
            field_name="email",
            field_type="email",
            is_required=True,
            order=2,
        )

    def test_missing_required_field_shows_field_specific_message(self):
        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={"email": "candidate@business.com"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context["messages"])
        self.assertTrue(
            any("Full Name: This field is required." in str(message) for message in messages_list)
        )

    @override_settings(
        UNIQUE_EMAIL_FORM_SLUGS=["feedback-form"],
    )
    def test_duplicate_email_shows_clear_rejection_reason(self):
        IntakeSubmission.objects.create(
            form=self.form,
            data={"Email Address": "candidate@business.com", "Full Name": "Existing User"},
        )

        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "Second User",
                "email": "candidate@business.com",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context["messages"])
        self.assertTrue(
            any("Email Address: This email has already been used for Feedback Form." in str(message)
                for message in messages_list)
        )

    @override_settings(
        UNIQUE_EMAIL_FORM_SLUGS=["join-our-team"],
        ENABLE_SLACK_NOTIFICATIONS=False,
    )
    def test_duplicate_email_is_allowed_for_client_consultation(self):
        client_form = IntakeForm.objects.create(
            title="Request a Free Consultation",
            slug="client-consultation",
            allow_file_uploads=False,
        )
        IntakeField.objects.create(
            form=client_form,
            label="Full Name",
            field_name="full_name",
            field_type="text",
            is_required=True,
            order=1,
        )
        IntakeField.objects.create(
            form=client_form,
            label="Email Address",
            field_name="email",
            field_type="email",
            is_required=True,
            order=2,
        )

        IntakeSubmission.objects.create(
            form=client_form,
            data={"Email Address": "candidate@business.com", "Full Name": "Existing User"},
        )

        response = self.client.post(
            reverse("intake_form", kwargs={"slug": client_form.slug}),
            data={
                "full_name": "Second User",
                "email": "candidate@business.com",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IntakeSubmission.objects.filter(form=client_form).count(), 2)
        messages_list = list(response.context["messages"])
        self.assertFalse(
            any("already been used" in str(message) for message in messages_list)
        )

    def test_invalid_email_domain_shows_field_specific_reason(self):
        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "Candidate User",
                "email": "candidate@mailinator.com",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context["messages"])
        self.assertTrue(
            any("Email Address: Please use a permanent email address." in str(message)
                for message in messages_list)
        )


class IntakeSpamProtectionTests(TestCase):
    def setUp(self):
        self.form = IntakeForm.objects.create(
            title="Feedback Form",
            slug="feedback-form",
            allow_file_uploads=False,
        )
        IntakeField.objects.create(
            form=self.form,
            label="Full Name",
            field_name="full_name",
            field_type="text",
            is_required=True,
            order=1,
        )
        IntakeField.objects.create(
            form=self.form,
            label="Email Address",
            field_name="email",
            field_type="email",
            is_required=True,
            order=2,
        )
        IntakeField.objects.create(
            form=self.form,
            label="Message",
            field_name="message",
            field_type="textarea",
            is_required=False,
            order=3,
        )

    def test_honeypot_field_silently_rejects_without_creating_submission(self):
        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "Bot Name",
                "email": "bot@business.com",
                HONEYPOT_FIELD_NAME: "http://spam.example",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "intake_confirmation.html")
        self.assertEqual(IntakeSubmission.objects.filter(form=self.form).count(), 0)

    def test_legitimate_submission_with_empty_honeypot_succeeds(self):
        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "Real User",
                "email": "real@business.com",
                HONEYPOT_FIELD_NAME: "",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IntakeSubmission.objects.filter(form=self.form).count(), 1)

    def test_rate_limit_blocks_excessive_submissions_from_same_ip(self):
        for _ in range(INTAKE_RATE_LIMIT_MAX_SUBMISSIONS):
            IntakeSubmission.objects.create(
                form=self.form,
                data={"Email Address": "existing@business.com", "Full Name": "Existing User"},
                ip_address="203.0.113.5",
            )

        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "New User",
                "email": "new@business.com",
            },
            follow=True,
            REMOTE_ADDR="203.0.113.5",
        )

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context["messages"])
        self.assertTrue(
            any("too many requests" in str(message).lower() for message in messages_list)
        )
        self.assertEqual(IntakeSubmission.objects.filter(form=self.form).count(), INTAKE_RATE_LIMIT_MAX_SUBMISSIONS)

    def test_message_containing_link_is_rejected_with_field_specific_message(self):
        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "Spammy Sender",
                "email": "spammy@business.com",
                "message": "Check out https://bonusbacklinks.com/sale for cheap SEO!",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context["messages"])
        self.assertTrue(
            any("Links aren't allowed" in str(message) for message in messages_list)
        )
        self.assertEqual(IntakeSubmission.objects.filter(form=self.form).count(), 0)

    def test_message_without_link_succeeds(self):
        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "Real User",
                "email": "real@business.com",
                "message": "I have a question about my tax filing.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(IntakeSubmission.objects.filter(form=self.form).count(), 1)

    def test_different_ip_is_not_rate_limited(self):
        for _ in range(INTAKE_RATE_LIMIT_MAX_SUBMISSIONS):
            IntakeSubmission.objects.create(
                form=self.form,
                data={"Email Address": "existing@business.com", "Full Name": "Existing User"},
                ip_address="203.0.113.5",
            )

        response = self.client.post(
            reverse("intake_form", kwargs={"slug": self.form.slug}),
            data={
                "full_name": "New User",
                "email": "new@business.com",
            },
            follow=True,
            REMOTE_ADDR="198.51.100.9",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            IntakeSubmission.objects.filter(form=self.form).count(),
            INTAKE_RATE_LIMIT_MAX_SUBMISSIONS + 1,
        )


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


class IntakeFileUploadRoutingTests(TestCase):
    def setUp(self):
        self.temp_media_root = tempfile.mkdtemp(prefix="xfed-routing-media-")
        self.media_override = override_settings(MEDIA_ROOT=self.temp_media_root)
        self.media_override.enable()

    def tearDown(self):
        self.media_override.disable()
        shutil.rmtree(self.temp_media_root, ignore_errors=True)

    def _create_file_for_form(self, form_slug, form_title):
        form = IntakeForm.objects.create(
            title=form_title,
            slug=form_slug,
            allow_file_uploads=True,
        )
        submission = IntakeSubmission.objects.create(
            form=form,
            data={"Email Address": f"{form_slug}@examplebusiness.com"},
        )
        return IntakeFile.objects.create(
            submission=submission,
            file=SimpleUploadedFile(
                "upload.pdf",
                b"%PDF-1.7\n1 0 obj\n<<>>\n",
                content_type="application/pdf",
            ),
            original_filename="upload.pdf",
        )

    def test_talent_form_uploads_are_routed_to_resumes_prefix(self):
        intake_file = self._create_file_for_form("join-our-team", "Join Our Team")
        self.assertTrue(intake_file.file.name.startswith("resumes/"))

    def test_client_form_uploads_are_routed_to_client_docs_prefix(self):
        intake_file = self._create_file_for_form(
            "client-consultation",
            "Client Consultation",
        )
        self.assertTrue(intake_file.file.name.startswith("client-docs/"))

    def test_unclassified_form_uploads_default_to_client_docs_prefix(self):
        intake_file = self._create_file_for_form(
            "general-intake",
            "General Intake",
        )
        self.assertTrue(intake_file.file.name.startswith("client-docs/"))


class SetupHireXfedContentCommandTests(TestCase):
    def test_default_mode_preserves_existing_submissions(self):
        form = IntakeForm.objects.create(
            title="Existing Consultation",
            slug="client-consultation",
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
