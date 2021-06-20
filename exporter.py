import base64
import json
import logging
import os
import re
from functools import reduce
from pprint import pprint
from typing import Union, Optional, List, Dict, Any

import click
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime


logging.basicConfig(level=logging.INFO)


def parse(soup: BeautifulSoup, input_directory: str) -> List[Dict[str, Optional[str]]]:
    def extract_hc_text(text_tag: Optional[Tag]) -> Optional[str]:
        replacements = [
            ('<span class="comments__table__items__parenttext__quote" el="HideQuoteBox">', ''),
            ('<span class="comments__table__items__parenttext__showquote" el="DisplayQuote">', ''),
            ('</span>', ''),
            ('\n', ' '),
        ]
        if text_tag is not None:
            inner_html = re.sub(' {2,}', '', text_tag.encode_contents().decode())
            for rp in replacements:
                inner_html = inner_html.replace(rp[0], rp[1])
            return inner_html.rstrip()

    comments = list()
    comments_tags = soup.select('.comments__block')
    logging.info('Parsing comments..')
    for tag in comments_tags:
        tag: Tag
        with open(os.path.join(input_directory, tag.select_one('.comments__boxavatar img').attrs.get('src')), 'rb') as f:
            avatar_base64 = base64.b64encode(f.read()).decode()
        comments.append({
            'name': tag.select_one('.comments__table__items__name').next_element,
            'date': datetime.strptime(tag.select_one('.comments__table__items__date').text, '%d.%m.%y %H:%M:%S').isoformat(),
            'parent_text': extract_hc_text(tag.select_one('.comments__table__items__parenttext')),
            'text': extract_hc_text(tag.select_one('.comments__table__items__text')),
            'url': tag.select_one('.comments__block__content a').attrs.get('href', ''),
            'title': tag.select_one('.comments__table__items__forumtitle').text.strip(),
            'avatar': f'data:image/jpeg;base64,{avatar_base64}',
            'ip': tag.select_one('.comments__table__items__name__ip').text.rstrip()
        })
    logging.info(f'Successfully parsed {len(comments)} comments!')
    return comments


def export(input_html, output):
    with open(input_html, 'r', encoding="UTF-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    object_output = parse(soup, os.path.dirname(input_html))
    with open(output, 'w', encoding="UTF-8") as f:
        json.dump(object_output, f, indent=4, ensure_ascii=False)


@click.command()
@click.option('--input-html', prompt='Path to saved page', help='Path to page with saved comments (full-page)')
@click.option('--o', prompt='Path to output file', help='Path to output JSON file')
def main(input_html, output):
    """
    Parses html with images from HyperComments and saves output to JSON.html
    """
    export(input_html, output)


if __name__ == '__main__':
    main()
