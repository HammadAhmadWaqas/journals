# Custom blocks
from django import forms
from django.utils import six
from wagtail.wagtailcore import blocks
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from bs4 import BeautifulSoup as parser

from .models import Video

PDF_BLOCK_TYPE = 'pdf'
VIDEO_BLOCK_TYPE = 'xblock_video'
IMAGE_BLOCK_TYPE = 'image'
RICH_TEXT_BLOCK_TYPE = 'rich_text'
RAW_HTML_BLOCK_TYPE = 'raw_html'
TOC_BLOCK_TYPE = 'table_of_content'
STREAM_DATA_TYPE_FIELD = 'type'
STREAM_DATA_DOC_FIELD = 'doc'

class VideoChooserBlock(blocks.ChooserBlock):
    target_model = Video
    widget = forms.Select

    class Meta:
        icon = "icon"

    # Return the key value for the select field
    def value_for_form(self, value):
        if isinstance(value, self.target_model):
            return value.pk
        else:
            return value


class PDFBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    doc = DocumentChooserBlock()

    def get_searchable_content(self, value):
        return ['Document: ' + value.get('title')]

    class Meta:
        template = 'blocks/pdf.html'


class TOCBlock(blocks.StructBlock):

    class Meta:
        template = 'blocks/toc.html'


class JournalRichTextBlock(blocks.RichTextBlock):
    def get_searchable_content(self, value):
        return [parser(value.source, 'html.parser').get_text(' ')]


class JournalRawHTMLBlock(blocks.RawHTMLBlock):
    def get_searchable_content(self, value):
        return [parser(six.text_type(value), 'html.parser').get_text()]


class XBlockVideoBlock(blocks.StructBlock):
    BLOCK_TYPE = 'xblock_video'
    STREAM_DATA_FIELD = 'video'

    name = blocks.CharBlock()
    video = VideoChooserBlock(required=True)

    def get_context(self, value, parent_context=None):
        context = super(XBlockVideoBlock, self).get_context(value, parent_context)
        return context

    def get_searchable_content(self, value):
        return ['Video: ' + value.get('name')]

    class Meta:
        template = 'blocks/xblockvideo.html'


class JournalImageChooserBlock(ImageChooserBlock):
    def get_searchable_content(self, value):
        return ['Image: ' + value.title]


