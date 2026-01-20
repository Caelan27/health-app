from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ListProperty


class QuizScreen(Screen):
    current_question = NumericProperty(0)
    score = NumericProperty(0)
    question_text = StringProperty("")
    option_a = StringProperty("")
    option_b = StringProperty("")
    option_c = StringProperty("")
    option_d = StringProperty("")
    result_text = StringProperty("")
    
    questions = [
        {
            "question": "How many hours of sleep should teenagers get each night?",
            "options": ["5-6 hours", "7-8 hours", "8-10 hours", "10-12 hours"],
            "correct": 2
        },
        {
            "question": "How much water should you drink daily?",
            "options": ["2-3 cups", "4-5 cups", "6-8 cups", "10-12 cups"],
            "correct": 2
        },
        {
            "question": "How many minutes of exercise per day is recommended?",
            "options": ["15 minutes", "30 minutes", "60 minutes", "90 minutes"],
            "correct": 2
        },
        {
            "question": "Which is the healthiest breakfast option?",
            "options": ["Sugary cereal", "Whole grain toast with fruit", "Donuts", "Skip breakfast"],
            "correct": 1
        },
        {
            "question": "How many servings of fruits and vegetables per day?",
            "options": ["1-2 servings", "3-4 servings", "5 or more servings", "No specific amount"],
            "correct": 2
        }
    ]
    
    def on_enter(self):
        """Called when the screen is entered"""
        self.reset_quiz()
    
    def reset_quiz(self):
        """Reset the quiz to the beginning"""
        self.current_question = 0
        self.score = 0
        self.result_text = ""
        self.load_question()
    
    def load_question(self):
        """Load the current question"""
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_text = q["question"]
            self.option_a = q["options"][0]
            self.option_b = q["options"][1]
            self.option_c = q["options"][2]
            self.option_d = q["options"][3]
        else:
            self.show_results()
    
    def check_answer(self, answer_index):
        """Check if the answer is correct and move to next question"""
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            if answer_index == q["correct"]:
                self.score += 1
            
            self.current_question += 1
            self.load_question()
    
    def show_results(self):
        """Show the final results"""
        total = len(self.questions)
        percentage = (self.score / total) * 100
        self.result_text = f"Quiz Complete!\n\nYour Score: {self.score}/{total}\n({percentage:.0f}%)\n\n"
        
        if percentage >= 80:
            self.result_text += "Excellent! You know a lot about healthy living!"
        elif percentage >= 60:
            self.result_text += "Good job! Keep learning about healthy habits!"
        else:
            self.result_text += "Keep studying! Review the information section."
