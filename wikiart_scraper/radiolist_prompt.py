from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import RadioList, Label
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import HSplit


def radiolist_prompt(
    title: str = "",
    values=None,
    default=None,
    cancel_value=None,
    style=None,
    async_=False,
):
    # Create the radio list
    radio_list = RadioList(values, default)
    # Remove the enter key binding so that we can augment it
    radio_list.control.key_bindings.remove("enter")

    bindings = KeyBindings()

    # Replace the enter key binding to select the value and also submit it
    @bindings.add("enter")
    def exit_with_value(event):
        """
        Pressing Enter will exit the user interface, returning the highlighted value.
        """
        radio_list._handle_enter()
        event.app.exit(result=radio_list.current_value)

    @bindings.add("c-c")
    def backup_exit_with_value(event):
        """
        Pressing Ctrl-C will exit the user interface with the cancel_value.
        """
        event.app.exit(result=cancel_value)

    # Create and run the mini inline application
    application = Application(
        layout=Layout(HSplit([Label(title), radio_list])),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=False,
    )
    if async_:
        return application.run_async()
    else:
        return application.run()
