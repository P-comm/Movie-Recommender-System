mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enablecors = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml