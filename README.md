## Overview
A python-based Discord chatbot that helps users practice spanish through conversation, quizzes, and grammar explanations. The bot can respond to questions, test vocabulary, and provide feedback.  

### Features
Interactive Spanish conversation practice  
Vocabulary quizzes (grammar, verbs, vocab)  
Grammar explanations  
Sentence correction and feedback  
AI-powered responses using OpenAI API  

### Technologies
Python  
OpenAI API  
discord.py  
python-dotenv  

### Deployment
The bot is hosted on Railway and runs continuously as a worker service.  
Environmental variables are configured on the hosting platform to securely store the Discord and OpenAI API keys.  

The application automatically starts the bot when the service is deployed.  

### Example Commands
!quiz verbs  
!quiz grammar  
!quiz basics  

### Future Improvements
* Progress tracking for individual users  
* Short-term conversation memory  
