import allure
import os

from common_src.pages.story_builder import StoryBuilderPage
from common_src.pages.main_employer import MainEmployerPage


@allure.title("[C2597] Category - Proposal topics are generated for each category")
@allure.description(f"Categories are displayed with corresponding proposal topics are generated for each category")
@allure.testcase(f"{os.getenv('TESTRAIL_URL')}2597")
def test_category(set_up_tear_down):
    page = set_up_tear_down
    with allure.step("Access Story Builder tab"):
        MainEmployerPage(page).access_story_builder_tab()
        story_builder_page = StoryBuilderPage(page)
        # story_builder_page.click_on_employer_branding_category_tab()
    with allure.step("Employer Branding - Validate Proposal Topic List"):
        topic_txt_1 = ('Diversity, Equity and InclusionCultureThought LeadershipTechnical InsightsCareer StoriesEarly '
                       'CareerLeadership StoriesTestimonial VideosCreate Custom Story')
        story_builder_page.check_categories_topic_list(topic_txt_1)
    with allure.step("Talent Acquisition - Validate Proposal Topic List"):
        topic_txt_2 = ("Hiring Manager Q&ADay In The LifeCandidate ObjectionsPerks and BenefitsOur Tech StackInside "
                       "Look Into TeamCreate Custom Story")
        story_builder_page.click_on_talent_acquisition_category_tab()
        story_builder_page.check_categories_topic_list(topic_txt_2)
