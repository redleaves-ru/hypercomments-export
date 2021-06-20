# HyperComments Export

to JSON exporter

---

## How to use

1. Install Python 3.6<, pip, and it's dependencies:
    ```shell
    pip install -r requirements.txt
    ```
2. Log in into your account to 
   [HyperComments admin panel](https://admin.hypercomments.com/).
3. Open [page with all comments](https://admin.hypercomments.com/comments/]) and save entire page with images
   (scroll down if needed to load all commentaries).
4. Run exporter:
    ```shell
    python exporter.py --input-html <path-to-saved-html> --o <path-to-json>
    ```
    
    For additional info see help:
    ```shell
    python exporter.py --help
    ```
   
## Why to use

- HyperComments officially closed their free business plans.
- You may prefer migrate to your own commentaries.
- The official HyperComments API is non-intuitive and don't support
  exporting entire site.
- You may prefer JSON over XML.

## Output format

```json
[
   {
        "name": "John Doe",
        "date": "2010-01-01T00:00:00",
        "parent_text": "Reply text commentary",
        "text": "Text commentary with <br> tags",
        "url": "http://example.com/example#hcm=1365272572193975",
        "title": "Title of the site",
        "avatar": "data:image/jpeg;base64,....",
        "ip": "0.0.0.0"
    },
    <...>
]
```