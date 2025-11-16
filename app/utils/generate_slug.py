from slugify import slugify
from app import db
from app.models import Destinations

def generate_unique_slug(name):
        """
        Generate a unique slug for a Destination based on its name.
        If the slug already exists, append a counter suffix (-1, -2)
        """

        # slugify the name
        base_slug = slugify(name)
        slug = base_slug

        # check DB for existing slugs
        counter = 1
        while Destinations.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug
