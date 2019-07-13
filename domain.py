from urllib.parse import urlparse

def get_domain_name(URL):
    """Get the domain name of a given URL.

    example:
        'secure.site.co.uk' = 'site.co.uk'

    Call get_sub_domain and split the domain into a list of components by '.'
    To cater for .co.uk style domains as well as .com
    Check against the last 2 items of sub-domain,
    If second-from-last is .com or .co then also return third-from-last domain.
    """
    try:
        results = get_sub_domain_name(URL).split('.')
        if len(results) > 2:
            if len(results[-1]) == 2 and results[-2] in ('com', 'co'):
                domain = results[-3] + '.' + results[-2] + '.' + results[-1]
            else:
                domain = results[-2] + '.' + results[-1]
        else:
            domain = results[-2] + '.' + results[-1]
        return domain
    except:
        return ''


def get_sub_domain_name(URL):
    """Get the entire sub-domain of a given URL.

    example:
        'https://secure.site.co.uk/basket' = 'secure.site.co.uk'
    """
    try:
        return urlparse(URL).netloc
    except:
        return ''


