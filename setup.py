
#build output


#'<title>(.*?)</title>', re.IGNORECASE|re.DOTALL
#regex.search(string_to_search).group(2)

import os
from urllib.robotparser import RobotFileParser


# ------------------------------------------------------------#
def robots_check(baseURL, pageURL):
    robotParser = RobotFileParser()
    robotParser.set_url(baseURL + 'robots.txt')
    robotParser.read()
    return robotParser.can_fetch('*', pageURL)

# ------------------------------------------------------------#
def create_site_folder(directory):
    """Each site you crawl has a separate folder."""

    if not os.path.exists(directory):
        print('Creating folder {}'.format(directory))
        os.makedirs(directory)

# ------------------------------------------------------------#
def create_site_data_files(siteName, baseURL):
    """Create queue and history of crawled files.

    If not already created.
    """

    queue = siteName + '/pageQueue.txt'
    crawled = siteName + '/pagesCrawled.txt'
    external = siteName + '/externalPages.txt'

    if not os.path.isfile(queue):
        create_file(queue, baseURL)

    if not os.path.isfile(crawled):
        create_file(crawled, '')

    if not os.path.isfile(external):
        create_file(external, '')

# ------------------------------------------------------------#
def create_file(filePath, fileData):
    """Create new file."""

    with open(filePath, 'w') as file:
        file.write(fileData)
        file.close()

# ------------------------------------------------------------#
def amend_file(filePath, fileData):
    """Amend existing file."""

    with open(filePath, 'a') as file:
        file.write(fileData + '\n')
        file.close()

# ------------------------------------------------------------#
def delete_file_contents(filePath):
    """Delete contents of existing file."""

    with open(filePath, 'w') as file:
        pass
        file.close()

# ------------------------------------------------------------#
def file_to_set(fileName):
    """Read a file and convert lines to set."""

    results = set()
    with open(fileName, 'rt') as file:
        for line in file:
            results.add(line.replace('\n', ''))
    return results

# ------------------------------------------------------------#
def set_to_file(linkSet, fileName):
    """Iterate through a set and set each item as a new line in file."""

    delete_file_contents(fileName)
    for link in sorted(linkSet):
        amend_file(fileName, link)

# ------------------------------------------------------------#
def external_to_file(links, fileName):
    """Iterate through a set and set each item as a new line in file."""

    delete_file_contents(fileName)
    with open(fileName, 'w') as file:
        file.write(str(links) + '\n')
        file.close()

# ------------------------------------------------------------#
def set_output(siteName, baseURL, ):
    import ast

    crawledResults = set()
    with open(siteName + '/pagesCrawled.txt', 'rt') as crawled:
        for line in crawled:
            crawledResults.add(line.replace('\n', ''))

    with open(siteName + '/externalPages.txt', 'rt') as external:
        data = external.read()
        externalResults = ast.literal_eval(data.strip())

    from xml.etree.ElementTree import Element, ElementTree, SubElement

    root = Element('Domain')
    tree = ElementTree(root)

    for sitePage in crawledResults:
        page = Element('Page')
        page.set('URL', sitePage)

        siteTitle = SubElement(page, 'Title')
        siteTitle.text = 'None'

        for externalSite in externalResults:
            for externalPage in externalResults[externalSite]:
                #print(externalPage)
                external = SubElement(page, 'External')
                external.text = externalPage

        root.append(page)
    root.set('URL', baseURL)

    tree.write('sitemap.xml')



