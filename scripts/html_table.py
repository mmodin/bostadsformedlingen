import pandas


def html_table(df):
    # Load table template
    with open('table_template.html', 'r') as f:
        template = f.read().replace('\n', '')

    # Replace id column with url
    html_tag = '<a href="https://bostad.stockholm.se/Lista/details?aid={0}" rel="notrack">{0}</a>'
    df['id'] = df['id'].apply(lambda x: html_tag.format(x))

    # Set display options to enable long URLs
    pandas.set_option('display.max_colwidth', -1)

    # Replace formatting options that come with to_html()
    html_str = df.to_html(escape=False)\
        .replace('\n', '')\
        .replace('<table border=\"1\" class=\"dataframe\">', '')\
        .replace('</table>', '')
    return template % html_str
