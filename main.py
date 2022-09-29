import re

from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import mysql.connector
Window.size(350,600)


kv = """
MFDloatLayout:  #1Parent
    md_bg_color : 1,1,1,1
    MFDloatLayout:  #2Parent
       sizehint:  .4, 1
       pos_hint:{"center_x": .7, "center_y": .9 }
       MFDloatLayout:
           sizehint:  .4, 1
           pos_hint:{"center_x": .4, "center_y": .5 }
           canvas:
                color:
                    rgb: rgba(139,202,193,255)
                rectangle:
                    size: self.size
                    pos: self.pos
                    radius: [8,0,0,8]
            MDIconButton:
                id: color1
                icon: "circle"
                theme_text_color : "custom"
                text_color: 1,1,1,1
                pos_hint: {"center_x": .5 ,"center_y": .5}
                user_font_size: "15sp"
                on_release: app.change_color(self)
                
       MFDloatLayout:
           sizehint:  .4, 1
           pos_hint:{"center_x": .4, "center_y": .5 }
           canvas:
                color:
                    rgb: rgba(137,35,65,255)
                rectangle:
                    size: self.size
                    pos: self.pos
            
            MDIconButton:
                id: color2
                icon: "circle"
                theme_text_color : "custom"
                text_color: 1,1,1,1
                pos_hint: {"center_x": .5 ,"center_y": .5}
                user_font_size: "15sp"
                on_release: app.change_color(self)
        
       MFDloatLayout:
           sizehint:  .4, 1
           pos_hint:{"center_x": .8, "center_y": .5 }
           canvas:
                color:
                    rgb: rgba(99,102,241,255)
                Rounded rectangle:
                    size: self.size
                    pos: self.pos
                    radius: [0,8,8,0]
            
            MDIconButton:
                id: color3
                icon: "circle"
                theme_text_color : "custom"
                text_color: 1,1,1,1
                pos_hint: {"center_x": .5 ,"center_y": .5}
                user_font_size: "15sp"
                on_release: app.change_color(self)     
                    
    MDLabel:
        text: "hey, Login_now."
        pos_hint: {"center_x": .5 , "center_y": .75}
        size_hint_x: .42 
        halign: "left"
        font_name: "BPoppins"
        font_size: "26sp"
    MFDloatLayout:
           sizehint:  .8, .09
           pos_hint:{"center_x": .5, "center_y": .55}
           canvas:
                color:
                    rgb: rgba(99,102,241,255)
                Rounded rectangle:
                    size: self.size
                    pos: self.pos
                    radius : [8]
           TextInput:
                id : email
                hint_text: "Email"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                multiline: False
                hint_text_color: rgba(168,168,168,255)
                background_color: 0,0,0,0
                padding: 18
                font_name = "Poppins"
                font_size = "16Sp"
                
    
    MFDloatLayout:
           sizehint:  .8, .09
           pos_hint:{"center_x": .5, "center_y": .45}
           canvas:
                color:
                    rgb: rgba(99,102,241,255)
                Rounded rectangle:
                    size: self.size
                    pos: self.pos
                    radius : [8]
           TextInput:
                id : password
                hint_text: "Password"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                multiline: False
                Password: True
                hint_text_color: rgba(168,168,168,255)
                background_color: 0,0,0,0
                padding: 18
                font_name = "Poppins"
                font_size = "16Sp"
    MDTextButton:
           text: "Forget Password?"
           font_name: "Poppins"
           theme_text_color: "Custom"
           text_color: rgba(168,168,168,255)
           font_size: "14sp"
           pos_hint: {"center_x": .3, "center_y": .33}
    Button:
          Text : "Login"
          font_name: "Poppins"
          size_hint: .8, .09
          font_size: "18sp"
          pos_hint: {"center_x": .5, "center_y": .15}
          Background_color: 0,0,0,0
          on_release: app.send_data(email,password)
          Canvas.before:
            Color:
                rgb: app.btn_color
             
            Rounded rectangle:
                    size: self.size
                    pos: self.pos
                    radius : [8]
                         
        

"""

class LoginPage(MDApp):

    btn_color = ListProperty(177/255,35/255,65/255,1)
    database = mysql.connector.Connect(host="localhost", user="root", password="", database="loginform")
    cursor = database.cursor()
    cursor.execute("select * from logindata")
    for i in cursor.fetchall():
        print(i[0], i[1])

    def build(self):
        return Builder.loadstring(kv)

    def get_id(self,instance):
        for id, widget in instance.parent.parent.parent.ids.items():
            if widget.__self__ == instance:
                return id

    def change_color(self,instance):
        if self.get_id(instance) == "color1":
            self.btn_color = (139/255,202/255,193/255,1)
            self.roots.ids.color1.icon = "circle"
        elif self.get_id(instance) == "color2":
            self.btn_color = (139/255,202/255,193/255,1)
        elif self.get_id(instance) == "color3":
            self.btn_color = (139/255,202/255,193/255,1)

    def send_data(self, email, password):
        if re.fullmatch(self.regex,email):
            self.cursor.execute(f"insert into logindata values ('{email.text}','{password.text}')")
            self.database.commit()
            email.text = ""
            password.text = ""

    def receive_data(self, username, password):

        self.cursor.execute("select * from logindata")
        email_list = []
        for i in self.cursor.fetchall():
            email_list.append(i[0])
        if username.text in email_list and username.text!= "":
            self.cursor.execute(f"select password from logindata where username = '{email.text}'")
            for j in self.cursor:
                if password.text == j[0]:
                    print("You have successfully logged in!")
                else:
                    print("Incorrect Password")
            else:
                print("Incorrect Username")



if __name__== "__main__":
    LabelBase.register(name = "Poppins", fn_regular="font-family: 'Montserrat', sans-serif")
    LabelBase.register(name="BPoppins", fn_italic="font-family: 'PT Sans', sans-serif")

# For sql I'm assuming database (Loginform) and table in it name (Logindata) with entry email varchar(255) , password varchar(255);

