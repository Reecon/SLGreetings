#---------------------------
#   Import Libraries
#---------------------------
import os
import codecs
import sys
import json
import re
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Greetings"
Website = "reecon820@gmail.com"
Description = "Gives you a list of people greeting you"
Creator = "Reecon820"
Version = "0.0.3.0"

#---------------------------
#   Settings Handling
#---------------------------
class GreetSettings:
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            self.Keyword = "hello"
            self.KeywordUse = False
            self.Emote = "HeyGuys VoHiYo"
            self.EmoteUse = False
            self.PauseScroll = 20
            self.PauseScrollUse = True
            self.permission = "everyone"
            self.info = ""

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")

    def Save(self, settingsfile):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------
#   Define Global Variables
#---------------------------
global greetQueueHtmlPath
greetQueueHtmlPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "Queue.html"))

global greetQueue
greetQueue = set()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    global greetSettingsFile
    greetSettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    global greetScriptSettings
    greetScriptSettings = GreetSettings(greetSettingsFile)

    updateUi()

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    #   only handle messages from chat
    if data.IsChatMessage() and Parent.HasPermission(data.User, greetScriptSettings.permission, greetScriptSettings.info) and not data.IsWhisper():

        # is in queue?
        if data.User.lower() in greetQueue:
            # ignore message
            return

        keywordsPass = True
        emotesPass = True

        # use keyword filter?
        if greetScriptSettings.KeywordUse:
            # check for keywords
            keywords = set(greetScriptSettings.Keyword.split(" "))
            tokens = set(data.Message.lower().split(" "))
            
            if keywords.isdisjoint(tokens):
                keywordsPass = False

        # use emote filter?
        if greetScriptSettings.EmoteUse:
            # check for emotes
            emotes = set(greetScriptSettings.Emote.split(" "))
            tokens = set(data.Message.split(" "))
            
            if emotes.isdisjoint(tokens):
                emotesPass = False
        
        # send to html
        if (keywordsPass and emotesPass) or (greetScriptSettings.EmoteUse and emotesPass) or (greetScriptSettings.KeywordUse and keywordsPass):
            greetQueue.add(data.User.lower())
            jsonData = '{{ "user":"{0}", "message": "{1}"}}'.format(data.User, data.Message.replace('"', '\\"'))
            Parent.BroadcastWsEvent("EVENT_GREET_MESSAGE", jsonData)


    # remove messages from user who got timed out
    if data.IsRawData():
        tokens = data.RawData.split(" ")
        
        # check for CLEARCHAT
        #0 @ban-reason=;room-id=987654321;target-user-id=123456789;tmi-sent-ts=1534998648808
        #1 :tmi.twitch.tv
        #2 CLEARCHAT
        #3 #<channel>
        #4 :<username>
        try:
            if tokens[2] == "CLEARCHAT":
                # check if user is in queue
                user = tokens[4][1:]
                if user in greetQueue:
                    # yes? send clear
                    jsonData = '{{ "user":"{0}" }}'.format(user)
                    Parent.BroadcastWsEvent("EVENT_GREET_CLEARCHAT", jsonData)
                else:
                    # no? add to queue
                    greetQueue.add(data.User.lower())
        except IndexError:
            pass

    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    greetScriptSettings.Reload(jsonData)
    greetScriptSettings.Save(greetSettingsFile)
    updateUi()
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def OpenQueueFile():
    os.startfile(greetQueueHtmlPath)
    time.sleep(2)
    pauseUse = 'true' if greetScriptSettings.PauseScrollUse else 'false'
    jsonData = '{{ "pauseOnScroll":{0}, "scrollTimeout": {1}}}'.format(pauseUse, greetScriptSettings.PauseScroll)
    Parent.BroadcastWsEvent("EVENT_GREET_SETTINGS", jsonData)


def updateUi():
    ui = {}
    UiFilePath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="r") as f:
            ui = json.load(f, encoding="utf-8")
    except Exception as err:
        Parent.Log(ScriptName, "{0}".format(err))

    # update ui with loaded settings
    ui['Keyword']['value'] = greetScriptSettings.Keyword
    ui['KeywordUse']['value'] = greetScriptSettings.KeywordUse
    ui['Emote']['value'] = greetScriptSettings.Emote
    ui['EmoteUse']['value'] = greetScriptSettings.EmoteUse
    ui['PauseScroll']['value'] = greetScriptSettings.PauseScroll
    ui['PauseScrollUse']['value'] = greetScriptSettings.PauseScrollUse
    ui['info']['value'] = greetScriptSettings.info
    ui['permission']['value'] = greetScriptSettings.permission

    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="w+") as f:
            json.dump(ui, f, encoding="utf-8", indent=4, sort_keys=True)
    except Exception as err:
        Parent.Log(ScriptName, "{0}".format(err))