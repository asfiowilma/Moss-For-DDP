scrape_report() {
    # to scrape reports from MOSS
    # url should look like this: http://moss.stanford.edu/results/6/9408393705181/
    # including protocol specifier, forward-slash at the end
    url="$1"
    for url_child in "$url"match{0..300}; do
        wget -r -p -k "$url_child"{,\-0,\-1,\-top}.html || break;
    done
    wget -r -p -k $url;
    find . -type f -name "*.html" -exec sed -i "s|$url||g" {} +
}
