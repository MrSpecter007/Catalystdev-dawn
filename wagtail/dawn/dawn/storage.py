from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class RelaxedManifestStorage(ManifestStaticFilesStorage):
    manifest_strict = False
