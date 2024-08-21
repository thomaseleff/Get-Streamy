""" Page builder """

from typing import List
import os
import copy
import streamlit as st
from assemblit import setup, blocks
from assemblit.toolkit import _exceptions, content
from assemblit._database import users
from assemblit.pages._components import _core, _key_value, _selector

_COMPATIBLE_APP_TYPES = ['aaas']


class Content():
    """ A `class` that contains the session selector-page content.

    Parameters
    ----------
    header : `str`
        String to display as the webpage header.
    tagline : `str`
        String to display as the webpage tagline.
    selector : `Selector`
        `assemblit.app.structures.Selector` object containing the setting parameter & value to populate the
            drop-down selection options.
    settings : `List[Setting]`
        List of `assemblit.app.structures.Setting` objects containing the setting(s) parameters & values.
    headerless : `bool`
        `True` or `False`, determines whether to display the header & tagline.
    clear_on_submit : `bool`
        `True` or `False`, determines whether to clear the form-submission responses
            after submission.

    Examples
    --------

    ``` python

    # Constructing the session selector-page content

    from assemblit.pages import session_selector

    Sessions = session_selector.Content(
        header='Sessions',
        tagline='Select a session.'
    )

    # Serving the session selector-page content

    Sessions.serve()

    ```
    """

    def __init__(
        self,
        header: str = 'Sessions',
        tagline: str = 'Select a session.',
        selector: blocks.structures.Selector = blocks.structures.Selector(
            parameter='session_name'
        ),
        settings: List[blocks.structures.Setting] = [
            blocks.structures.Setting(
                type='text-input',
                dtype='str',
                parameter='session_name',
                name='Session name',
                description='Input the name of a new session.'
            )
        ],
        headerless: bool = False,
        clear_on_submit: bool = True
    ):
        """ Initializes an instance of the session selector-page content.

        Parameters
        ----------
        header : `str`
            String to display as the webpage header.
        tagline : `str`
            String to display as the webpage tagline.
        selector : `Selector`
            `assemblit.app.structures.Selector` object containing the setting parameter & value to populate the
                drop-down selection options.
        settings : `List[Setting]`
            List of `assemblit.app.structures.Setting` objects containing the setting(s) parameters & values.
        headerless : `bool`
            `True` or `False`, determines whether to display the header & tagline.
        clear_on_submit : `bool`
            `True` or `False`, determines whether to clear the form-submission responses
                after submission.
        """

        # Validate compatibility
        if setup.TYPE not in _COMPATIBLE_APP_TYPES:
            raise _exceptions.CompatibilityError(
                app_type=setup.TYPE,
                page_name=os.path.splitext(os.path.basename(__file__))[0],
                compatible_app_types=_COMPATIBLE_APP_TYPES
            )

        # Assign content class variables
        self.header = content.clean_text(header)
        self.tagline = content.clean_text(tagline)
        self.headerless = headerless
        self.clear_on_submit = clear_on_submit

        # Assign database class variables to set the scope for the sessions-selector
        self.scope_db_name = setup.USERS_DB_NAME
        self.scope_query_index = setup.USERS_DB_QUERY_INDEX

        # Assign database class variables
        self.db_name = setup.SESSIONS_DB_NAME
        self.table_name = setup.SESSIONS_DB_NAME
        self.query_index = setup.SESSIONS_DB_QUERY_INDEX

        # Assign default session state class variables
        self.selector = _selector.parse_selector(
            parameter=selector.parameter,
            settings=settings
        )
        self.settings = copy.deepcopy(settings)

        # Initialize session state defaults
        _core.initialize_session_state_defaults()

        # Assign session selector defaults
        if self.db_name not in st.session_state[setup.NAME]:
            st.session_state[setup.NAME][self.db_name] = {
                self.table_name: {
                    'selector': copy.deepcopy(self.selector),
                    'settings': copy.deepcopy(self.settings),
                    'form-submission': False,
                    'set-up': False
                },
            }
        else:
            if self.table_name not in st.session_state[setup.NAME][self.db_name]:
                st.session_state[setup.NAME][self.db_name][self.table_name] = {
                    'selector': copy.deepcopy(self.selector),
                    'settings': copy.deepcopy(self.settings),
                    'form-submission': False,
                    'set-up': False
                }

        # Initialize session state status defaults
        _core.initialize_session_state_status_defaults(
            db_name=self.db_name
        )

    def serve(self):
        """ Serves the session selector-page content.
        """

        # Manage authentication
        if st.session_state[setup.NAME][setup.AUTH_NAME][setup.AUTH_QUERY_INDEX]:

            # Configure and display the header
            if not self.headerless:
                _core.set_page_config(
                    header=self.header,
                    icon=None,
                    layout=setup.LAYOUT,
                    initial_sidebar_state=setup.INITIAL_SIDEBAR_STATE
                )
                _core.display_page_header(
                    header=self.header,
                    tagline=self.tagline,
                    context=None
                )

            # Parse the form response
            response = _key_value.parse_form_response(
                db_name=self.db_name,
                table_name=self.table_name
            )

            # Update the sessions-settings database
            if response:

                # Create a new session
                if st.session_state[setup.NAME][self.db_name][self.table_name]['set-up']:
                    _selector.create_session(
                        db_name=self.db_name,
                        table_name=self.table_name,
                        query_index=self.query_index,
                        scope_db_name=self.scope_db_name,
                        scope_query_index=self.scope_query_index,
                        response=response
                    )

                    # Reset set-up form
                    if not st.session_state[setup.NAME][self.db_name]['errors']:
                        _selector.display_session_setup_form(
                            db_name=self.db_name,
                            table_name=self.table_name,
                            value=False
                        )

                # Update an existing session
                else:
                    _selector.update_session(
                        db_name=self.db_name,
                        table_name=self.table_name,
                        query_index=self.query_index,
                        scope_db_name=self.scope_db_name,
                        scope_query_index=self.scope_query_index,
                        response=response
                    )

            # Initialize the scope-database table
            _ = users.Connection().create_table(
                table_name=users.Schemas.sessions.name,
                schema=users.Schemas.sessions
            )

            # Manage the sessions-key-value-pair-settings database table
            _key_value.initialize_key_value_pair_table(
                db_name=self.db_name,
                table_name=self.table_name,
                query_index=self.query_index,
                settings=copy.deepcopy(self.settings)
            )

            # Retrieve sessions-key-value-pair drop-down selection options
            options = _selector.select_selector_dropdown_options(
                db_name=self.db_name,
                table_name=self.table_name,
                query_index=self.query_index,
                scope_db_name=self.scope_db_name,
                scope_query_index=self.scope_query_index
            )

            # Set sessions-key-value-pair drop-down default query index
            index = _selector.select_selector_default_value(
                db_name=self.db_name,
                table_name=self.table_name,
                query_index=self.query_index,
                scope_db_name=self.scope_db_name,
                scope_query_index=self.scope_query_index,
                options=options
            )

            # Set default sessions-key-value-pair settings configuration form attributes
            if not options:
                st.session_state[setup.NAME][self.db_name][self.table_name]['set-up'] = True

            # Display the session selector drop-down
            self._display_session_selector(
                options=options,
                index=index
            )

            # Display the sessions-key-value-pair-settings configuration form for an existing session
            if (
                (st.session_state[setup.NAME][setup.SESSIONS_DB_NAME][setup.SESSIONS_DB_QUERY_INDEX])
                and (not st.session_state[setup.NAME][self.db_name][self.table_name]['set-up'])
            ):
                _key_value.display_key_value_pair_settings_form(
                    header='Parameters',
                    tagline='Edit the form then click `Save` to modify the currently selected entry.',
                    db_name=self.db_name,
                    table_name=self.table_name,
                    query_index=self.query_index,
                    apply_db_values=True,
                    clear_on_submit=self.clear_on_submit
                )

            # Display the sessions-key-value-pair-settings configuration form for a new session
            else:

                # Reset session selector settings defaults
                st.session_state[setup.NAME][self.db_name][self.table_name]['settings'] = copy.deepcopy(self.settings)

                # Display
                _key_value.display_key_value_pair_settings_form(
                    header='Setup',
                    tagline='Populate each field in the form then click `Save` to create a new entry.',
                    db_name=self.db_name,
                    table_name=self.table_name,
                    query_index=self.query_index,
                    apply_db_values=False,
                    clear_on_submit=self.clear_on_submit
                )

            # Display page status
            _core.display_page_status(
                db_name=self.db_name
            )

        else:

            # Return to home-page
            st.switch_page(st.session_state[setup.NAME]['pages']['home'])

    # Define generic sessions-selector service function(s)
    def _display_session_selector(
        self,
        options: list,
        index: int
    ):
        """ Displays the database table drop-down options and default value as a selector.

        Parameters
        ----------
        options: `list`
            The list containing the the drop-down options.
        index : `int`
            The index position of the value to be displayed as the default selection.
        """

        # Layout columns
        _, col2 = st.columns(setup.CONTENT_COLUMNS)

        # Display the session selector drop-down
        with col2:

            # Layout session selector columns
            col1, col2, col3 = st.columns([.6, .2, .2])

            # Display the session selector
            if not st.session_state[setup.NAME][self.db_name][self.table_name]['set-up']:
                with col1:
                    _selector.display_selector(
                        db_name=self.db_name,
                        table_name=self.table_name,
                        query_index=self.query_index,
                        scope_db_name=self.scope_db_name,
                        scope_query_index=self.scope_query_index,
                        options=options,
                        index=index,
                        disabled=False
                    )
                with col2:
                    self._display_session_delete_button(
                        disabled=False
                    )
                with col3:
                    self._display_session_new_button(
                        disabled=False
                    )
            else:
                with col1:
                    _selector.display_selector(
                        db_name=self.db_name,
                        table_name=self.table_name,
                        query_index=self.query_index,
                        scope_db_name=self.scope_db_name,
                        scope_query_index=self.scope_query_index,
                        options=options,
                        index=index,
                        disabled=True
                    )
                with col2:
                    self._display_session_delete_button(
                        disabled=True
                    )

                with col3:
                    if options:
                        self._display_session_edit_button(
                            disabled=False
                        )
                    else:
                        self._display_session_edit_button(
                            disabled=True
                        )

    def _display_session_delete_button(
        self,
        disabled: bool
    ):
        """ Displays the button to delete the selected session.

        Parameters
        ----------
        disabled : `int`
            `True` or `False`, whether the button is displayed disabled or not.
        """

        # Display the 'Delete' button
        st.button(
            label='Delete',
            key='Button:%s' % _selector.generate_selector_key(
                db_name=self.db_name,
                table_name=self.table_name,
                parameter='Delete'
            ),
            type='secondary',
            disabled=disabled,
            on_click=_selector.delete_session,
            kwargs={
                'session_id': st.session_state[setup.NAME][self.db_name][self.query_index]
            },
            use_container_width=True
        )

    def _display_session_edit_button(
        self,
        disabled: bool
    ):
        """ Displays the button to edit the settings of the selected session.

        Parameters
        ----------
        disabled : `int`
            `True` or `False`, whether the button is displayed disabled or not.
        """

        # Display the 'Edit' button
        st.button(
            label='Edit',
            key='Button:%s' % _selector.generate_selector_key(
                db_name=self.db_name,
                table_name=self.table_name,
                parameter='Edit'
            ),
            type='primary',
            disabled=disabled,
            on_click=_selector.display_session_setup_form,
            kwargs={
                'db_name': self.db_name,
                'table_name': self.table_name,
                'value': False
            },
            use_container_width=True
        )

    def _display_session_new_button(
        self,
        disabled: bool
    ):
        """ Displays the button to create a new session.

        Parameters
        ----------
        disabled : `int`
            `True` or `False`, whether the button is displayed disabled or not.
        """

        # Display the 'New' button
        st.button(
            label='New',
            key='Button:%s' % _selector.generate_selector_key(
                db_name=self.db_name,
                table_name=self.table_name,
                parameter='New'
            ),
            type='primary',
            disabled=disabled,
            on_click=_selector.display_session_setup_form,
            kwargs={
                'db_name': self.db_name,
                'table_name': self.table_name,
                'value': True
            },
            use_container_width=True
        )
