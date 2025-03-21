import json
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableLambda

class CourseGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            api_key='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',
            temperature=0,
            model_name="gemma2-9b-it"
        )

        self.initial_prompt_template = """ 
        Design a comprehensive and well-structured course for learning {skill}. 
        The response should be formatted strictly as valid JSON, without any additional text.

        Example JSON output:
        {{
            "course_name": "Python Programming",
            "modules": [
                {{
                    "Module Name": "Introduction to Python",
                    "Topics Covered": ["Variables", "Data Types"],
                    "Free Articles": [
                        {{"Title": "Python Basics", "link": "https://example.com"}}
                    ],
                    "YouTube Video": {{"Title": "Python Crash Course", "link": "https://youtube.com"}}
                }}
            ]
        }}
        """

        self.initial_prompt = PromptTemplate(template=self.initial_prompt_template, input_variables=["skill"])
        self.course_chain = self.initial_prompt | self.llm  

        self.article_prompt_template = """
        Using the module details: {module_name}, {topics}, {free_articles}, {youtube_video},
        generate a full-length article covering the module in-depth.

        Example JSON output:
        {{
            "title": "{module_name}",
            "content": "Detailed explanation covering all the topics...",
            "resources": [
                {{"type": "article", "title": "Python Basics", "link": "https://example.com"}},
                {{"type": "video", "title": "Python Crash Course", "link": "https://youtube.com"}}
            ]
        }}
        """

        self.article_prompt = PromptTemplate(template=self.article_prompt_template, 
                                             input_variables=["module_name", "topics", "free_articles", "youtube_video"])
        self.article_chain = self.article_prompt | self.llm  

    def generate_course_blueprint(self, skill):
        """ Generate a course blueprint based on the given skill """
        output = self.course_chain.invoke({"skill": skill})

        if hasattr(output, 'content'):
            output = output.content  

        print(f"Raw LLM Response: {output}")  # Debugging

        if not output.strip():  
            raise ValueError("LLM returned an empty response.")

        try:
            return json.loads(output)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format received from LLM. Raw output: {output}")

    def generate_module_article(self, module):
        """ Generate a detailed article for a module """
    
        module_name = module.get("Module Name", "Unnamed Module")
        topics_list = module.get("Topics Covered", [])
        free_articles_list = module.get("Free Articles", [])
        youtube_video_info = module.get("YouTube Video", {})
    
        topics_str = ", ".join(topics_list)
        free_articles_str = "; ".join([f'{item.get("Title", "Untitled")}: {item.get("link", "#")}' for item in free_articles_list])
        youtube_video_str = f'{youtube_video_info.get("Title", "No Video")}: {youtube_video_info.get("link", "#")}'
    
        # Send module details in the prompt
        article = self.article_chain.invoke({
            "module_name": module_name,
            "topics": topics_str,
            "free_articles": free_articles_str,
            "youtube_video": youtube_video_str
        })
    
        if hasattr(article, 'content'):
            article = article.content  
    
        if not article.strip():
            raise ValueError("LLM returned an empty response for the article.")
    
        return article