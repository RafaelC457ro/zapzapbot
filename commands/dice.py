import random

class Dice:
    name = 'd'
    description = """
    
    Roll dice
    Usage: /d dice_range
    Ex: 
    
    /d 20
    Result: 20
    """
    
    @staticmethod
    def execute(caller, driver, command):
        arg = command['command']['args'][0]
        print(arg)
        if arg.isdigit():
            number = Dice.rand_number(int(arg))
            caller.send_message(str(number))

        else:
            caller.send_message('invalid command: '+ Dice.description)

    @staticmethod
    def rand_number(range):
        return random.randint(1, range) 
