""" assemblit.org

Assemblit is helping data analysts and scientists rapidly scale notebooks into analytics-as-a-service (AaaS) web-applications.
"""

import assemblit.pages.home as home

# Initialize the home-page content
Welcome = home.Content(
    header='Welcome',
    tagline="""
        Assemblit is helping data analysts and scientists rapidly scale notebooks into
         analytics-as-a-service (AaaS) web-applications.
    """,
    content_file_path='./documentation/README.md',
    content_info=None
)

# Serve content
Welcome.serve()
