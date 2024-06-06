"""
Information
---------------------------------------------------------------------
Name        : run_listing.py
Location    : ~/pages
Author      : Tom Eleff
Published   : 2024-06-02
Revised on  : .

Description
---------------------------------------------------------------------
Contains the `Class` for the run-listing-page.
"""

import streamlit as st
from assemblit import setup, db
from assemblit.pages._components import _core, _run_listing


class Content():

    def __init__(
        self,
        header: str = 'Listing',
        tagline: str = 'Browse submitted analysis runs, review status and navigate to outputs.',
        content_info: str = (
            'Navigate to the **%s** page to load a session.' % (
                ''.join([
                    setup.SESSIONS_DB_NAME[0].upper(),
                    setup.SESSIONS_DB_NAME[1:].lower()
                ])
            )
        ),
        headerless: bool = False
    ):
        """ Initializes the content of the run-analysis `Class`.

        Parameters
        ----------
        header : `str`
            String to display as the web-page header.
        tagline : `str`
            String to display as the web-page tagline.
        content_info : `str`
            String to display as `streamlit.info()` when there is no active session.
        headerless : `bool`
            `True` or `False`, determines whether to display the header & tagline.
        """

        # Assign content class variables
        self.header = header
        self.tagline = tagline
        self.content_info = content_info
        self.headerless = headerless

        # Assign database class variables to set the scope for run-analysis
        self.scope_db_name = setup.SESSIONS_DB_NAME
        self.scope_query_index = setup.SESSIONS_DB_QUERY_INDEX

        # Assign database class variables
        self.db_name = setup.ANALYSIS_DB_NAME
        self.table_name = 'listing'
        self.query_index = setup.ANALYSIS_DB_QUERY_INDEX

        # Initialize session state defaults
        _core.initialize_session_state_defaults()

        # Initialize session state status defaults
        _core.initialize_session_state_status_defaults(
            db_name=self.db_name
        )

    def serve(
        self
    ):
        """ Serves the run-analysis-page content.
        """

        # Manage authentication
        if st.session_state[setup.NAME][setup.AUTH_NAME][setup.AUTH_QUERY_INDEX]:

            # Display web-page header
            _core.display_page_header(
                header=self.header,
                tagline=self.tagline,
                headerless=self.headerless,
                show_context=True
            )

            # Manage the active session
            if st.session_state[setup.NAME][setup.SESSIONS_DB_NAME][setup.SESSIONS_DB_QUERY_INDEX]:

                # Initialize the scope-database table
                _ = db.initialize_table(
                    db_name=self.scope_db_name,
                    table_name=self.table_name,
                    cols=(
                        [self.scope_query_index] + [self.query_index]
                    )
                )

                # Initialize the analysis-database table
                _ = db.initialize_table(
                    db_name=self.db_name,
                    table_name=self.table_name,
                    cols=(
                        [
                            self.query_index,
                            'name',
                            'server_type',
                            'submitted_by',
                            'created_on',
                            'state',
                            'start_time',
                            'end_time',
                            'run_time',
                            'file_name',
                            'inputs',
                            'outputs',
                            'run_information',
                            'parameters',
                            'tags',
                            'url'
                        ]
                    )
                )

                # Refresh the run-listing table
                _run_listing.refresh_run_listing_table(
                    db_name=self.db_name,
                    table_name=self.table_name,
                    query_index=self.query_index,
                )

                # Display the run-listing table
                _run_listing.display_run_listing_table(
                    db_name=self.db_name,
                    table_name=self.table_name,
                    query_index=self.query_index,
                    scope_db_name=self.scope_db_name,
                    scope_query_index=self.scope_query_index
                )

                # Display page status
                _core.display_page_status(
                    db_name=self.db_name
                )

            else:

                # Display content information
                _core.display_page_content_info(
                    content_info=self.content_info
                )

        else:

            # Return to home-page
            st.switch_page(st.session_state[setup.NAME]['pages']['home'])