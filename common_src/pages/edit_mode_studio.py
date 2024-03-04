import re

from playwright.sync_api import expect


class EditModeStudioPage:

    def __init__(self, page):
        self.page = page

    def click_on_text_effects_and_cards(self):
        self.page.locator("p").filter(has_text="Text Effects & Cards").click()

    def click_on_text_effects_tab(self):
        self.page.get_by_text("Text Effects", exact=True).click()

    def click_on_text_effects_headline_text_option(self):
        self.page.get_by_text("Headline Text").click()

    def move_slider_to_active_headline_update(self):
        handle = self.page.query_selector(".slide-handle")
        slider_width = float(handle.bounding_box()['width'])
        slider_track = self.page.locator('.slide-handle')
        # slider_width = slider_track.evaluate("return el.getBoundingClientRect().width")
        print(f"slider_width: {slider_width}")
        desired_x = 0.5 * slider_width
        print(f"desired_x: {desired_x}")
        # Hover over starting position (force=True for interactive elements)
        slider_track.hover(force=True, position={"x": 0, "y": 0})
        # Press and hold the left mouse button
        self.page.mouse.down()
        # Hover over calculated X coordinate and maintain 0 Y coordinate
        slider_track.hover(force=True, position={"x": desired_x, "y": 0})
        # Release the left mouse button
        self.page.mouse.up()

    def click_on_headline_text_in_preview(self):
        self.page.get_by_text("Headline Text").nth(1).click()

    def select_font_style(self):
        xpath = "//div[@id='react-select-2-placeholder']/following-sibling::div"
        self.page.locator(xpath).click()
        self.page.locator("#react-select-2-option-0-0").click()

    def check_font_style_is_selected(self, font_style):
        (expect(self.page.get_by_label("Text Effects & Cards"))
         .to_contain_text(font_style))

    def set_loaded_color_for_text(self):
        xpath = "//p[.='Colour']/following-sibling::div[2]/div"
        self.page.locator(xpath).click()

    def set_color_for_text(self, previous_color_code, new_color_code):
        xpath = f"//p[.='{previous_color_code}']/parent::div/div"
        self.page.locator(xpath).click()
        self.page.get_by_label("hex").fill(new_color_code)
        self.page.locator("//div[@class='css-kooiip']/div[1]").click()

    def set_loaded_color_for_background(self):
        self.page.locator("//p[.='Background Colour']/following-sibling::div[2]/div").click()

    def check_color_is_set(self, color_code):
        xpath = "//p[.='Colour']/following-sibling::div[1]"
        expect(self.page.locator(xpath)).to_contain_text(color_code)
        # (expect(self.page.get_by_label("Text Effects & Cards")).to_contain_text(color_code))

    def back_to_creative_studio(self):
        (self.page.locator("div").filter(has_text=re.compile(r"^Create Studio$"))
         .get_by_role("img").click())

    def check_timeline_has_video(self):
        xpath = "//div[contains(@id,'time-box') and @type='VIDEO']"
        expect(self.page.locator(xpath)).to_be_visible()

    def check_timeline_has_text_effects_as(self, text_type):
        expect(self.page.get_by_text(f"{text_type}")).to_be_visible()

    def check_timeline_has_card_as(self, card_name):
        expect(self.page.locator("#control-frame-editing").get_by_text(card_name)).to_be_visible()
