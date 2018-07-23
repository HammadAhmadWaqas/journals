""" Model factories """

import random
import string

from urllib.parse import urljoin, urlsplit, urlunsplit

import factory
from factory.fuzzy import FuzzyText
from faker import Faker
from wagtail.wagtailcore.models import Page, Site
from wagtail.wagtailimages.models import Image

from journals.apps.journals.models import JournalAboutPage, JournalPage
from journals.apps.core.models import SiteConfiguration, User
from journals.apps.theming.models import SiteBranding

USER_PASSWORD = 'password'
RANDOM_SEED_STATE = random.getstate()


def random_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    while True:
        yield ''.join(random.choice(chars) for _ in range(size))


def fake_words_generator(prefix=None, numwords=3):
    """
    Generates strings of randomly generated words
    Args:
         prefix (str): will be appended to the front of the string
         numwords (int): number of words generated (prefix is not included in the count)
    Yields:
         (str): string of randomly generated words separated by spaces
    """
    fake = Faker()
    while True:
        fake_words = fake.words(nb=numwords)  # pylint: disable=no-member
        if prefix:
            fake_words = [prefix] + fake_words

        yield ' '.join(fake_words)


def fake_url_generator(netloc_prefix='', path='', random_state=None):
    fake = Faker()
    if random_state:
        fake.random.setstate(random_state)
    while True:
        fake_url = fake.url()  # pylint: disable=no-member

        if netloc_prefix or path:
            split_fake_url = urlsplit(fake_url)
            fake_url = urlunsplit([
                split_fake_url.scheme,
                netloc_prefix + split_fake_url.netloc,
                path if path else split_fake_url.path,
                split_fake_url.query,
                split_fake_url.fragment
            ])

        yield fake_url


class UserFactory(factory.DjangoModelFactory):
    """ Model factory for User model """
    username = factory.Sequence(lambda n: 'user_%d' % n)
    password = factory.PostGenerationMethodCall('set_password', USER_PASSWORD)
    is_active = True
    is_superuser = False
    is_staff = False
    email = factory.Faker('email')
    first_name = FuzzyText()
    last_name = factory.Faker('last_name')
    full_name = factory.LazyAttribute(lambda user: ' '.join((user.first_name, user.last_name)))

    class Meta:
        model = User


class PageFactory(factory.DjangoModelFactory):
    """ Model factory for Page model """

    slug = FuzzyText()
    title = FuzzyText(prefix='page-title')
    path = factory.Iterator(random_string_generator())
    depth = 1
    numchild = 2

    class Meta:
        model = Page


class JournalAboutPageFactory(factory.DjangoModelFactory):
    """ Model factory for JournalAboutPage model """

    slug = FuzzyText()
    title = FuzzyText(prefix='page-title')
    path = factory.Iterator(random_string_generator())
    depth = 1
    numchild = 0
    custom_content = factory.Iterator(random_string_generator(size=250))
    short_description = FuzzyText(prefix='about-page-short-description')

    class Meta:
        model = JournalAboutPage


class JournalPageFactory(factory.DjangoModelFactory):
    """ Model factory for JournalPage model """

    slug = FuzzyText()
    title = FuzzyText(prefix='page-title')
    path = factory.Iterator(random_string_generator())
    depth = 1
    numchild = 0
    body = factory.Iterator(random_string_generator(size=250))

    class Meta:
        model = JournalPage


class SiteFactory(factory.DjangoModelFactory):
    """ Model factory for Site model """

    hostname = factory.Faker('url')
    port = "18606"
    is_default_site = False
    root_page = factory.SubFactory(PageFactory)
    site_name = FuzzyText(prefix='site-name-')

    class Meta:
        model = Site


class ImageFactory(factory.DjangoModelFactory):
    """ Model factory for Image model """

    title = factory.Iterator(fake_words_generator(prefix='title:'))
    file = factory.Faker('file_path', depth=1, extension='png')
    width = random.randint(100, 2000)
    height = random.randint(100, 2000)
    collection_id = 1

    class Meta:
        model = Image


class SiteBrandingFactory(factory.DjangoModelFactory):
    """ Model factory for SiteBranding model """

    theme_name = factory.Iterator(fake_words_generator(prefix='theme name:'))
    site = factory.SubFactory(SiteFactory)
    site_logo = factory.SubFactory(ImageFactory)

    class Meta:
        model = SiteBranding


class SiteConfigurationFactory(factory.DjangoModelFactory):
    """ Model factory for SiteConfiguration model """

    def _get_oauth_settings(lms_url_root):  # pylint: disable=no-self-argument
        """ Returns populated oauth_settings """
        oauth_settings = {
            "SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY": "journals-secret",
            "SOCIAL_AUTH_EDX_OIDC_URL_ROOT": urljoin(lms_url_root, 'oauth2'),
            "SOCIAL_AUTH_EDX_OIDC_ISSUERS": [
                lms_url_root
            ],
            "SOCIAL_AUTH_EDX_OIDC_KEY": "journals-key",
            "SOCIAL_AUTH_EDX_OIDC_SECRET": "journals-secret",
            "SOCIAL_AUTH_EDX_OIDC_PUBLIC_URL_ROOT": urljoin(lms_url_root, 'oauth2'),
            "SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL": urljoin(lms_url_root, 'logout'),
            "SOCIAL_AUTH_EDX_OIDC_ISSUER": urljoin(lms_url_root, 'oauth2')
        }
        return oauth_settings

    site = factory.SubFactory(SiteFactory)

    discovery_api_url = factory.Iterator(fake_url_generator(
        netloc_prefix='discovery-',
        path='api/v1',
        random_state=RANDOM_SEED_STATE
    ))
    discovery_journal_api_url = factory.Iterator(fake_url_generator(
        netloc_prefix='discovery-',
        path='journal/api/v1',
        random_state=RANDOM_SEED_STATE
    ))
    ecommerce_api_url = factory.Iterator(fake_url_generator(
        netloc_prefix='ecommerce-',
        path='api/v2',
        random_state=RANDOM_SEED_STATE
    ))
    ecommerce_api_url = factory.Iterator(fake_url_generator(
        netloc_prefix='ecommerce-',
        path='journal/api/v1',
        random_state=RANDOM_SEED_STATE
    ))
    lms_url_root = factory.Iterator(fake_url_generator(
        netloc_prefix='lms-',
        random_state=RANDOM_SEED_STATE
    ))
    oauth_settings = factory.Iterator(
        iterator=fake_url_generator(netloc_prefix='lms-', random_state=RANDOM_SEED_STATE),
        getter=_get_oauth_settings
    )
    frontend_url = factory.Iterator(fake_url_generator(
        netloc_prefix='frontend-',
        random_state=RANDOM_SEED_STATE
    ))

    currency_codes = 'USD'
    discovery_partner_id = 'edx'
    ecommerce_partner_id = 'edx'

    class Meta:
        model = SiteConfiguration