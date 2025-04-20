from aiogram.client.default import DefaultBotProperties
from aiogram.types.link_preview_options import LinkPreviewOptions

__all__ = ("DEFAULTS", "Defaults")


class LinkPreview(LinkPreviewOptions):
    def __init__(self):
        super().__init__(is_disabled=True)


LINK_PREVIEW_DEFAULTS = LinkPreview()


class Defaults(DefaultBotProperties):
    def __init__(self):
        self.parse_mode = "MarkdownV2"
        self.disable_notification = False
        self.protect_content = False
        self.link_preview = LINK_PREVIEW_DEFAULTS

        super().__init__(
            parse_mode=self.parse_mode,
            disable_notification=self.disable_notification,
            protect_content=self.protect_content,
            link_preview=self.link_preview,
        )


DEFAULTS = Defaults()
