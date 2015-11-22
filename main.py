﻿#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import vispy                    # Main application support.

import window                   # Terminal input and display.

from datetime import datetime


class HAL9000(object):
    
    def __init__(self, terminal):
        """Constructor for the agent, stores references to systems and initializes internal memory.
        """
        self.terminal = terminal
        self.location = 'unknown'
        self.first_time = True;

    def on_input(self, evt):
        """Called when user types anything in the terminal, connected via event.
        """
        if evt.text == "Where am I":
            self.terminal.log('\u2014 Current Location: {}. \u2014'.format(self.location), align='right', color='#404040')
        elif self.first_time == True:
           self.terminal.log("Greetings! I am HAL.", align='right', color='#00805A')
           self.first_time = False
        else:
            self.terminal.log("Hello", align='right', color='#00805A')
            
    def on_command(self, evt):
        """Called when user types a command starting with `/` also done via events.
        """
        if evt.text == 'quit':
            vispy.app.quit()

        elif evt.text.startswith('relocate'):
            new_location = evt.text[9:];
            if new_location != self.location:
                self.terminal.log('', align='center', color='#404040')
                self.terminal.log('\u2014 Leaving {}. \u2014'.format(self.location), align='center', color='#404040')
                self.terminal.log('\u2014 Now in the {}. \u2014'.format(new_location), align='center', color='#404040')
                self.location = new_location;
            else:
                self.terminal.log('\u2014 You are already in {}. \u2014'.format(new_location), align='center', color='#404040')
            
        else:
            self.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
            self.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')

    def update(self, _):
        """Main update called once per second via the timer.
        """
        pass


class Application(object):
    
    def __init__(self):
        # Create and open the window for user interaction.
        self.window = window.TerminalWindow()

        # Print some default lines in the terminal as hints.
        self.window.log('Operator started the chat.', align='left', color='#808080')
        self.window.log('HAL9000 joined.', align='right', color='#808080')

        # Construct and initialize the agent for this simulation.
        self.agent = HAL9000(self.window)

        # Connect the terminal's existing events.
        self.window.events.user_input.connect(self.agent.on_input)
        self.window.events.user_command.connect(self.agent.on_command)

    def run(self):
        timer = vispy.app.Timer(interval=1.0)
        timer.connect(self.agent.update)
        timer.start()
        
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
