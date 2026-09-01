from whitenoise.storage import CompressedManifestStaticFilesStorage


class RelaxedManifestStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content=content, filename=filename)
        except ValueError:
            return name
