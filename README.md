# platform-automation
automation test for platform

# Required Set Up
- Playwright: 1.41.0
- Python: 3.11.5
- Pytest: 8.0.1
- Allure: 2.26.0

# Env Define
    - env_id = 1 for STAGING
    - env_id = 2 for DEV
    - browser: currently test for chrome (chromium)

# How to run test
- Precondition: Database connection to DEV, STAGING should be available
- Execution: From package `regression-test`,
  - To test all scripts: Execute `pytest --browser chromium --env_id=<env_id>  --alluredir=allure_results 
    --clean-alluredir`
  - To test single script: Execute `pytest tests/<test_file_name>.py --browser chromium --env_id=<env_id>  
    --alluredir=allure_results 
    --clean-alluredir`
    - Example: `pytest tests/test_studio_brand_kit.py --browser chromium --env_id=<env_id>  
    --alluredir=allure_results 
    --clean-alluredir`
- Report: view locally by `npx allure serve allure_results`  