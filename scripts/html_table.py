import pandas


def html_table(df):
    # Load table template
    with open('table_template.html', 'r') as f:
        template = f.read().replace('\n', '')

    # Replace formatting options that come with to_html()
    html_str = df.to_html()\
        .replace('\n', '')\
        .replace('<table border=\"1\" class=\"dataframe\">', '')\
        .replace('</table>', '')
    return template % html_str



