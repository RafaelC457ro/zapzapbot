class Help:
    name = 'help'
    description = 'Show help'
    
    @staticmethod
    def execute(caller, driver, command):
        caller.send_message('Não tem ajuda te vira')
