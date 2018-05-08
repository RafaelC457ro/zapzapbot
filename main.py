import importlib
from bot import Bot


def main():
    list_commands = ['Help','Dice']
    bot = Bot()
    
    list_of_class = importlib.import_module("commands")
    
    for command in list_commands:
        command = getattr(list_of_class,'Help')
        bot.register_command(command) 
    
    bot.run()

if __name__ == '__main__':
    main()