from artcle_rewriter.article_rewriter import AIRewriter

class Article:
    def __init__(self, title: str, anonse: str, text: str) -> None:
        self.title = title
        self.anonse = anonse
        self.text = text
    
    
class ArticleManager:
    def __init__(self, ai_rewr_obj: AIRewriter) -> Article:
        if isinstance(ai_rewr_obj, AIRewriter):
            self.ai_rewr_obj = ai_rewr_obj
        else:
            raise Exception(f"AI rewriter must be instance of class AIRewriter, but got: {type(ai_rewr_obj)}")
        
    
    def trigger_rewriting(self):
        results = self.ai_rewr_obj.gpt_rewriter()
        
        for result_index, data in results.items():
            text = data.get('text', '')
            curr_ai_score = self.ai_rewr_obj.get_ai_detection_edenai(text)
            results[result_index]['ai_score'] = curr_ai_score
        
        best_result_index = min(results, key=lambda x: results[x]['ai_score']['ai_score'])
        best_result = results[best_result_index]
        
        return Article(
            title=best_result.get('title', ''),
            anonse=best_result.get('subtitle', ''),
            text=best_result.get('text', '')
        )
        
        
        
        
        
    