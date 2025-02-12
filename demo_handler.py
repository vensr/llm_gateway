from flowise_llm import FlowiseLLM
from dotenv import get_key

class DemoHelper(FlowiseLLM):

    def __init__(self):               
        self.api_url = get_key('.env', 'DEMO_URL')
    
demo_model = DemoHelper()
