"""
SEO utility functions for better search engine optimization
"""

def generate_alt_text(photo, service_name=None):
    """
    Generate SEO-friendly alt text for photos
    """
    if service_name:
        return f"{service_name} photography by Shotz - Professional photographer in The Gambia"
    elif photo.category:
        return f"{photo.category.name} photography by Shotz - Professional photographer in The Gambia"
    else:
        return "Professional photography by Shotz - The Gambia's premier photography service"

def generate_meta_description(service_name, location="The Gambia"):
    """
    Generate SEO-friendly meta descriptions
    """
    return f"Professional {service_name.lower()} services in {location}. Expert photography and video production by Shotz. Book your session today!"

def generate_page_title(page_name, location="The Gambia"):
    """
    Generate SEO-friendly page titles
    """
    return f"{page_name} | Shotz Photography - Professional Services in {location}"
