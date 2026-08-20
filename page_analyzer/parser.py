from bs4 import BeautifulSoup


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text().strip() if h1_tag else ''

    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ''

    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = (
        desc_tag.get('content', '').strip()
        if desc_tag and desc_tag.get('content')
        else ''
    )

    return {
        'h1': h1,
        'title': title,
        'description': description
    }
