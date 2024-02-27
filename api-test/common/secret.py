bear_token_dev = (
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFIVnZibWN1ZEhKcGJtaEFkR2hsYldGeWRHVmpMbU52YlE9PSIsImF1dGhfaWQiOiJhMTQ2OWI2Mi0wM2E0LTRhZTktYWIyMi01Zjc3MjEwY2ZjYjYiLCJjb21wYW55X2lkIjoiY2E0OTg5NzQtMWFmZC00N2M0LWJiNTgtODE4NTlkYzY1YTM2IiwiY29tcGFueV9uYW1lIjoidGhlIE1hcnRlYyIsImF1ZCI6IkJyb3dzZXIiLCJwbGF0Zm9ybSI6IkVNUExPWUVSIiwic2VydmljZSI6IlNUVURJTyIsImlhdCI6MTcwOTAwMTI3NywiZXhwIjoxNzA5MDg3Njc3fQ.lwI4EYuHRAIS-subyg8OU8dK6PgxaX6NC6K1fR0AB9o')

bear_token_stg = (
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFIVnZibWN1ZEhKcGJtaEFkR2hsYldGeWRHVmpMbU52YlE9PSIsImF1dGhfaWQiOiIzZDc3M2E2Ni02ZjM2LTRlN2ItYjAxNi1kZjZmMjNiYzBjN2UiLCJjb21wYW55X2lkIjoiYzJiZWExZDktNDhmYS00YTQ1LThkMDgtM2NjNDAwNGU3ODY0IiwiY29tcGFueV9uYW1lIjoiVGhlIE1hcnRlYyIsImF1ZCI6IkJyb3dzZXIiLCJwbGF0Zm9ybSI6IkVNUExPWUVSIiwic2VydmljZSI6IlNUVURJTyIsImlhdCI6MTcwOTAyNzQ1MSwiZXhwIjoxNzA5MTEzODUxfQ.v2LIB5c7TeYTNJwM2Ocj7i4Xa2BuptGLwPzvwL8vM3A')


class MartecSecret:

    def __init__(self, base_url):
        self.base_url = base_url

    def get_martec_header(self):
        if "staging" in self.base_url:
            headers = {'Authorization': bear_token_stg}
        elif "dev" in self.base_url:
            headers = {'Authorization': bear_token_dev}
        else:
            headers = ""
        return headers

    def get_martec_token(self):
        if "staging" in self.base_url:
            return bear_token_stg
        elif "dev" in self.base_url:
            return bear_token_dev
        else:
            return ""

    def get_header_with_content_type(self):
        if "staging" in self.base_url:
            headers = {'Authorization': self.get_martec_token(), 'Content-Type': 'application/json'}
        elif "dev" in self.base_url:
            headers = {'Authorization': self.get_martec_token(), 'Content-Type': 'application/json'}
        else:
            headers = ""
        return headers

    def get_token_for_brand_kit_tab_api(self):
        if "staging" in self.base_url:
            return 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFIVnZibWN1ZEhKcGJtaEFkR2hsYldGeWRHVmpMbU52YlE9PSIsImF1dGhfaWQiOiIzZDc3M2E2Ni02ZjM2LTRlN2ItYjAxNi1kZjZmMjNiYzBjN2UiLCJjb21wYW55X2lkIjoiYzJiZWExZDktNDhmYS00YTQ1LThkMDgtM2NjNDAwNGU3ODY0IiwiY29tcGFueV9uYW1lIjoiVGhlIE1hcnRlYyIsImF1ZCI6IkJyb3dzZXIiLCJjcmVhdGVkX2F0IjoiMjAyNC0wMi0xOVQxMzo1MToyMS42MjdaIiwicGxhdGZvcm0iOiJFTVBMT1lFUiIsImlhdCI6MTcwOTAyNzMyNiwiZXhwIjoxNzA5MTEzNzI2fQ.ScflktwuUhmqs6ypCf4TNbPydNWZHufJawaR0ELsZIw'
        elif "dev" in self.base_url:
            return 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFIVnZibWN1ZEhKcGJtaEFkR2hsYldGeWRHVmpMbU52YlE9PSIsImF1dGhfaWQiOiJhMTQ2OWI2Mi0wM2E0LTRhZTktYWIyMi01Zjc3MjEwY2ZjYjYiLCJjb21wYW55X2lkIjoiY2E0OTg5NzQtMWFmZC00N2M0LWJiNTgtODE4NTlkYzY1YTM2IiwiY29tcGFueV9uYW1lIjoidGhlIE1hcnRlYyIsImF1ZCI6IkJyb3dzZXIiLCJjcmVhdGVkX2F0IjoiMjAyNC0wMi0xOVQxMDozNjozNS42MzRaIiwicGxhdGZvcm0iOiJFTVBMT1lFUiIsImlhdCI6MTcwODk5OTc1NSwiZXhwIjoxNzA5MDg2MTU1fQ.htJB6mW0q1sTyAHpbXiaxzd4tsvBLKOu7BsXWF9WkqU'
        else:
            return ""
