import os
import re
import hashlib
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

class Bot:
    def __init__(self):
        self.commands = []
        self.commands_history = []
        
        self.options = Options()
        self.options.add_experimental_option('prefs', {
            'download.default_directory': './tmp',
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })

    def run(self):
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.get('https://web.whatsapp.com')
        
        while True:
            messages = self._extract_message_list()
            if messages:
                list_commands = self._filter_commands(messages)
                #print(list_commands)
                self._execute_merge_command(list_commands)
            sleep(0.5)
        

    def register_command(self, command):
        if not hasattr(command,'name'):
            raise Exception('Command should have a name prop')
        
        if not hasattr(command,'description'):
            raise Exception('Command should have a description prop')  

        if "execute" not in dir(command):
            raise Exception('Command should have a execute method') 

        self.commands.append(command)
        
    def send_message(self,msg):
        try:
            msg_component = self.driver.find_element_by_class_name('_2S1VP')
            msg_component.send_keys(msg)
            msg_component.send_keys(Keys.ENTER)
            return True
        except NoSuchElementException as e:
            return False

    def _execute_merge_command(self,commands):
        for command in commands:
            if command['command']['hash'] not in self.commands_history:
                self._find_execute_command(command)
                self.commands_history.append(command['command']['hash'])

    def _find_execute_command(self,command):
        for caller_command in self.commands:
            if caller_command.name == command['command']['command']:
                caller_command.execute(self, self.driver, command)
    
    def _filter_commands(self, messages):
        commands = list(filter(lambda x: x['type'] == 'command' , messages))
        return commands

    def _find_audio_element(self, element):
        try:
            return element.find_element_by_tag_name('audio') 
        except NoSuchElementException as e:
            return False

    def _find_sender(self, element):
        try:
            return element.find_element_by_xpath('//div[@data-pre-plain-text]').get_attribute('data-pre-plain-text')
        except NoSuchElementException as e:
            return False

    def _find_message_text(self, element):
        try:
            return element.find_element_by_class_name("copyable-text")
        except NoSuchElementException as e:
            return False

    def _parse_command(self, text, sender):
        if re.match(r'\/[a-z0-9]+', str(text).strip()):
            beans = text[1:].split()
            data = sender + text
            
            hexhash = hashlib.md5(data.encode('utf-8')).hexdigest()
    
            return True, {
                'command': beans[0], 
                'args': beans[1:], 
                'text': ' '.join(beans[1:]),
                'hash': hexhash
                }
        else:
            return False, None

    def _extract_message_list(self):
        try:
            list_of_messages = []
            text_boxes = self.driver.find_elements_by_class_name("message-in")
        
            for box in text_boxes:
                audio = self._find_audio_element(box) 
                if audio:
                    list_of_messages.append({
                            'type':'audio', 
                            'audio': audio.get_attribute('src')
                        })
                else: 
                    msg_text = self._find_message_text(box)
                    if msg_text:
                        sender = self._find_sender(box)
                        is_command, command = self._parse_command(msg_text.text.lower(), sender.lower())
                        
                        if is_command:
                            list_of_messages.append({
                                'type':'command',
                                'command': command,
                                'sender': sender
                            })
                        else:
                            list_of_messages.append({
                                'type':'message',
                                'message':msg_text.text.lower(),
                                'sender': sender
                            })

            if len(list_of_messages) > 0:
                return list_of_messages

        except StaleElementReferenceException as e:
            print(str(e))
    
        return False
    