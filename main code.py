import arcade
import arcade.gui
import random
import arabic_reshaper
from bidi.algorithm import get_display


def fix_hebrew(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def wrap_text(text, max_chars):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            lines.append('')
            current_line = word

    lines.append(current_line.strip())
    return lines

description_text_view1 = 'ברוך הבא!'

description_text_view2 = """ברוכים הבאים למשחק זיהוי AI!
לפניכם יוצגו זוגות של תמונות – אחת אמיתית ואחת שנוצרה על ידי בינה מלאכותית.
המשימה שלכם: ללחוץ על התמונה שלדעתכם היא האמיתית.
שימו לב לפרטים הקטנים: אצבעות, השתקפויות וטקסטורות מוזרות...
ה-AI לא תמיד מושלם!"""

description_text_view3='לחצו על התמונה האמיתית'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pics = [{'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.58.jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (1).jpeg",'clue':''},
        {'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (2).jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.58 (3).jpeg",'clue':''},
        {'Ai':r"assets/WhatsApp Image 2026-04-13 at 17.31.59.jpeg",'real':r"assets/WhatsApp Image 2026-04-13 at 17.31.59 (1).jpeg",'clue':''}]
background_view2 = r"assets/WhatsApp Image 2026-04-13 at 17.36.55.jpeg"
clue_pic = r"assets/pngtree-cute-hand-drawn-cartoon-lamp-with-yellow-light-vector-png-image_14109462.png"

real_pics = []
AI_pics= []
for pic in pics:
    AI_pics.append(pic['Ai'])
    real_pics.append(pic['real'])

class View2(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture(background_view2)

        #continue button
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        continue_button = arcade.gui.UIFlatButton(text='continue', width=100, height=50, style={"normal": {"bg_color": arcade.color.GREEN},"hover": {"bg_color": arcade.color.DARK_GREEN},"press": {"bg_color": arcade.color.DARK_YELLOW},})
        continue_button.center_x = SCREEN_WIDTH - 150
        continue_button.center_y = 75
        continue_button.on_click = self.continue_to_view3
        self.manager.add(continue_button)

    def continue_to_view3(self, event):
        self.window.show_view(View3())

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,arcade.rect.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT))

        y = SCREEN_HEIGHT - 100
        paragraphs = description_text_view2.split("\n")

        for paragraph in paragraphs:
            lines = wrap_text(paragraph, 50)

            for line in lines:
                fixed_line = fix_hebrew(line)
                arcade.draw_text(fixed_line,SCREEN_WIDTH - 50,y,arcade.color.BLACK,14,anchor_x="right")
                y -= 25
                y -= 10
        self.manager.draw()

class View3(arcade.View):
    def __init__(self):
        super().__init__()
        self.pics = pics.copy()
        self.player_score = 0
        self.player_life = 3
        self.pic_height = SCREEN_HEIGHT*0.7
        self.pic_width = SCREEN_WIDTH*0.487
        arcade.set_background_color(arcade.color.DARK_BLUE)
        arcade.AI = ''
        arcade.real = ''
        self.AI = r'assets/WhatsApp Image 2026-04-13 at 17.31.59.jpeg'
        self.real = r'assets/WhatsApp Image 2026-04-13 at 17.31.59 (1).jpeg'
        self.clue = 'תמונות AI פחות ריאליסטיות'
        self.show_clue = False

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        #תמונה AI
        self.texture1 , self.texture2 = self.random_position()
        texture_1 = arcade.load_texture(self.texture1)
        self.button1 = arcade.gui.UITextureButton(texture=texture_1,
                                               width=self.pic_width,
                                               height=self.pic_height,
                                               x= 0,
                                               y=SCREEN_HEIGHT*0.133)
        self.manager.add(self.button1)
        #תמונה אמיתית
        self.txture_2 = arcade.load_texture(self.texture2)
        self.button2 = arcade.gui.UITextureButton(texture=self.txture_2,
                                                    width=self.pic_width,
                                                    height=self.pic_height,
                                                    x= SCREEN_WIDTH * 0.512 ,
                                                 y= SCREEN_HEIGHT*0.133)
        self.manager.add(self.button2)
        self.button2.on_click = self.button2_pressed
        self.button1.on_click = self.button1_pressed

        #רמז
        self.txture3 = arcade.load_texture(clue_pic)
        self.clue_button = arcade.gui.UITextureButton(texture=self.txture3,
                                                      width=SCREEN_WIDTH*0.04,
                                                      height=SCREEN_HEIGHT*0.03,
                                                      x= SCREEN_WIDTH*0.95,
                                                      y=SCREEN_HEIGHT*0.0333)
        self.manager.add(self.clue_button)
        self.clue_button.on_click = self.clue_button_clicked

    def random_position(self):
        button = [self.AI,self.real]
        buttons = button.copy()
        texture1 = random.choice(buttons)
        buttons.remove(texture1)
        texture2 = buttons[0]
        return texture1,texture2

    def clue_button_clicked(self, event):
        self.show_clue = True
    def button1_pressed(self, event):
        self.run_pics()
        self.clear()
        if self.texture1 in AI_pics:
            self.player_life -= 1

        if self.texture1 in real_pics:
            self.player_score += 1

    def button2_pressed(self, event):
        self.run_pics()
        self.clear()
        if self.texture2 in AI_pics:
            self.player_life -= 1

        if self.texture2 in real_pics:
            self.player_score+=1

    def run_pics(self):
        self.show_clue = False
        selected_pictures = random.choice(self.pics)
        self.pics.remove(selected_pictures)
        AI_picture = selected_pictures['Ai']
        real_picture = selected_pictures['real']
        self.clue = selected_pictures['clue']
        self.AI = arcade.load_texture(AI_picture)
        self.real= arcade.load_texture(real_picture)
        self.button2.texture = self.real
        self.button2.texture_pressed = self.real
        self.button2.texture_hovered = self.real
        self.button1.texture = self.AI
        self.button1.texture_pressed = self.AI
        self.button1.texture_hovered = self.AI

    def on_draw(self) :
        self.clear()
        self.manager.draw()
        arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH*0.487,SCREEN_WIDTH*0.512,SCREEN_HEIGHT*0.133,SCREEN_HEIGHT*0.833,arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_filled(0,SCREEN_WIDTH,SCREEN_HEIGHT*0.1,SCREEN_HEIGHT*0.133,arcade.color.BLACK)
        arcade.draw_lrbt_rectangle_filled(0,SCREEN_WIDTH,SCREEN_HEIGHT*0.833,SCREEN_HEIGHT*0.866,arcade.color.BLACK)

        arcade.draw_text(fix_hebrew(description_text_view3),SCREEN_WIDTH*0.35,SCREEN_HEIGHT*0.9,arcade.color.RED,20)

        arcade.draw_text(f'score: {self.player_score}',SCREEN_WIDTH*0.025,SCREEN_HEIGHT*0.9,arcade.color.RED,20)
        arcade.draw_text(f'life: {self.player_life}',SCREEN_WIDTH*0.9,SCREEN_HEIGHT*0.9,arcade.color.RED,20)

        if self.show_clue:
            arcade.draw_text(fix_hebrew(self.clue), SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.03,arcade.color.WHITE,20)


window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,'Hacaton project 2026')
window.show_view(View2())
arcade.run()