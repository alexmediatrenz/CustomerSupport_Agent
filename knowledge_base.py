
This file covers basic queries about services, contact info, and hours, as well as detailed responses for follow-up questions (e.g., about SEO or social media). It also includes an entry for urgent issues to support escalation.

---

### 2. Knowledge Base Initialization (`knowledge_base.py`)
This script defines a custom knowledge base class that loads the `faqs.txt` file and provides a simple search mechanism. Since Agno is assumed to support text-based knowledge bases, we’ll create a class that parses the file and performs keyword matching. This is a basic approach; a vector database would use embeddings for semantic similarity, but we’ll keep it simple for now.

**`knowledge_base.py`**
```python
class TextFileKnowledgeBase:
    def __init__(self, file_path):
        """Initialize the knowledge base with a text file."""
        self.file_path = file_path
        self.qa_pairs = {}
        self.load()

    def load(self):
        """Load question-answer pairs from the text file."""
        with open(self.file_path, 'r') as f:
            content = f.read().strip().split('---')
            for entry in content:
                if entry.strip():
                    question, answer = entry.strip().split('\nA: ')
                    question = question.replace('Q: ', '').strip()
                    self.qa_pairs[question.lower()] = answer.strip()

    def search(self, query):
        """Search for the most relevant answer based on keyword matching."""
        query_lower = query.lower()
        best_match = None
        highest_score = 0

        for question, answer in self.qa_pairs.items():
            question_words = set(question.split())
            query_words = set(query_lower.split())
            score = len(question_words.intersection(query_words))
            
            if score > highest_score:
                highest_score = score
                best_match = answer

        # Return the answer if there's a reasonable match, otherwise None
        return best_match if highest_score > 0 else None
