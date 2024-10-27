import pyray as pr

class ServerInputWindow:
    def __init__(self):
        self.server_ip = ""
        self.server_port = ""
        self.input_active = False
        self.input_type = "ip"  # Can be "ip" or "port"
        self.ip_box = pr.Rectangle(20, 50, 360, 30)
        self.port_box = pr.Rectangle(20, 130, 360, 30)
        self.submit_button = pr.Rectangle(150, 170, 100, 30)
        self.submitted = False

    def start(self):
        pr.init_window(400, 220, "Enter Server Details")
        pr.set_target_fps(60)

        while not pr.window_should_close():
            self.handle_input()
            self.render()

            if self.submitted:
                pr.close_window()
                break

        return self.server_ip, int(self.server_port)

    def handle_input(self):
        mouse_point = pr.get_mouse_position()

        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
            if pr.check_collision_point_rec(mouse_point, self.ip_box):
                self.input_type = "ip"
                self.input_active = True
            elif pr.check_collision_point_rec(mouse_point, self.port_box):
                self.input_type = "port"
                self.input_active = True
            elif pr.check_collision_point_rec(mouse_point, self.submit_button):
                if self.server_ip and self.server_port:
                    self.submitted = True
            else:
                self.input_active = False

        if self.input_active:
            if self.input_type == "ip":
                self.server_ip = self.get_input_text(self.server_ip)
            elif self.input_type == "port":
                self.server_port = self.get_input_text(self.server_port)

    def get_input_text(self, current_text):
        key = pr.get_key_pressed()
        if key >= 32 and key <= 125:
            current_text += chr(key)
        elif key == pr.KeyboardKey.KEY_BACKSPACE and len(current_text) > 0:
            current_text = current_text[:-1]
        return current_text

    def render(self):
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("Enter Server IP:", 20, 20, 20, pr.DARKGRAY)
        self.draw_textbox(self.ip_box, self.server_ip, self.input_type == "ip")

        pr.draw_text("Enter Server Port:", 20, 100, 20, pr.DARKGRAY)
        self.draw_textbox(self.port_box, self.server_port, self.input_type == "port")

        self.draw_button(self.submit_button, "Submit")

        pr.end_drawing()

    def draw_textbox(self, box, text, active):
        mouse_point = pr.get_mouse_position()
        if pr.check_collision_point_rec(mouse_point, box):
            pr.draw_rectangle_rec(box, pr.LIGHTGRAY)
        else:
            pr.draw_rectangle_rec(box, pr.GRAY)

        pr.draw_rectangle_lines_ex(box, 1, pr.DARKGRAY)
        pr.draw_text(text, int(box.x) + 5, int(box.y) + 5, 20, pr.BLACK)

    def draw_button(self, button, text):
        mouse_point = pr.get_mouse_position()
        if pr.check_collision_point_rec(mouse_point, button):
            pr.draw_rectangle_rec(button, pr.LIGHTGRAY)
        else:
            pr.draw_rectangle_rec(button, pr.GRAY)

        pr.draw_rectangle_lines_ex(button, 1, pr.DARKGRAY)
        pr.draw_text(text, int(button.x) + 10, int(button.y) + 5, 20, pr.BLACK)