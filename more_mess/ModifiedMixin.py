# @Source: http://code.activestate.com/recipes/464635-call-a-callback-when-a-tkintertext-is-modified/
from tkinter import Text, BOTH


class ModifiedMixin:
    '''
    Class to allow a Tkinter Text widget to notice when it's modified.

    To use this mixin, subclass from Tkinter.Text and the mixin, then write
    an __init__() method for the new class that calls _init().

    Then override the beenModified() method to implement the behavior that
    you want to happen when the Text is modified.
    '''

    def _init(self):
        # Danger Will Robinson!
        # Heavy voodoo here. All widget changes happen via
        # an internal Tcl command with the same name as the
        # widget:  all inserts, deletes, cursor changes, etc
        #
        # The beauty of Tcl is that we can replace that command
        # with our own command. The following code does just
        # that: replace the code with a proxy that calls the
        # original command and then calls a callback. We
        # can then do whatever we want in the callback.
        private_callback = self.register(self._callback)
        self.tk.eval('''
                    proc widget_proxy {actual_widget callback args} {

                        # this prevents recursion if the widget is called
                        # during the callback
                        set flag ::dont_recurse(actual_widget)

                        # call the real tk widget with the real args
                        set result [uplevel [linsert $args 0 $actual_widget]]

                        # call the callback and ignore errors, but only
                        # do so on inserts, deletes, and changes in the 
                        # mark. Otherwise we'll call the callback way too 
                        # often.
                        if {! [info exists $flag]} {
                            if {([lindex $args 0] in {insert replace delete}) ||
                                ([lrange $args 0 2] == {mark set insert})} {
                                # the flag makes sure that whatever happens in the
                                # callback doesn't cause the callbacks to be called again.
                                set $flag 1
                                catch {$callback $result {*}$args } callback_result
                                unset -nocomplain $flag
                            }
                        }

                        # return the result from the real widget command
                        return $result
                    }
                    ''')
        self.tk.eval('''
                    rename {widget} _{widget}
                    interp alias {{}} ::{widget} {{}} widget_proxy _{widget} {callback}
                '''.format(widget=str(self), callback=private_callback))
        '''
        Prepare the Text for modification notification.
        '''
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)
        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result

    def _callback(self, result, *args):
        self.callback(result, *args)

    def set_callback(self, callable):
        self.callback = callable

